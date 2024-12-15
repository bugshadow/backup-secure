import argparse  # Module pour analyser les arguments de ligne de commande
from encrypt import encrypt_file, decrypt_file  # Importation des fonctions de chiffrement et déchiffrement
from file_operations import save_locally  # Fonction pour sauvegarder un fichier localement
from integrity_check import check_integrity  # Fonction pour vérifier l'intégrité d'un fichier
import os  # Module pour manipuler les chemins et les fichiers

# Fonction principale du script
def main():
    # Création d'un parser pour gérer les arguments de ligne de commande
    parser = argparse.ArgumentParser(description="Outil de sauvegarde sécurisé avec chiffrement AES")
    
    # Argument pour spécifier le fichier à traiter
    parser.add_argument("-f", "--file", required=True, help="Chemin du fichier à traiter")
    # Argument pour fournir le mot de passe pour le chiffrement/déchiffrement
    parser.add_argument("-p", "--password", required=True, help="Mot de passe pour le chiffrement/déchiffrement")
    # Argument pour indiquer le dossier où sauvegarder le fichier
    parser.add_argument("-l", "--local", required=True, help="Dossier de sauvegarde local")
    # Option pour activer le chiffrement
    parser.add_argument("-e", "--encrypt", action="store_true", help="Chiffrer le fichier")
    # Option pour activer le déchiffrement
    parser.add_argument("-d", "--decrypt", action="store_true", help="Déchiffrer le fichier")
    # Option pour vérifier l'intégrité d'un fichier
    parser.add_argument("-i", "--integrity", action="store_true", help="Vérifier l'intégrité du fichier")
    # Option pour spécifier le fichier où stocker ou comparer le hash
    parser.add_argument("-hf", "--hashfile", help="Fichier pour stocker le hash", default="file_hash.txt")
    
    # Analyse des arguments passés en ligne de commande
    args = parser.parse_args()

    # Si l'option de chiffrement est spécifiée
    if args.encrypt:
        # Chiffrement du fichier et récupération du chemin du fichier chiffré
        encrypted_file_path = encrypt_file(args.file, args.password)
        print(f"Le fichier a été chiffré et sauvegardé sous : {encrypted_file_path}")

        # Vérifie si le fichier chiffré est déjà dans le dossier de sauvegarde
        destination_path = os.path.join(os.path.abspath(args.local), os.path.basename(encrypted_file_path))
        if os.path.abspath(encrypted_file_path) != destination_path:
            # Sauvegarde le fichier chiffré dans le dossier local spécifié
            save_locally(encrypted_file_path, args.local)
        else:
            print("Le fichier chiffré est déjà dans le dossier de sauvegarde.")

    # Si l'option de déchiffrement est spécifiée
    elif args.decrypt:
        # Déchiffrement du fichier et récupération du chemin du fichier déchiffré
        decrypted_file_path = decrypt_file(args.file, args.password)
        print(f"Le fichier a été déchiffré et sauvegardé sous : {decrypted_file_path}")

        # Vérifie si le fichier déchiffré est déjà dans le dossier de sauvegarde
        destination_path = os.path.join(os.path.abspath(args.local), os.path.basename(decrypted_file_path))
        if os.path.abspath(decrypted_file_path) != destination_path:
            # Sauvegarde le fichier déchiffré dans le dossier local spécifié
            save_locally(decrypted_file_path, args.local)
        else:
            print("Le fichier déchiffré est déjà dans le dossier de sauvegarde.")

    # Si l'option de vérification d'intégrité est spécifiée
    elif args.integrity:
        # Appelle la fonction pour vérifier l'intégrité du fichier
        check_integrity(args.file, args.hashfile)

# Point d'entrée principal du script
if __name__ == "__main__":
    main()
