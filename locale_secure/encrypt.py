from Crypto.Cipher import AES  # Pour le chiffrement/déchiffrement AES
from Crypto.Util.Padding import pad, unpad  # Pour gérer le remplissage des données
from Crypto.Protocol.KDF import scrypt  # Pour dériver une clé à partir d'un mot de passe
import os  # Pour la gestion des fichiers et la génération de données aléatoires

# Fonction pour générer une clé sécurisée à partir d'un mot de passe
def generate_key(password):
    # Génère un sel (16 octets aléatoires) pour rendre la dérivation unique
    salt = os.urandom(16)
    # Utilise l'algorithme scrypt pour dériver une clé sécurisée
    # key_len=32 : longueur de clé pour AES-256
    # N, r, p : paramètres pour ajuster la difficulté de scrypt
    key = scrypt(password.encode(), salt, key_len=32, N=2**14, r=8, p=1)
    return key, salt  # Retourne la clé dérivée et le sel

# Fonction pour chiffrer un fichier
def encrypt_file(file_path, password):
    # Génère la clé et le sel à partir du mot de passe
    key, salt = generate_key(password)
    # Crée un objet de chiffrement AES en mode CBC avec une clé aléatoire
    cipher = AES.new(key, AES.MODE_CBC)
    
    # Lit les données du fichier en mode binaire
    with open(file_path, 'rb') as f:
        data = f.read()
    
    # Ajoute un remplissage pour s'assurer que les données soient un multiple de la taille de bloc AES
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))

    # Détermine le nom du fichier chiffré en ajoutant l'extension `.enc`
    encrypted_file_path = f"{file_path}.enc"
    
    # Sauvegarde le fichier chiffré avec le sel, le IV et les données chiffrées
    with open(encrypted_file_path, 'wb') as f:
        f.write(salt)  # Écrit le sel en premier (16 octets)
        f.write(cipher.iv)  # Écrit le vecteur d'initialisation (IV, 16 octets)
        f.write(encrypted_data)  # Écrit les données chiffrées
    
    return encrypted_file_path  # Retourne le chemin du fichier chiffré

# Fonction pour déchiffrer un fichier
def decrypt_file(file_path, password):
    # Ouvre le fichier chiffré en mode binaire pour lecture
    with open(file_path, 'rb') as f:
        salt = f.read(16)  # Lit les 16 premiers octets pour récupérer le sel
        iv = f.read(16)  # Lit les 16 octets suivants pour récupérer le vecteur d'initialisation (IV)
        encrypted_data = f.read()  # Lit le reste du fichier pour récupérer les données chiffrées

    # Reproduit la clé dérivée à partir du mot de passe et du sel
    key = scrypt(password.encode(), salt, key_len=32, N=2**14, r=8, p=1)
    
    # Crée un objet de déchiffrement AES en mode CBC avec la clé et le IV
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    
    # Déchiffre les données et enlève le remplissage (padding)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    # Détermine le nom du fichier déchiffré en retirant l'extension `.enc`
    decrypted_file_path = file_path.replace('.enc', '.dec')
    
    # Sauvegarde les données déchiffrées dans un nouveau fichier
    with open(decrypted_file_path, 'wb') as f:
        f.write(decrypted_data)
    
    return decrypted_file_path  # Retourne le chemin du fichier déchiffré