from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from db import MySheetData  # Assuming your MySheetData class is in the db.py file


engine = create_engine('mysql+mysqlconnector://root:sirigowri2508@localhost/google_sheet_sync')
Session = sessionmaker(bind=engine)
session = Session()


mock_data = [
    {"name": "John Doe", "age": 25},
    {"name": "Jane Smith", "age": 30},
    {"name": "Alice Johnson", "age": 22},
    {"name": "Bob Brown", "age": 28},
    {"name": "Charlie White", "age": 35},
]

for entry in mock_data:
    new_entry = MySheetData(
        name=entry["name"],
        age=entry["age"],
        updated_at=datetime.datetime.utcnow()
    )
    session.add(new_entry)

# Commit the transaction
session.commit()

# Query and print all records to verify
entries = session.query(MySheetData).all()
for entry in entries:
    print(f"ID: {entry.id}, Name: {entry.name}, Age: {entry.age}, Updated At: {entry.updated_at}")

session.close()
