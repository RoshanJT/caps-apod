import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
20

load_dotenv()  

API_KEY = os.getenv('NASA_API_KEY')
SAVE_DIR = 'images'

def create_path_for_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    path = os.path.join(SAVE_DIR, str(date_obj.year), f"{date_obj.month:02d}")
    os.makedirs(path, exist_ok=True)
    return os.path.join(path, f"{date_obj.day:02d}.jpg")

def fetch_apod(date):
    url = f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={date}'
    try:
        response = requests.get(url).json()
        if response.get('media_type') == 'image':
            image_url = response['url']
            save_path = create_path_for_date(date)
            img_data = requests.get(image_url).content
            with open(save_path, 'wb') as f:
                f.write(img_data)
            print(f"Downloaded: {save_path}") 
        else:
            print(f"Skipped (not image): {date}")
            
    except Exception as e:
        print(f"Error {e}")
def fetch_range(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    while start <= end:
        fetch_apod(start.strftime('%Y-%m-%d'))
        start += timedelta(days=1)

start = input("Start date (YYYY-MM-DD): ")
end = input("End date (YYYY-MM-DD): ")

try:
    datetime.strptime(start, "%Y-%m-%d")
    datetime.strptime(end, "%Y-%m-%d")
    fetch_range(start, end)
except ValueError:
    print("Dates are invalid.")
