import gspread
from oauth2client.service_account import ServiceAccountCredentials

def test_google_sheets_connection(sheet_name):
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/sirigowrih/Desktop/googlesheets_sql_sync/credentials.json', scope)
        client = gspread.authorize(creds)
        
        sheet = client.open(sheet_name).sheet1
        
        print(f"Successfully connected to Google Sheets. Sheet name: '{sheet.title}'")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_google_sheets_connection('GoogleSheetSync')
