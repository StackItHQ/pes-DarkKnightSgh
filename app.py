from flask import Flask, jsonify, request
from db.db import session, MySheetData
from google_sheet.google_sheet import get_google_sheet
import datetime

app = Flask(__name__)

@app.route("/sync", methods=["GET"])
def sync_data():
    try:
        # Fetch Google Sheets data
        sheet = get_google_sheet("GoogleSheetSync")
        google_data = sheet.get_all_records()
        
        # Fetch MySQL data
        mysql_data = session.query(MySheetData).all()
        
        # Debug info
        print(f"Google Sheets data: {google_data}")
        print(f"MySQL data before sync: {[{'name': e.name, 'age': e.age, 'updated_at': e.updated_at} for e in mysql_data]}")
        
        # Perform synchronization logic (MySQL -> Sheets and Sheets -> MySQL)
        sync_google_to_mysql(google_data)
        sync_mysql_to_google(mysql_data, sheet)
        
        return jsonify({"message": "Sync completed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def sync_google_to_mysql(google_data):
    existing_entries = { (entry.name, entry.age): entry for entry in session.query(MySheetData).all() }
    google_data_set = set((record.get('Name'), record.get('Age')) for record in google_data)

    print(f"Existing entries in MySQL: {existing_entries}")
    print(f"Google data set: {google_data_set}")

    # Update existing records and add new ones
    for record in google_data:
        name = record.get('Name')
        age = record.get('Age')
        if not name or age is None:
            continue

        if (name, age) in existing_entries:
            # Update existing record
            entry = existing_entries[(name, age)]
            entry.updated_at = datetime.datetime.utcnow()
            print(f"Updated record: {entry}")
        else:
            # Add new record
            new_entry = MySheetData(name=name, age=age, updated_at=datetime.datetime.utcnow())
            session.add(new_entry)
            print(f"Added new record: {new_entry}")

    # Handle records in MySQL that are not in Google Sheets
    to_delete = [entry for (name, age), entry in existing_entries.items() if (name, age) not in google_data_set]
    for entry in to_delete:
        session.delete(entry)
        print(f"Deleted record: {entry}")
    
    session.commit()

def sync_mysql_to_google(mysql_data, sheet):
    existing_data = sheet.get_all_records()
    existing_entries = { (row['Name'], row['Age']): i for i, row in enumerate(existing_data) }

    print(f"Existing sheet data: {existing_data}")
    print(f"MySQL data: {mysql_data}")

    rows_to_add = []
    rows_to_update = []
    rows_to_delete = set(existing_entries.keys())  # Start with all existing sheet entries

    for entry in mysql_data:
        row = [entry.name, entry.age, str(entry.updated_at)]
        if (entry.name, entry.age) in existing_entries:
            existing_row_index = existing_entries[(entry.name, entry.age)]
            rows_to_update.append((existing_row_index + 2, row))
            rows_to_delete.discard((entry.name, entry.age))
            print(f"Update row index {existing_row_index + 2} with data: {row}")
        else:
            rows_to_add.append(row)
            print(f"Queueing row for addition: {row}")
    
    # Delete rows that are no longer in MySQL
    for (name, age) in rows_to_delete:
        row_index = existing_entries[(name, age)] + 2
        sheet.delete_row(row_index)
        print(f"Deleted row index {row_index}")

    # Update existing rows
    for row_index, row in rows_to_update:
        sheet.update(f"A{row_index}:C{row_index}", [row])
    
    # Append new rows
    if rows_to_add:
        sheet.append_rows(rows_to_add)
        print(f"Added rows: {rows_to_add}")

@app.route("/add", methods=["POST"])
def add_record():
    data = request.json
    new_entry = MySheetData(name=data["name"], age=data["age"], updated_at=datetime.datetime.utcnow())
    session.add(new_entry)
    session.commit()
    print(f"Record added: {new_entry}")
    return jsonify({"message": "Record added successfully"}), 201

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_record(id):
    entry = session.query(MySheetData).filter_by(id=id).first()
    if entry:
        session.delete(entry)
        session.commit()
        print(f"Record deleted: {entry}")
        return jsonify({"message": "Record deleted successfully"}), 200
    return jsonify({"error": "Record not found"}), 404

@app.route("/data", methods=["GET"])
def get_data():
    records = session.query(MySheetData).all()
    data = [{"id": record.id, "name": record.name, "age": record.age, "updated_at": record.updated_at} for record in records]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=8082)
