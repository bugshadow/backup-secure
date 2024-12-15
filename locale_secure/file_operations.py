import os
import shutil

# Fonction pour sauvegarder localement le fichier chiffré
def save_locally(file_path, local_folder):
    if not os.path.exists(local_folder):  # Vérifier si le dossier existe
        os.makedirs(local_folder)  # Créer le dossier s'il n'existe pas
    shutil.copy(file_path, local_folder)  # Copier le fichier dans le dossier local
    print(f"Le fichier a été sauvegardé localement sous : {local_folder}/{os.path.basename(file_path)}")

