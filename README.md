# Secure Backup Tool

Ce projet propose un outil complet pour le chiffrement, le déchiffrement et la vérification d'intégrité des fichiers en utilisant l'algorithme AES, ainsi que des options pour la sauvegarde locale ou dans le cloud (Azure).

## Fonctionnalités

- **Chiffrement local** des fichiers.
- **Déchiffrement local** des fichiers chiffrés.
- **Vérification de l'intégrité** des fichiers pour s'assurer qu'ils n'ont pas été altérés.
- **Sauvegarde et récupération via Azure Blob Storage**.

## Prérequis

- Python 3.8 ou supérieur.
- Bibliothèques Python :
  - `pycryptodome`
  - `argparse`
  - `azure-storage-blob` (pour la sauvegarde sur Azure)

Installez les dépendances nécessaires avec :
```bash
pip install -r requirements.txt
```

## Avant de Commencer

### Sélectionnez le Répertoire Approprié

Avant d'exécuter les commandes, assurez-vous de vous placer dans le répertoire approprié :

#### Pour les opérations locales (chiffrement, déchiffrement, vérification d'intégrité) :
```bash
cd locale_secure
```
#### Pour les opérations Azure (sauvegarde et récupération) :
```bash
cd azure_secure
```

## Utilisation

### 1. Chiffrement Local

Pour chiffrer un fichier localement et le sauvegarder dans un dossier :
```bash
python main.py -f /chemin/vers/fichier.txt -p MotDePasse -l /chemin/vers/dossier -e
```
**Exemple** :
```bash
python main.py -f /home/kali/fichier/omarbouhaddach.txt -p CODM -l /home/kali/fichier -e
```

### 2. Déchiffrement Local

Pour déchiffrer un fichier localement et sauvegarder le fichier déchiffré :
```bash
python main.py -f /chemin/vers/fichier_chiffré.txt.enc -p MotDePasse -l /chemin/vers/dossier -d
```
**Exemple** :
```bash
python main.py -f /home/kali/fichier/CODM.txt.enc -p CODM -l /home/kali/fichier -d
```

### 3. Vérification d'Intégrité Localement

Pour vérifier si le fichier chiffré correspond au fichier déchiffré en utilisant un hash :
```bash
python main.py -f /chemin/vers/fichier_original -p MotDePasse -l /chemin/vers/fichier_déchiffré -i
```
**Exemple** :
```bash
python main.py -f /home/kali/test/cryptage.txt -p HELLO1234 -l /home/kali/test/dec/cryptage.txt -i
```

### 4. Sauvegarde sur Azure

#### Chiffrement et Sauvegarde sur Azure Blob Storage

Pour chiffrer et sauvegarder un fichier directement sur un conteneur Azure Blob :
```bash
python Azure.py -f /chemin/vers/fichier -b nom_du_blob -c nom_du_conteneur -cs "chaîne_de_connexion"
```

#### Déchiffrement et Récupération depuis Azure Blob Storage

Pour déchiffrer et récupérer un fichier stocké sur un conteneur Azure Blob :
```bash
python Azure.py -f /chemin/vers/fichier -b nom_du_blob -c nom_du_conteneur -cs "chaîne_de_connexion" -d
```


## Structure du Projet

- **main.py** : Script principal pour le chiffrement, déchiffrement et vérification locale.
- **Azure.py** : Script pour la gestion des fichiers sur Azure Blob Storage.
- **encrypt.py** : Contient les fonctions de chiffrement/déchiffrement.
- **file_operations.py** : Gère les sauvegardes locales.
- **integrity_check.py** : Vérifie l'intégrité des fichiers à l'aide de hash.

## Sécurité

- **AES-256** est utilisé pour un chiffrement sécurisé.
- Le mot de passe de chiffrement doit être fort pour éviter les attaques par force brute.
- Les données sensibles (par exemple, `AccountKey` Azure) doivent être protégées et jamais exposées publiquement.

## Avertissements

- Toujours sauvegarder vos mots de passe et clés dans un endroit sécurisé.
- Testez le processus complet pour vous assurer qu'aucune donnée n'est perdue lors du chiffrement ou du transfert.

## Auteurs
**Omar Bouhaddach**

**Rayane Berrada**

**Aimad Bouya**

**Rania Fajri**
