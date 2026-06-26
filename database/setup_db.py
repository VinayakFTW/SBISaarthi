from .postgres import init_db

if __name__ == "__main__":
    print("Running database initialization...")
    init_db()
    print("Done!")