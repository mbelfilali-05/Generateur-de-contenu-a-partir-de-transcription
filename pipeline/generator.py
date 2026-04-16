# pipeline/generator.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Charge OPENAI_API_KEY depuis le fichier .env
load_dotenv()

# Client OpenAI — créé une seule fois au chargement du module
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Chemin absolu vers le dossier prompts/
# __file__ = chemin de ce fichier (generator.py)
# on remonte d'un niveau pour atteindre la racine du projet
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")


def _load_prompt(nom_fichier: str) -> str:
    """
    Lit un fichier .txt dans le dossier prompts/ et retourne son contenu.
    Le underscore au début signale que c'est une fonction interne au module.
    """
    chemin = os.path.join(PROMPTS_DIR, nom_fichier)

    # Vérifie que le fichier existe avant de l'ouvrir
    if not os.path.exists(chemin):
        raise FileNotFoundError(f"Fichier prompt introuvable : {chemin}")

    with open(chemin, "r", encoding="utf-8") as f:
        return f.read()


def generate_content(texte: str, format_sortie: str, ton: str = "professionnel") -> str:
    """
    Génère du contenu structuré à partir d'une transcription.

    Args:
        texte         : la transcription nettoyée
        format_sortie : "resume", "article", ou "linkedin"
        ton           : "professionnel", "décontracté", ou "marketing"

    Returns:
        Le contenu généré sous forme de string
    """

    # Mappe chaque format vers son fichier prompt
    fichiers_prompts = {
        "resume":   "summary_prompt.txt",
        "article":  "article_prompt.txt",
        "linkedin": "linkedin_prompt.txt"
    }

    # Vérifie que le format demandé est supporté
    if format_sortie not in fichiers_prompts:
        raise ValueError(
            f"Format '{format_sortie}' non supporté. "
            f"Formats disponibles : {list(fichiers_prompts.keys())}"
        )

    # Charge le prompt depuis le fichier .txt
    # et injecte les variables {texte} et {ton}
    prompt = _load_prompt(fichiers_prompts[format_sortie])
    prompt_final = prompt.format(texte=texte, ton=ton)

    # Appel à l'API OpenAI
    # On sépare le prompt en deux messages :
    # - "user" : contient tout (rôle + règles + transcription)
    # Pourquoi pas "system" ? Pour rester simple et compatible
    # avec tous les modèles OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # modèle plus rapide et moins cher que gpt-4
        messages=[
            {"role": "user", "content": prompt_final}
        ],
        temperature=0.7,  # équilibre entre créativité et cohérence
        max_tokens=2000   # ~1500 mots maximum en sortie
    )

    return response.choices[0].message.content
