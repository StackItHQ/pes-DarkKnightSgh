import sys
import os
import time  # Import time module
import datetime  # Import datetime module
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

# Add paths for modules
sys.path.append(os.path.abspath('/Users/sirigowrih/Desktop/googlesheets_sql_sync/google_sheet'))
sys.path.append(os.path.abspath('/Users/sirigowrih/Desktop/googlesheets_sql_sync/db'))

# Database setup
Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://root:sirigowri2508@localhost/google_sheet_sync')
Session = sessionmaker(bind=engine)

class SheetData(Base):
    __tablename__ = 'sheet_data'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# Function to get Google Sheets service
def get_google_sheets_service():
    creds = None
    if os.path.exists('/Users/sirigowrih/Desktop/googlesheets_sql_sync/credentials.json'):
        creds = service_account.Credentials.from_service_account_file(
            '/Users/sirigowrih/Desktop/googlesheets_sql_sync/credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
    return build('sheets', 'v4', credentials=creds)

# Function to get Google Sheet
def get_google_sheet(sheet_name):
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    # Replace with your actual spreadsheet ID
    spreadsheet_id = '13OnX2PYBgvNtmMfCUTTJolCVaPNvcpEXdpUDBUz0bkw'
    # Correct range reference (Sheet1 within GoogleSheetSync file)
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=f'Sheet1!A1:C').execute()
    return result.get('values', [])

def fetch_google_sheet_data(sheet_name):
    try:
        records = get_google_sheet(sheet_name)
        print(f"Fetched {len(records)} records from Google Sheets")
        return records
    except HttpError as e:
        print(f"Error fetching Google Sheets data: {e}")
        return []

def fetch_mysql_data(session):
    try:
        records = session.query(SheetData).all()
        print(f"Fetched {len(records)} records from MySQL")
        return records
    except SQLAlchemyError as e:
        print(f"Error fetching MySQL data: {e}")
        return []

def update_google_sheet(sheet_name, db_data):
    try:
        service = get_google_sheets_service()
        sheet = service.spreadsheets()
        data = [["ID", "Name", "Age", "Updated At"]]  # Headers
        for entry in db_data:
            data.append([entry.id, entry.name, entry.age, entry.updated_at.isoformat()])
        body = {'values': data}
        result = sheet.values().update(
            spreadsheetId='13OnX2PYBgvNtmMfCUTTJolCVaPNvcpEXdpUDBUz0bkw', range=f'Sheet1!A1',
            valueInputOption='USER_ENTERED', body=body).execute()
        print(f"Updated Google Sheets with {len(db_data)} records")
    except HttpError as e:
        print(f"Error updating Google Sheets: {e}")

def update_mysql_db(session, google_data):
    try:
        google_dict = {int(record[0]): record for record in google_data[1:] if record[0]}  # Skip header
        db_records = session.query(SheetData).all()
        
        for db_record in db_records:
            if db_record.id in google_dict:
                google_record = google_dict[db_record.id]
                google_updated_at = datetime.datetime.fromisoformat(google_record[3])
                
                if google_updated_at > db_record.updated_at:
                    db_record.name = google_record[1]
                    db_record.age = int(google_record[2])
                    db_record.updated_at = google_updated_at
                del google_dict[db_record.id]
            else:
                session.delete(db_record)
        
        for new_record in google_dict.values():
            new_entry = SheetData(
                id=int(new_record[0]),
                name=new_record[1],
                age=int(new_record[2]),
                updated_at=datetime.datetime.fromisoformat(new_record[3])
            )
            session.add(new_entry)
        
        session.commit()
        print("MySQL Database updated successfully")
    except SQLAlchemyError as e:
        print(f"Error updating MySQL: {e}")
        session.rollback()

def sync_data(sheet_name):
    session = Session()
    
    google_data = fetch_google_sheet_data('Sheet1')  # Reference Sheet1
    update_mysql_db(session, google_data)
    
    db_data = fetch_mysql_data(session)
    update_google_sheet('Sheet1', db_data)  # Reference Sheet1
    
    session.close()

def run_sync(sheet_name, interval=10):
    while True:
        try:
            print(f"\nStarting sync at {datetime.datetime.now()}")
            sync_data(sheet_name)
            print(f"Sync completed. Waiting {interval} seconds for next sync...")
            time.sleep(interval)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Retrying in 60 seconds...")
            time.sleep(60)

if __name__ == "__main__":
    sheet_name = "GoogleSheetSync"  # Make sure this matches your actual sheet name
    sync_interval = 10  # seconds
    print(f"Starting automated sync for sheet '{sheet_name}' every {sync_interval} seconds")
    run_sync(sheet_name, interval=sync_interval)
