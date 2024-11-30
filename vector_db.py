from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.storage.storage_context import StorageContext
from llama_index.readers.json import JSONReader
from llama_index.vector_stores.postgres import PGVectorStore
from dotenv import load_dotenv
from deep_seekllm import DeepSeekLLM
import os
import time
import sys
import glob
from sqlalchemy import make_url
from logger_setup import setup_logger ,setup_query_time_logger

logger = setup_logger(__name__,log_to_file=True, log_file="vector_db.log")
query_time_logger = setup_query_time_logger()

load_dotenv()

def get_postgres_credentials():
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_pass = os.getenv("POSTGRES_PASSWORD")
    postgres_db = os.getenv("POSTGRES_DB")
    return postgres_user, postgres_pass, postgres_db


def create_vector_store():
    postgres_user, postgres_pass, postgres_db = get_postgres_credentials()
    connection_string = f"postgresql://{postgres_user}:{postgres_pass}@localhost:5432/{postgres_db}"
    url = make_url(connection_string)
    vector_store = PGVectorStore.from_params(
        database=postgres_db,
        host=url.host,
        password=url.password,
        port=url.port, 
        user=url.username, 
        table_name="linkedin_users",
        embed_dim=768
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

    documents = []
    for json_file in json_files:
        documents.extend(reader.load_data(input_file=json_file, extra_info={}))

    vector_store = create_vector_store()
    
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, show_progress=True)
    return index


def query_index(index, query):
    start_time = time.time()  # Start the timer
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time
    query_time_logger.info(f"Query executed in {elapsed_time:.2f} seconds.")  # Log to query_time.log
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
    "The results should be a list of 10 json values with their full profiles.\n"
    )
    user_query = "\n".join(query_tuple)
    response = query_index(index, user_query)
    logger.info(f"Response: {response}")