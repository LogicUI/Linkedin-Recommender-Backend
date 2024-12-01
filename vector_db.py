from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.storage.storage_context import StorageContext
from llama_index.readers.json import JSONReader
from llama_index.vector_stores.postgres import PGVectorStore
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from deep_seekllm import DeepSeekLLM
from functools import lru_cache
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from logger_setup import setup_logger, setup_query_time_logger
import os
import time
import sys
import glob
import multiprocessing


logger = setup_logger(__name__, log_to_file=True, log_file="vector_db.log")
query_time_logger = setup_query_time_logger()

load_dotenv()

engine = None


def initialize_engine():
    """
    Initializes a global SQLAlchemy engine with connection pooling.
    """
    global engine
    if engine is None:
        postgres_user, postgres_pass, postgres_db = get_postgres_credentials()
        connection_url = URL.create(
            drivername="postgresql",
            username=postgres_user,
            password=postgres_pass,
            host="localhost",
            port=5432,
            database=postgres_db,
        )
        engine = create_engine(
            connection_url,
            pool_size=10,  # Max connections in the pool
            max_overflow=20,  # Extra connections if pool is full
            pool_recycle=3600,  # Recycle connections after 1 hour
            pool_timeout=30,  # Timeout for getting a connection
        )
    return engine


def get_postgres_credentials():
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_pass = os.getenv("POSTGRES_PASSWORD")
    postgres_db = os.getenv("POSTGRES_DB")
    return postgres_user, postgres_pass, postgres_db


@lru_cache(maxsize=1)
def create_vector_store():
    initialize_engine()
    postgres_user, postgres_pass, postgres_db = get_postgres_credentials()
    vector_store = PGVectorStore.from_params(
        database=postgres_db,
        host="localhost",
        password=postgres_pass,
        port=5432,
        user=postgres_user,
        table_name="linkedin_users",
        embed_dim=768,
    )
    return vector_store


def load_and_index_json(directory_path):
    if not os.path.exists(directory_path):
        logger.error(f"Folder {directory_path} does not exist")
        sys.exit(1)

    reader = JSONReader(
        levels_back=0,
        collapse_length=None,
        ensure_ascii=False,
        is_jsonl=False,
        clean_json=True,
    )

    json_files = glob.glob(os.path.join(directory_path, "*.json"))

    def process_file(json_file):
        return reader.load_data(input_file=json_file, extra_info={})

    documents = []
    max_workers = min(len(json_files), multiprocessing.cpu_count())
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_file, json_file) for json_file in json_files]
        for future in as_completed(futures):
            try:
                result = future.result()
                if isinstance(result, list):
                    documents.extend(result)
                else:
                    print(f"Unexpected result type: {type(result)}")
            except Exception as e:
                print(f"Future processing failed: {e}")

    vector_store = create_vector_store()

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, show_progress=True
    )

    return index


def query_index(index, query):
    start_time = time.time()
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    end_time = time.time()
    elapsed_time = end_time - start_time
    query_time_logger.info(f"Query executed in {elapsed_time:.2f} seconds.")
    return response


if __name__ == "__main__":
    ## Example usage
    Settings.llm = DeepSeekLLM()
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    Settings.embed_model = "local:BAAI/bge-base-en-v1.5"
    index = load_and_index_json("./processed_data")
    query_tuple = (
        "Please provide at least 10 unique JSON objects in a list.\n",
        "Each JSON object should have the full profile.\n",
        "Each user should be a Software Engineer with at least 3 years experience or more.\n",
        "Ensure all objects have unique values.\n",
        "The results should be a list of 10 json values with their full profiles.\n",
    )
    user_query = "\n".join(query_tuple)
    response = query_index(index, user_query)
    logger.info(f"Response: {response}")
