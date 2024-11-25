"""
This py file is used to encrypt the data folder that contains the JSON files for the project

The encryption is done using the Fernet module from the cryptography library
"""

import os
import sys
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()


def load_key() -> str:
    return os.getenv("DATA_SECRET_KEY")


def generate_key() -> None:
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


def _encrypt_file(source_file_path: str, dest_folder_path: str, key: str) -> None:
    fernet = Fernet(key)
    with open(source_file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    base_name = os.path.basename(source_file_path)
    dest_file_path = os.path.join(dest_folder_path, base_name)
    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
    with open(dest_file_path, "wb") as file:
        file.write(encrypted_data)


def _check_folder_errors(source_file_path: str, dest_folder_path: str) -> None:
    if not os.path.exists(source_file_path):
        logging.error(f"File {source_file_path} does not exist")
        sys.exit(1)

    if os.path.exists(dest_folder_path):
        logging.info(f"Folder {dest_folder_path} already exists")
        sys.exit(1)


def encrypt_folder(source_file_path: str, dest_folder_path: str, key: str) -> None:
    _check_folder_errors(source_file_path, dest_folder_path)
    for root, dirs, files in os.walk(source_file_path):
        for file in files:
            file_path = os.path.join(root, file)
            _encrypt_file(file_path, dest_folder_path, key)
            print(f"Encrypted {file_path} to {dest_folder_path}")


def _decrypt_file(source_file_path: str, dest_folder_path: str, key: str) -> None:
    fernet = Fernet(key)
    with open(source_file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    base_name = os.path.basename(source_file_path)
    dest_file_path = os.path.join(dest_folder_path, base_name)
    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
    with open(dest_file_path, "wb") as file:
        file.write(decrypted_data)


def decrypt_folder(source_file_path: str, dest_folder_path: str, key: str) -> None:
    _check_folder_errors(source_file_path, dest_folder_path)
    for root, dirs, files in os.walk(source_file_path):
        for file in files:
            file_path = os.path.join(root, file)
            logging.info(f"Decrypting {file_path}")
            _decrypt_file(file_path, dest_folder_path, key)
            logging.info(f"Decrypted {file_path} to {dest_folder_path}")


if __name__ == "__main__":
    key = load_key()
    source_file = "./encrypted_files"
    dest_file = "./decrypted_files"
    decrypt_folder(source_file, dest_file, key)
    
#    source_file = './encrypted_files/data'
#    dest_file = "./decrypted_files"
#    decrypt_folder(source_file, dest_file, key)
