import os
from dotenv import load_dotenv

load_dotenv()

def construct_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 54321 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "abc123")
    user, db_name = "allocation", "allocation"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_postgres_uri():
    return os.getenv("POSTGRES_URI", construct_postgres_uri())


def construct_api_url():
    host = os.getenv("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"


def get_api_url():
    return os.getenv("API_URL", construct_api_url())
