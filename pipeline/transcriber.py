# pipeline/transcriber.py

import whisper
import os


# Charge le modèle une seule fois au démarrage du module
# Comme le client OpenAI dans generator.py — on ne recharge pas
# à chaque appel car le modèle pèse plusieurs centaines de MB
MODEL = whisper.load_model("base")


def transcribe_audio(chemin_audio: str) -> str:
    """
    Transcrit un fichier audio en texte brut via Whisper.

    Args:
        chemin_audio : chemin vers le fichier audio (.wav, .mp3, .m4a)

    Returns:
        Le texte transcrit sous forme de string
    """

    # Vérifie que le fichier existe
    if not os.path.exists(chemin_audio):
        raise FileNotFoundError(f"Fichier audio introuvable : {chemin_audio}")

    # Vérifie l'extension du fichier
    extensions_supportees = ['.wav', '.mp3', '.m4a', '.ogg', '.flac']
    _, extension = os.path.splitext(chemin_audio)
    if extension.lower() not in extensions_supportees:
        raise ValueError(
            f"Format '{extension}' non supporté. "
            f"Formats acceptés : {extensions_supportees}"
        )

    # Transcription — Whisper détecte automatiquement la langue
    # fp16=False → désactive la précision 16 bits
    # nécessaire sur CPU Windows, sinon Whisper affiche un warning
    resultat = MODEL.transcribe(chemin_audio, fp16=False)

    # resultat est un dictionnaire avec plusieurs clés :
    # - resultat["text"]     → le texte complet
    # - resultat["segments"] → liste de segments avec timestamps
    # - resultat["language"] → langue détectée
    # On retourne uniquement le texte complet
    return resultat["text"]