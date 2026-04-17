# utils/file_handler.py

import os
import tempfile
from docx import Document


# Extensions acceptées par l'application
EXTENSIONS_ACCEPTEES = ['.mp4', '.mov', '.avi', '.mkv', '.webm',
                        '.mp3', '.wav', '.m4a', '.ogg', '.flac']


def sauvegarder_upload(fichier_uploade) -> tuple[str, bool]:
    """
    Sauvegarde le fichier uploadé via Streamlit dans un fichier temporaire.

    Streamlit donne accès au fichier via un objet UploadedFile —
    ce n'est pas un vrai fichier sur le disque, juste des bytes en mémoire.
    On doit l'écrire sur le disque pour que ffmpeg et Whisper puissent le lire.

    Args:
        fichier_uploade : objet st.file_uploader de Streamlit

    Returns:
        tuple (chemin_fichier, fichier_temporaire)
    """

    # Récupère l'extension du fichier original
    _, extension = os.path.splitext(fichier_uploade.name)
    extension = extension.lower()

    # Vérifie que le format est supporté
    if extension not in EXTENSIONS_ACCEPTEES:
        raise ValueError(
            f"Format '{extension}' non supporté.\n"
            f"Formats acceptés : {EXTENSIONS_ACCEPTEES}"
        )

    # Crée un fichier temporaire avec la bonne extension
    fichier_temp = tempfile.NamedTemporaryFile(
        suffix=extension,
        delete=False
    )

    # Écrit les bytes du fichier uploadé sur le disque
    fichier_temp.write(fichier_uploade.read())
    fichier_temp.close()

    return fichier_temp.name, True


def exporter_txt(contenu: str, nom_fichier: str = "contenu_genere.txt") -> bytes:
    """
    Convertit le contenu généré en bytes téléchargeables en .txt.
    Streamlit attend des bytes pour st.download_button.
    """
    return contenu.encode("utf-8")


def exporter_md(contenu: str, nom_fichier: str = "contenu_genere.md") -> bytes:
    """
    Convertit le contenu généré en bytes téléchargeables en .md.
    Identique au .txt mais avec l'extension markdown.
    """
    return contenu.encode("utf-8")


def exporter_docx(contenu: str) -> bytes:
    """
    Convertit le contenu généré en fichier Word .docx téléchargeable.

    Returns:
        bytes du fichier .docx prêt à être téléchargé
    """
    doc = Document()

    # Ajoute chaque ligne comme paragraphe séparé
    # On évite \n dans un seul paragraphe car Word ne le gère pas bien
    for ligne in contenu.split('\n'):
        doc.add_paragraph(ligne)

    # Sauvegarde dans un fichier temporaire et lit les bytes
    fichier_temp = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
    chemin_temp = fichier_temp.name
    fichier_temp.close()

    doc.save(chemin_temp)

    with open(chemin_temp, 'rb') as f:
        bytes_docx = f.read()

    # Nettoie le fichier temporaire
    os.remove(chemin_temp)

    return bytes_docx


def nettoyer_fichier_temp(chemin: str) -> None:
    """
    Supprime un fichier temporaire du disque.
    À appeler après que le fichier n'est plus nécessaire.
    """
    if chemin and os.path.exists(chemin):
        os.remove(chemin)