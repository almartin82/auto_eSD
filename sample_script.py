import get_data
import process_data

def fetch_and_unzip():
    get_data.fetch_access_db()
    process_data.unzip()

if __name__ == '__main__':
    fetch_and_unzip()