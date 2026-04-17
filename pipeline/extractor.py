# pipeline/extractor.py

import os
import tempfile
import ffmpeg


# Extensions vidéo supportées
EXTENSIONS_VIDEO = ['.mp4', '.mov', '.avi', '.mkv', '.webm']

# Extensions audio supportées — dans ce cas pas besoin d'extraction
EXTENSIONS_AUDIO = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']


def extraire_audio(chemin_fichier: str) -> tuple[str, bool]:
    """
    Extrait la piste audio d'un fichier vidéo en fichier .wav temporaire.
    Si le fichier est déjà un audio, le retourne directement sans traitement.

    Args:
        chemin_fichier : chemin vers le fichier vidéo ou audio

    Returns:
        tuple (chemin_audio, fichier_temporaire)
        - chemin_audio      : chemin vers le fichier audio à transcrire
        - fichier_temporaire: True si un fichier temp a été créé (à supprimer après)
    """

    if not os.path.exists(chemin_fichier):
        raise FileNotFoundError(f"Fichier introuvable : {chemin_fichier}")

    _, extension = os.path.splitext(chemin_fichier)
    extension = extension.lower()

    # Cas 1 — c'est déjà un fichier audio, rien à faire
    if extension in EXTENSIONS_AUDIO:
        return chemin_fichier, False

    # Cas 2 — c'est une vidéo, on extrait l'audio
    if extension in EXTENSIONS_VIDEO:
        return _extraire_depuis_video(chemin_fichier)

    # Cas 3 — format non supporté
    raise ValueError(
        f"Format '{extension}' non supporté.\n"
        f"Vidéos acceptées : {EXTENSIONS_VIDEO}\n"
        f"Audios acceptés  : {EXTENSIONS_AUDIO}"
    )


def _extraire_depuis_video(chemin_video: str) -> tuple[str, bool]:
    """
    Utilise ffmpeg pour extraire la piste audio d'une vidéo.
    Crée un fichier .wav dans le dossier temporaire du système.

    Returns:
        tuple (chemin_wav_temporaire, True)
    """

    # Crée un fichier temporaire .wav
    # delete=False → on gère la suppression manuellement après la transcription
    fichier_temp = tempfile.NamedTemporaryFile(
        suffix='.wav',
        delete=False
    )
    chemin_wav = fichier_temp.name
    fichier_temp.close()

    try:
        (
            ffmpeg
            .input(chemin_video)          # fichier source
            .output(
                chemin_wav,
                acodec='pcm_s16le',       # codec audio WAV standard
                ac=1,                      # mono (suffisant pour la parole)
                ar='16000'                 # 16kHz — fréquence optimale pour Whisper
            )
            .overwrite_output()            # écrase si le fichier existe déjà
            .run(
                quiet=True,                # pas de logs ffmpeg dans le terminal
                capture_stdout=True,
                capture_stderr=True
            )
        )
    except ffmpeg.Error as e:
        # Nettoie le fichier temp si l'extraction échoue
        if os.path.exists(chemin_wav):
            os.remove(chemin_wav)
        raise RuntimeError(
            f"Erreur ffmpeg lors de l'extraction audio : {e.stderr.decode()}"
        )

    return chemin_wav, True


def nettoyer_fichier_temp(chemin: str) -> None:
    """
    Supprime le fichier temporaire après transcription.
    À appeler après transcribe_audio() si fichier_temporaire == True.
    """
    if os.path.exists(chemin):
        os.remove(chemin)