import sys
import os


sys.path.append(os.path.abspath('/Users/sirigowrih/Desktop/googlesheets_sql_sync/google_sheet'))
sys.path.append(os.path.abspath('/Users/sirigowrih/Desktop/googlesheets_sql_sync/db'))


from google_sheet import get_google_sheet
from db import session, MySheetData
import datetime


def fetch_google_sheet_data(sheet_name):
    sheet = get_google_sheet(sheet_name)
    records = sheet.get_all_records()  
    return records


def fetch_mysql_data():
    records = session.query(MySheetData).all()
    return records


def update_google_sheet(sheet_name, db_data):
    sheet = get_google_sheet(sheet_name)

    sheet.clear()  

    sheet.append_row(["Name", "Age", "Updated At"])  
    
    for entry in db_data:
        sheet.append_row([entry.name, entry.age, str(entry.updated_at)]) 

    print("Google Sheets updated with MySQL data.")


def update_mysql_db(google_data):
    for record in google_data:
       
        existing_entry = session.query(MySheetData).filter_by(name=record['name'], age=record['age']).first()
        
       
        if not existing_entry:
            new_entry = MySheetData(
                name=record['name'],
                age=record['age'],
                updated_at=datetime.datetime.utcnow()
            )
            session.add(new_entry)
    
    session.commit()
    print("MySQL Database updated with Google Sheets data.")


def sync_data(sheet_name):
    google_data = fetch_google_sheet_data(sheet_name)
    db_data = fetch_mysql_data()
    update_google_sheet(sheet_name, db_data)  
    update_mysql_db(google_data)  

if __name__ == "__main__":
    sync_data("GoogleSheetSync")  
