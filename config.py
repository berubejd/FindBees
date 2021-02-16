import os
from datetime import timedelta


class Config:
    """Set Flask configuration vars."""

    # General Config
    FLASK_APP = os.environ.get("FLASK_APP") or "application"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_key"

    ENV = os.environ.get("FLASK_ENV") or "development"
    if ENV == "development":
        DEBUG = True

    if os.environ.get("SESSION_LIFETIME"):
        PERMANENT_SESSION_LIFETIME = timedelta(
            minutes=int(os.environ.get("SESSION_LIFETIME"))
        )
