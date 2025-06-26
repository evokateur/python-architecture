import os


def get_postgres_uri():
    host = os.getenv("DB_HOST", "localhost")
    port = 54321 if host == "localhost" else 5432
    password = os.getenv("DB_PASSWORD", "abc123")
    user, db_name = "allocation", "allocation"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.getenv("API_HOST", "localhost")
    port = 50000 if host == "localhost" else 80
    return f"http://{host}:{port}"
