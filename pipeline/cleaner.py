# pipeline/cleaner.py

import re


def clean_transcription(texte: str) -> str:
    texte = _supprimer_timestamps(texte)
    texte = _supprimer_mots_parasites(texte)
    texte = _supprimer_repetitions(texte)
    texte = _normaliser_espaces(texte)
    return texte.strip()


def _supprimer_timestamps(texte: str) -> str:
    texte = re.sub(r'\[\d{2}:\d{2}:\d{2}[\.,]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[\.,]\d{3}\]', '', texte)
    texte = re.sub(r'\(\d{2}:\d{2}:\d{2}\)', '', texte)
    texte = re.sub(r'-->', '', texte)
    return texte


def _supprimer_mots_parasites(texte: str) -> str:
    mots_parasites = [
        # Hésitations orales
        r'\beuh+\b',
        r'\beu+\b',
        r'\bhmm+\b',
        r'\bahh?\b',
        r'\bohh?\b',

        # Remplisseurs — ordre important : expressions longues avant mots courts
        r'\bdonc voilà\b',
        r'\bvoilà voilà\b',
        r'\bvoilà\b',
        r'\bc\'est-à-dire\b',
        r'\ben fait\b',
        r'\ben gros\b',
        r'\bdu coup\b',
        r'\bgenre\b',
        r'\bkind of\b',
        r'\bbah\b',
        r'\bben\b',
        r'\bhein\b',

        # "donc" et "alors" en début ou milieu de phrase
        # mais pas dans "indispensable" etc — \b protège
        r'\bdonc\b',
        r'\balors\b',
        r'\bquoi\b',
        r'\bstyle\b',
    ]

    for mot in mots_parasites:
        texte = re.sub(mot, '', texte, flags=re.IGNORECASE)

    return texte


def _supprimer_repetitions(texte: str) -> str:
    """
    Gère deux cas :
    1. Mots simples répétés : "de de" → "de"
    2. Expressions avec apostrophe répétées : "c'est c'est" → "c'est"
    """
    # Cas 1 : mots simples consécutifs (ex: "on va on va")
    # On répète le pattern jusqu'à ce qu'il n'y ait plus de répétitions
    # car un seul passage ne suffit pas pour "on va on va on va"
    precedent = None
    while precedent != texte:
        precedent = texte
        texte = re.sub(r'\b(\w+)\s+\1\b', r'\1', texte, flags=re.IGNORECASE)

    # Cas 2 : expressions avec apostrophe (ex: "c'est c'est", "j'ai j'ai")
    precedent = None
    while precedent != texte:
        precedent = texte
        texte = re.sub(r"\b(\w+'\w+)\s+\1\b", r'\1', texte, flags=re.IGNORECASE)

    return texte


def _normaliser_espaces(texte: str) -> str:
    # Virgule ou point orphelin en début de segment
    texte = re.sub(r'^\s*[,]\s*', '', texte, flags=re.MULTILINE)

    # Espaces multiples → espace simple
    texte = re.sub(r' {2,}', ' ', texte)

    # Espace en début de ligne
    texte = re.sub(r'^\s+', '', texte, flags=re.MULTILINE)

    # Espaces avant ponctuation
    texte = re.sub(r' ([,\.\!\?])', r'\1', texte)

    # Lignes vides multiples → une seule
    texte = re.sub(r'\n{3,}', '\n\n', texte)

    return texte