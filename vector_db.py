from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.readers.json import JSONReader
from dotenv import load_dotenv
from deep_seekllm import DeepSeekLLM 
import logging
import os 
import sys
import glob

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()

def load_and_index_json(directory_path):
    if not os.path.exists(directory_path):
        logging.error(f"Folder {directory_path} does not exist")
        sys.exit(1)
        
    reader = JSONReader( 
        levels_back = 0,
        collapse_length=None, 
        ensure_ascii=False, 
        is_jsonl=False, 
        clean_json=True
    )
    
    json_files = glob.glob(os.path.join(directory_path, "*.json"))

    documents = []
    for json_file in json_files:
        documents.extend(reader.load_data(input_file=json_file, extra_info={}))
        
    index = VectorStoreIndex.from_documents(documents)
    return index

def query_index(index, query):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response


if __name__ == "__main__":
    Settings.llm = DeepSeekLLM()
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    Settings.embed_model = "local:BAAI/bge-base-en-v1.5"
    index = load_and_index_json("./decrypted_files")
    user_query = "Give a list of users who are software engineer in their occupations, in your response please return a list of eligible user json and their full json profiles"
    response = query_index(index, user_query)
    logging.info(f"Response: {response}")
    
