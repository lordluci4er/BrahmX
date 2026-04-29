import os
from dotenv import load_dotenv

# -------- LOAD ENV --------
load_dotenv()


class BaseConfig:
    # -------- BASIC --------
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # -------- JSON --------
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True

    # -------- CORS --------
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

    # -------- APP --------
    DEBUG = False
    TESTING = False

    # -------- MODEL --------
    MODEL_NAME = os.getenv("MODEL_NAME", "sshleifer/distilbart-cnn-12-6")

    # -------- LIMITS --------
    MAX_INPUT_LENGTH = int(os.getenv("MAX_INPUT_LENGTH", 2000))


# -------- DEVELOPMENT CONFIG --------
class DevelopmentConfig(BaseConfig):
    DEBUG = True


# -------- PRODUCTION CONFIG --------
class ProductionConfig(BaseConfig):
    DEBUG = False


# -------- SELECT CONFIG --------
def get_config():
    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        return ProductionConfig
    return DevelopmentConfig