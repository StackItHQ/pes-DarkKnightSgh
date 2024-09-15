import time
import requests

def run_sync(interval=5):
    while True:
        try:
            response = requests.get("http://127.0.0.1:8082/sync")
            print(response.json())
        except Exception as e:
            print(f"Error during sync: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    run_sync()
