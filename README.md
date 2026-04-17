# Générateur de contenu à partir de transcription

Transforme automatiquement un fichier audio ou vidéo en contenu structuré
prêt à publier : résumé, article de blog ou post LinkedIn.

## Aperçu

1. Tu uploades un fichier audio (.mp3, .wav) ou vidéo (.mp4, .mov)
2. L'application transcrit la parole en texte via Whisper
3. GPT-4o génère le contenu dans le format choisi
4. Tu télécharges le résultat en .txt, .md ou .docx

## Stack technique

- **Streamlit** — interface web
- **Whisper (OpenAI)** — transcription audio locale et gratuite
- **GPT-4o (OpenAI API)** — génération de contenu
- **ffmpeg** — extraction audio depuis vidéo
- **Python 3.10**

## Prérequis

- Python 3.10+
- ffmpeg installé sur le système
- Une clé API OpenAI

## Installation

### 1. Cloner le projet

git clone https://github.com/TON_USERNAME/transcription-content-generator.git
cd transcription-content-generator

### 2. Installer ffmpeg

Windows :
winget install ffmpeg

Mac :
brew install ffmpeg

Linux :
sudo apt-get install ffmpeg

### 3. Créer l'environnement virtuel

python -m venv venv

Windows :
venv\Scripts\Activate.ps1

Mac/Linux :
source venv/bin/activate

### 4. Installer les dépendances Python

pip install -r requirements.txt

### 5. Configurer la clé API

cp .env.example .env

Ouvre .env et remplace par ta vraie clé OpenAI :
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

### 6. Lancer l'application

streamlit run app.py

L'application s'ouvre sur http://localhost:8501

## Installation avec Docker

### Prérequis

- Docker Desktop installé

### Lancer avec Docker

docker compose up --build

L'application s'ouvre sur http://localhost:8501

Pour arrêter :
docker compose down

## Structure du projet

transcription-content-generator/
│
├── app.py                          # Interface Streamlit
│
├── pipeline/
│   ├── extractor.py                # Extraction audio depuis vidéo (ffmpeg)
│   ├── transcriber.py              # Transcription audio → texte (Whisper)
│   ├── cleaner.py                  # Nettoyage de la transcription
│   └── generator.py                # Génération contenu via GPT-4o
│
├── prompts/
│   ├── summary_prompt.txt          # Template prompt résumé
│   ├── article_prompt.txt          # Template prompt article
│   └── linkedin_prompt.txt         # Template prompt LinkedIn
│
├── utils/
│   ├── file_handler.py             # Upload et export fichiers
│   └── session_state.py            # Gestion état Streamlit
│
├── Dockerfile                      # Image Docker
├── docker-compose.yml              # Orchestration Docker
├── requirements.txt                # Dépendances Python
├── .env.example                    # Template variables d'environnement
└── README.md                       # Ce fichier

## Pipeline de traitement

Fichier vidéo/audio
       ↓
extractor.py      → extrait la piste audio (ffmpeg)
       ↓
transcriber.py    → transcrit la parole en texte (Whisper)
       ↓
cleaner.py        → nettoie la transcription
       ↓
generator.py      → génère le contenu structuré (GPT-4o)
       ↓
Résumé / Article / Post LinkedIn

## Formats supportés

Vidéo : .mp4, .mov, .avi, .mkv, .webm
Audio : .mp3, .wav, .m4a, .ogg, .flac

## Formats d'export

- .txt — texte brut
- .md  — Markdown
- .docx — Word

## Auteur

Mohamed Belfilali — Projet réalisé dans le cadre du cursus IA