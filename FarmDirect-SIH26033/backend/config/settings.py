import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from root directory if it exists
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class Config:
    """Base Configuration Class"""

    PROJECT_NAME = "FarmDirect"
    PROBLEM_STATEMENT_ID = "SIH26033"
    TEAM = "Shadow Stack"
    SECRET_KEY = os.getenv("SECRET_KEY", "farmdirect_dev_secret_key_change_in_production_sih2026")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "farmdirect_jwt_secret_key_change_in_production_sih2026")

    # Database Configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "farmdirect_db")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    # Default MySQL database URL using PyMySQL driver
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS origins setting
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")


class DevelopmentConfig(Config):
    """Development Environment Config"""

    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing Environment Config"""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    """Production Environment Config"""

    DEBUG = False
    TESTING = False


def get_config():
    env = os.getenv("FLASK_ENV", "development").lower()
    if env == "production":
        return ProductionConfig
    elif env == "testing":
        return TestingConfig
    return DevelopmentConfig
