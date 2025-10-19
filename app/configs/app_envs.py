from dotenv import load_dotenv
import os

load_dotenv()


class Env:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")  # example


env = Env()

if __name__ == "__main__":
    print(f"Starting app with DATABASE_URL={env.DATABASE_URL}")
