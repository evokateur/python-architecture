import os
from dotenv import load_dotenv

load_dotenv()


def construct_postgres_uri():
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", 54321 if host == "localhost" else 5432))
    password = os.getenv("DB_PASSWORD", "abc123")
    user = os.getenv("DB_USER", "allocation")
    db_name = os.getenv("DB_NAME", "allocation")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_postgres_uri():
    return os.getenv("POSTGRES_URI", construct_postgres_uri())


def construct_api_url():
    host = os.getenv("API_HOST", "localhost")
    port = int(os.getenv("API_PORT", 5005 if host == "localhost" else 80))
    return f"http://{host}:{port}"


def get_api_url():
    return os.getenv("API_URL", construct_api_url())
