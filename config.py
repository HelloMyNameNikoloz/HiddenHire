from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = "hiddenhire-local-dev"
    DATABASE = BASE_DIR / "instance" / "hiddenhire.sqlite"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_UPLOAD_EXTENSIONS = {".csv"}
    DEFAULT_HIDE_REJECTED_DUPLICATES = True
