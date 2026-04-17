# utils/session_state.py

import streamlit as st


def initialiser_session():
    """
    Initialise toutes les variables de session au démarrage de l'application.
    À appeler une seule fois au début de app.py.

    st.session_state fonctionne comme un dictionnaire persistant —
    les valeurs survivent entre les re-exécutions du script Streamlit.
    """

    # Fichier uploadé par l'utilisateur
    if 'fichier_uploade' not in st.session_state:
        st.session_state.fichier_uploade = None

    # Chemin du fichier temporaire sur le disque
    if 'chemin_fichier_temp' not in st.session_state:
        st.session_state.chemin_fichier_temp = None

    # Transcription brute retournée par Whisper
    if 'transcription_brute' not in st.session_state:
        st.session_state.transcription_brute = None

    # Transcription nettoyée par cleaner.py
    if 'transcription_nettoyee' not in st.session_state:
        st.session_state.transcription_nettoyee = None

    # Contenu généré par GPT-4o
    if 'contenu_genere' not in st.session_state:
        st.session_state.contenu_genere = None

    # Format de sortie choisi par l'utilisateur
    if 'format_sortie' not in st.session_state:
        st.session_state.format_sortie = "resume"

    # Ton choisi par l'utilisateur
    if 'ton' not in st.session_state:
        st.session_state.ton = "professionnel"

    # Etat du pipeline — pour afficher les messages de progression
    if 'etape_en_cours' not in st.session_state:
        st.session_state.etape_en_cours = None

    # Message d'erreur éventuel
    if 'erreur' not in st.session_state:
        st.session_state.erreur = None


def reinitialiser_resultats():
    """
    Remet à zéro uniquement les résultats du pipeline.
    À appeler quand l'utilisateur uploade un nouveau fichier —
    on garde ses préférences (format, ton) mais on efface les résultats précédents.
    """
    st.session_state.transcription_brute = None
    st.session_state.transcription_nettoyee = None
    st.session_state.contenu_genere = None
    st.session_state.etape_en_cours = None
    st.session_state.erreur = None


def reinitialiser_tout():
    """
    Remet tout à zéro — comme si l'application venait de démarrer.
    À appeler sur le bouton "Recommencer".
    """
    for cle in list(st.session_state.keys()):
        del st.session_state[cle]
    initialiser_session()