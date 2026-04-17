# app.py

import streamlit as st
from utils.session_state import initialiser_session, reinitialiser_resultats, reinitialiser_tout
from utils.file_handler import sauvegarder_upload, exporter_txt, exporter_md, exporter_docx, nettoyer_fichier_temp
from pipeline.extractor import extraire_audio
from pipeline.transcriber import transcribe_audio
from pipeline.cleaner import clean_transcription
from pipeline.generator import generate_content


# ---------- CONFIGURATION PAGE ----------
st.set_page_config(
    page_title="Générateur de contenu",
    page_icon="🎙️",
    layout="wide"
)

# Initialise le session state au démarrage
initialiser_session()


# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("Paramètres")
    st.divider()

    # Format de sortie
    st.subheader("Format de contenu")
    format_sortie = st.radio(
        label="Choisir le format",
        options=["resume", "article", "linkedin"],
        format_func=lambda x: {
            "resume": "Résumé",
            "article": "Article de blog",
            "linkedin": "Post LinkedIn"
        }[x],
        index=["resume", "article", "linkedin"].index(
            st.session_state.format_sortie
        )
    )
    st.session_state.format_sortie = format_sortie

    st.divider()

    # Ton
    st.subheader("Ton de la rédaction")
    ton = st.selectbox(
        label="Choisir le ton",
        options=["professionnel", "décontracté", "marketing"],
        index=["professionnel", "décontracté", "marketing"].index(
            st.session_state.ton
        )
    )
    st.session_state.ton = ton

    st.divider()

    # Bouton recommencer
    if st.button("Recommencer", use_container_width=True):
        reinitialiser_tout()
        st.rerun()


# ---------- TITRE PRINCIPAL ----------
st.title("Générateur de contenu")
st.caption("Transforme un audio ou une vidéo en contenu structuré prêt à publier.")
st.divider()


# ---------- UPLOAD ----------
st.subheader("1. Uploade ton fichier")

fichier = st.file_uploader(
    label="Fichier audio ou vidéo",
    type=["mp4", "mov", "avi", "mkv", "webm", "mp3", "wav", "m4a", "ogg", "flac"],
    help="Formats supportés : MP4, MOV, AVI, MKV, WEBM, MP3, WAV, M4A, OGG, FLAC"
)

# Quand un nouveau fichier est uploadé
if fichier and fichier != st.session_state.fichier_uploade:
    st.session_state.fichier_uploade = fichier
    reinitialiser_resultats()


# ---------- BOUTON GENERER ----------
st.subheader("2. Lance la génération")

bouton_generer = st.button(
    label="Générer le contenu",
    type="primary",
    disabled=st.session_state.fichier_uploade is None,
    use_container_width=True
)

if bouton_generer:
    chemin_audio_temp = None
    chemin_fichier_temp = None

    try:
        # ETAPE 1 — Sauvegarde du fichier uploadé
        with st.status("Traitement en cours...", expanded=True) as status:

            st.write("Sauvegarde du fichier...")
            chemin_fichier_temp, _ = sauvegarder_upload(
                st.session_state.fichier_uploade
            )

            # ETAPE 2 — Extraction audio si vidéo
            st.write("Extraction de l'audio...")
            chemin_audio, est_temporaire = extraire_audio(chemin_fichier_temp)
            if est_temporaire:
                chemin_audio_temp = chemin_audio

            # ETAPE 3 — Transcription Whisper
            st.write("Transcription en cours (peut prendre quelques secondes)...")
            transcription_brute = transcribe_audio(chemin_audio)
            st.session_state.transcription_brute = transcription_brute

            # ETAPE 4 — Nettoyage
            st.write("Nettoyage de la transcription...")
            transcription_nettoyee = clean_transcription(transcription_brute)
            st.session_state.transcription_nettoyee = transcription_nettoyee

            # ETAPE 5 — Génération GPT
            st.write("Génération du contenu avec GPT-4o...")
            contenu = generate_content(
                texte=transcription_nettoyee,
                format_sortie=st.session_state.format_sortie,
                ton=st.session_state.ton
            )
            st.session_state.contenu_genere = contenu

            status.update(label="Contenu généré avec succès !", state="complete")

    except Exception as e:
        st.error(f"Erreur : {str(e)}")
        st.session_state.erreur = str(e)

    finally:
        # Nettoyage des fichiers temporaires dans tous les cas
        if chemin_fichier_temp:
            nettoyer_fichier_temp(chemin_fichier_temp)
        if chemin_audio_temp:
            nettoyer_fichier_temp(chemin_audio_temp)


# ---------- AFFICHAGE RESULTATS ----------
if st.session_state.contenu_genere:
    st.divider()
    st.subheader("3. Résultat")

    # Affiche la transcription dans un expander (masquée par défaut)
    with st.expander("Voir la transcription brute"):
        st.text(st.session_state.transcription_brute)

    # Affiche le contenu généré
    st.markdown(st.session_state.contenu_genere)

    # ---------- EXPORT ----------
    st.divider()
    st.subheader("4. Télécharger le contenu")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="Télécharger en .txt",
            data=exporter_txt(st.session_state.contenu_genere),
            file_name="contenu_genere.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        st.download_button(
            label="Télécharger en .md",
            data=exporter_md(st.session_state.contenu_genere),
            file_name="contenu_genere.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col3:
        st.download_button(
            label="Télécharger en .docx",
            data=exporter_docx(st.session_state.contenu_genere),
            file_name="contenu_genere.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )