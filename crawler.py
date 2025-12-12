import requests
import json
import os
import urllib3
import sqlite3
from datetime import datetime

# Database filename
DB_NAME = 'sqlitedata.db'

def init_db():
    """Initialize the SQLite database and create tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Table for general weather profile (text description)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_text TEXT,
        fetch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Table for specific daily forecasts by location
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_forecasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT,
        date TEXT,
        weather TEXT,
        max_temp TEXT,
        min_temp TEXT,
        fetch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' initialized.")

def save_to_db(weather_profile, forecast_data):
    """Save parsed data into SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Insert Weather Profile
    if weather_profile:
        cursor.execute('INSERT INTO weather_summary (profile_text) VALUES (?)', (weather_profile,))
    
    # 2. Insert Daily Forecasts
    # forecast_data is a list of dictionaries: 
    # [{'location': 'Taipei', 'date': '2025-12-03', 'weather': 'Rain', 'max_temp': '20', 'min_temp': '18'}, ...]
    if forecast_data:
        cursor.executemany('''
        INSERT INTO daily_forecasts (location, date, weather, max_temp, min_temp)
        VALUES (:location, :date, :weather, :max_temp, :min_temp)
        ''', forecast_data)
        
    conn.commit()
    print(f"Saved {len(forecast_data)} daily forecast records to database.")
    conn.close()

def fetch_cwa_data():
    # Disable SSL warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization=CWA-0A58B91B-0CA1-4F74-8F0D-FF7A81A2B4F1&downloadType=WEB&format=JSON"

    print(f"Fetching data from: {url}")

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        data = response.json()

        # Save raw JSON just in case
        with open('cwa_weather_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        # --- Parse Data for Database ---
        weather_profile_text = None
        db_records = []

        if 'cwaopendata' in data:
            cwa_root = data['cwaopendata']
            
            # Locate agrWeatherForecasts
            if 'resources' in cwa_root:
                resources = cwa_root['resources']
                resource_item = resources.get('resource', {})
                if isinstance(resource_item, list): resource_item = resource_item[0]
                
                data_content = resource_item.get('data', {})
                
                if 'agrWeatherForecasts' in data_content:
                    agr_data = data_content['agrWeatherForecasts']
                    
                    # Get Profile Text
                    weather_profile_text = agr_data.get('weatherProfile', '')
                    print(f"Weather Profile: {weather_profile_text[:50]}...")

                    # Process Locations
                    if 'weatherForecasts' in agr_data and 'location' in agr_data['weatherForecasts']:
                        locations = agr_data['weatherForecasts']['location']
                        
                        for loc in locations:
                            loc_name = loc.get('locationName', 'Unknown')
                            
                            # Extract Elements lists
                            elements = loc.get('weatherElements', {})
                            wx_list = elements.get('Wx', {}).get('daily', [])
                            maxt_list = elements.get('MaxT', {}).get('daily', [])
                            mint_list = elements.get('MinT', {}).get('daily', [])

                            # We iterate through the Wx list and try to match temps by date
                            for i, wx_item in enumerate(wx_list):
                                date = wx_item.get('dataDate')
                                weather_desc = wx_item.get('weather')
                                
                                # Find matching MaxT and MinT by date (safer than index assumption)
                                max_t = next((item['temperature'] for item in maxt_list if item['dataDate'] == date), None)
                                min_t = next((item['temperature'] for item in mint_list if item['dataDate'] == date), None)
                                
                                record = {
                                    'location': loc_name,
                                    'date': date,
                                    'weather': weather_desc,
                                    'max_temp': max_t,
                                    'min_temp': min_t
                                }
                                db_records.append(record)

        # Save to SQLite
        init_db() # Ensure tables exist
        save_to_db(weather_profile_text, db_records)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_cwa_data()