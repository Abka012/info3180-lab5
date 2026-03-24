import os

from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env if it exists.

# Get the application's base directory
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config(object):
    """Base Config Object"""

    DEBUG = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER", os.path.join(BASE_DIR, "app", "uploads")
    )
    DATABASE_URL = os.environ["DATABASE_URL"]
    SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace("postgres://", "postgresql://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # This is just here to suppress a warning from SQLAlchemy as it will soon be removed
