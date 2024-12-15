import hashlib
import os

# Fonction pour calculer le hash du fichier
def calculate_hash(file_path):
    hash_sha256 = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            hash_sha256.update(chunk)
    
    return hash_sha256.hexdigest()

# Fonction pour vérifier l'intégrité du fichier
def check_integrity(file_path, hash_file):
    original_hash = calculate_hash(file_path)
    print(f"Hash SHA-256 du fichier {file_path}: {original_hash}")
    print("le fichier n'est pas modifier")
