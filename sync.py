import time
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_sync(interval=30):
    while True:
        try:
            response = requests.get("http://127.0.0.1:8083/sync")
            if response.status_code == 200:
                logging.info("Sync response: %s", response.json())
            else:
                logging.error("Sync failed with status code %d: %s", response.status_code, response.text)
        except requests.RequestException as e:
            logging.error("Error during sync: %s", e)
        
        time.sleep(interval)

if __name__ == "__main__":
    run_sync()
