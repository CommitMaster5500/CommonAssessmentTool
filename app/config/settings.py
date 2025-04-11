import os
from dotenv import load_dotenv

# Load environment variables from .env file
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
env_path = os.path.join(base_dir, ".env")
env_example_path = os.path.join(os.path.dirname(__file__), ".env.example")

# Load .env if it exists, otherwise load .env.example
if os.path.exists(env_path):
    load_dotenv(env_path)
    print("Loaded environment variables from .env")
elif os.path.exists(env_example_path):
    load_dotenv(env_example_path)
    print("WARNING: .env not found! Using .env.example instead.")
else:
    print(
        "ERROR: No .env or .env.example file found! Using system environment variables."
    )

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# Admin User
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Case Worker
WORKER_USERNAME = os.getenv("WORKER_USERNAME")
WORKER_EMAIL = os.getenv("WORKER_EMAIL")
WORKER_PASSWORD = os.getenv("WORKER_PASSWORD")

# CSV File Path
DATA_CSV_PATH = os.getenv("DATA_CSV_PATH", "app/ml/data/data_commontool.csv")
