import os
import sys
from termcolor import colored
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from azure.storage.blob import BlobServiceClient

def check_root():
    if "SUDO_UID" not in os.environ.keys():
        print(colored("[*] ERROR: Run with sudo command so that the script will work!", "red"))
        exit()

def check_arguments():
    file = None
    container_name = None
    blob_name = None
    connection_string = None
    commands = {
        "-f": "Path of the file which you want to encrypt/decrypt.",
        "-c": "Container name.",
        "-b": "Blob name.",
        "-cs": "Azure connection string.",
        "-d": "Decrypt the file."
    }
    if len(sys.argv) > 1 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print("Usage:")
        for cmd, desc in commands.items():
            print(colored(f" {cmd} : ", "cyan"), desc)
        print("Ensure you provide the Azure information to connect, as well as the file path.")
        exit()
    if len(sys.argv) < 8:
        print(colored("[*] ERROR: Enter the required commands", "red"))
        print("Usage:")
        for cmd, desc in commands.items():
            print(colored(f"{cmd} :", "cyan"), desc)
        exit()

    try:
        file_index = sys.argv.index("-f") + 1
        file = sys.argv[file_index]
    except (ValueError, IndexError):
        print(colored("[*] ERROR: Missing required argument '-f' (file path)", "red"))
        exit()
    try:
        container_index = sys.argv.index("-c") + 1
        container_name = sys.argv[container_index]
    except (ValueError, IndexError):
        print(colored("[*] ERROR: Missing required argument '-c' (container name)", "red"))
        exit()
    try:
        blob_index = sys.argv.index("-b") + 1
        blob_name = sys.argv[blob_index]
    except (ValueError, IndexError):
        print(colored("[*] ERROR: Missing required argument '-b' (blob name)", "red"))
        exit()
    try:
        connection_index = sys.argv.index("-cs") + 1
        connection_string = sys.argv[connection_index]
    except (ValueError, IndexError):
        print(colored("[*] ERROR: Missing required argument '-cs' (connection string)", "red"))
        exit()

    return container_name, blob_name, connection_string, file

def encrypt_file(input_file, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    with open(input_file, "rb") as f:
        plaintext = f.read()
        padding_length = 16 - (len(plaintext) % 16)
        plaintext += bytes([padding_length] * padding_length)

    ciphertext = iv + cipher.encrypt(plaintext)
    return ciphertext

def decrypt_file(input_file, output_file, key):
    with open(input_file, "rb") as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    padding_length = plaintext[-1]
    plaintext = plaintext[:-padding_length]

    with open(output_file, "wb") as f:
        f.write(plaintext)

    print(f"File decrypted and saved as: {output_file}")
    return output_file

def upload_to_azure(connection_string, container_name, blob_name, data):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    container_client.upload_blob(name=blob_name, data=data, overwrite=True)
    print(f"File uploaded to Azure Blob Storage as: {blob_name}")

def download_from_azure(connection_string, container_name, blob_name, file_path):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    with open(file_path, "wb") as file:
        blob_data = container_client.download_blob(blob_name)
        file.write(blob_data.readall())

    print(f"File downloaded from Azure Blob Storage and saved as: {file_path}")

def compute_sha256(file_path):
    sha256 = SHA256.new()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.digest()

def main():
    check_root()
    container_name, blob_name, connection_string, file = check_arguments()

    if "-d" in sys.argv:
        # Decryption process
        encrypted_file_path = "downloaded_" + file
        decrypted_file_path = "decrypted_" + file.replace(".enc", "")

        # Download the encrypted file
        download_from_azure(connection_string, container_name, blob_name, encrypted_file_path)

        # Download the encryption key
        key_blob_name = blob_name + ".key"
        encryption_key_path = "key_" + key_blob_name
        download_from_azure(connection_string, container_name, key_blob_name, encryption_key_path)

        # Load the encryption key
        with open(encryption_key_path, "rb") as key_file:
            encryption_key = key_file.read()

        # Decrypt the file
        decrypt_file(encrypted_file_path, decrypted_file_path, encryption_key)

        # Check file integrity
        decrypted_hash = compute_sha256(decrypted_file_path)

        # Load original hash for integrity checking
        original_hash_blob_name = blob_name + ".hash"
        original_hash_path = "original_" + original_hash_blob_name
        download_from_azure(connection_string, container_name, original_hash_blob_name, original_hash_path)
        with open(original_hash_path, "rb") as f:
            original_hash = f.read()

        if original_hash == decrypted_hash:
            print(colored("[*] Integrity check PASSED: The decrypted file matches the original file.", "green"))
        else:
            print(colored("[*] Integrity check FAILED: The decrypted file does not match the original file.", "red"))
    else:
        # Encryption process
        encryption_key = get_random_bytes(32)

        # Compute and save the original file hash
        original_hash = compute_sha256(file)
        original_hash_blob_name = blob_name + ".hash"
        with open(original_hash_blob_name, "wb") as f:
            f.write(original_hash)

        # Upload original file hash to Azure
        upload_to_azure(connection_string, container_name, original_hash_blob_name, original_hash)

        encrypted_data = encrypt_file(file, encryption_key)

        # Upload the encrypted file to Azure
        upload_to_azure(connection_string, container_name, blob_name, encrypted_data)

        # Upload the encryption key to Azure
        key_blob_name = blob_name + ".key"
        upload_to_azure(connection_string, container_name, key_blob_name, encryption_key)

if __name__ == "__main__":
    main()
