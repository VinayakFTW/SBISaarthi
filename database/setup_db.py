from database.postgres import init_db
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    print("Running database initialization...")
    init_db()
    print("Done!")