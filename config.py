# config.py

class Config:
    # URL-encoded password: Ninja@123 → Ninja%40123
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:Ninja%40123@localhost:5432/postgres"
        "?connect_timeout=10&sslmode=prefer"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MODEL_PATH = "./saved_model_gpt"  # Adjust the path as needed
