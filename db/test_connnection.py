import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

DATABASE_URL = 'mysql+mysqlconnector://root:sirigowri2508@localhost/google_sheet_sync'

def test_connection():
    try:
        engine = create_engine(DATABASE_URL)

        with engine.connect() as connection:
            print("Connection to the database was successful!")

    except OperationalError as e:
        print(f"Error: Unable to connect to the database. {e}")

if __name__ == "__main__":
    test_connection()
