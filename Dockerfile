# Dockerfile

# --- IMAGE DE BASE ---
# On part d'une image Python 3.10 officielle sur Linux slim
# "slim" = version allégée sans outils inutiles, moins lourde
FROM python:3.10-slim

# --- VARIABLES D'ENVIRONNEMENT SYSTÈME ---
# Empêche Python de créer des fichiers .pyc inutiles dans le conteneur
ENV PYTHONDONTWRITEBYTECODE=1
# Force Python à afficher les logs immédiatement sans les bufferiser
# Important pour voir les logs Streamlit en temps réel
ENV PYTHONUNBUFFERED=1

# --- INSTALLATION DE FFMPEG ---
# apt-get est le gestionnaire de paquets Linux (comme winget sur Windows)
# On installe ffmpeg directement dans le conteneur — plus besoin de le
# faire manuellement sur chaque machine
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --- DOSSIER DE TRAVAIL ---
# Crée et définit /app comme dossier de travail dans le conteneur
# Toutes les commandes suivantes s'exécutent depuis ce dossier
WORKDIR /app

# --- INSTALLATION DES DÉPENDANCES PYTHON ---
# On copie UNIQUEMENT requirements.txt en premier
# Pourquoi ? Docker le readmet en cache chaque étape — si requirements.txt
# ne change pas, Docker réutilise le cache et ne réinstalle pas tout
# C'est beaucoup plus rapide lors des rebuilds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- COPIE DU CODE ---
# On copie le reste du projet APRÈS les dépendances
# Ainsi modifier app.py ne force pas à réinstaller toutes les libs
COPY . .

# --- PORT ---
# Informe Docker que le conteneur écoute sur le port 8501
# C'est le port par défaut de Streamlit
EXPOSE 8501

# --- COMMANDE DE DÉMARRAGE ---
# Lance Streamlit quand le conteneur démarre
# --server.address=0.0.0.0 → accessible depuis l'extérieur du conteneur
# --server.port=8501 → port d'écoute
# --server.fileWatcherType=none → désactive le hot-reload inutile en prod
CMD ["streamlit", "run", "app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.fileWatcherType=none"]