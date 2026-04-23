from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database" / "hiddenhire.sqlite"
LEGACY_DATABASES = [
    BASE_DIR / "instance" / "hiddenhire.sqlite",
    Path.home() / "AppData" / "Local" / "HiddenHire" / "hiddenhire.sqlite",
]


class Config:
    SECRET_KEY = "hiddenhire-local-dev"
    DATABASE = DATABASE_PATH
    LEGACY_DATABASES = LEGACY_DATABASES
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_UPLOAD_EXTENSIONS = {".csv"}
    DEFAULT_HIDE_REJECTED_DUPLICATES = True
