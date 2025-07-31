import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Exam Site Backend"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:a_secret_password@localhost:3307/exam_site_db_dev")

settings = Settings()
