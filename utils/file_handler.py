from pathlib import Path

from docx import Document

OUTPUTS_DIR = Path("outputs")


def _ensure_dir() -> None:
    OUTPUTS_DIR.mkdir(exist_ok=True)


def save_txt(content: str, filename: str) -> Path:
    _ensure_dir()
    path = OUTPUTS_DIR / filename
    path.write_text(content, encoding="utf-8")
    return path


def save_docx(content: str, filename: str) -> Path:
    _ensure_dir()
    doc = Document()
    for line in content.split("\n"):
        doc.add_paragraph(line)
    path = OUTPUTS_DIR / filename
    doc.save(str(path))
    return path


def read_txt(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")
