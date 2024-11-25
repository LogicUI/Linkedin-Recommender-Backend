from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
from crypto import load_key , decrypt_folder 
import logging
from dotenv import load_dotenv
import os 



logging.basicConfig(level=logging.INFO)


load_dotenv()

def create_llm():
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_SECRET_KEY")


if __name__ == "__main__":
    create_llm()
    key = load_key()
    source_file = "./encrypted_files"
    dest_file = "./decrypted_files"
    if not os.path.exists(dest_file):
        decrypt_folder(source_file, dest_file, key)
        logging.info(f"Folder {dest_file} created")
    else:
        logging.info(f"Folder {dest_file} exist using exising file")

