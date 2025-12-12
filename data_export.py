import sqlite3
import json
from datetime import datetime

# Database filename
DB_NAME = 'sqlitedata.db'

# Approximate coordinates for Taiwan regions
# Based on major cities/centers in each region
LOCATION_COORDS = {
    "北部地區": {"lat": 25.0330, "lon": 121.5654, "city": "Taipei"},      # Taipei area
    "中部地區": {"lat": 24.1477, "lon": 120.6736, "city": "Taichung"},    # Taichung area
    "南部地區": {"lat": 22.9908, "lon": 120.2133, "city": "Tainan"},      # Tainan area
    "東部地區": {"lat": 23.9871, "lon": 121.6015, "city": "Hualien"},     # Hualien area
    "東北部地區": {"lat": 24.7736, "lon": 121.7580, "city": "Yilan"},     # Yilan area
    "東南部地區": {"lat": 22.7583, "lon": 121.1444, "city": "Taitung"}    # Taitung area
}

def export_weather_data():
    """Export weather data from SQLite to JSON format for web consumption."""
    print("Connecting to database...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get all locations
    cursor.execute('SELECT DISTINCT location FROM daily_forecasts ORDER BY location')
    locations = [row[0] for row in cursor.fetchall()]
    
    print(f"Found {len(locations)} locations")
    
    # Build data structure
    data = {
        "generated_at": datetime.now().isoformat(),
        "locations": []
    }
    
    for location in locations:
        print(f"Processing: {location}")
        
        # Get coordinates for this location
        coords = LOCATION_COORDS.get(location, {"lat": 23.5, "lon": 121.0, "city": "Unknown"})
        
        # Get weather data for this location
        cursor.execute('''
            SELECT date, weather, max_temp, min_temp, fetch_time
            FROM daily_forecasts
            WHERE location = ?
            ORDER BY date
        ''', (location,))
        
        forecasts = []
        for row in cursor.fetchall():
            forecasts.append({
                "date": row[0],
                "weather": row[1],
                "max_temp": float(row[2]) if row[2] else None,
                "min_temp": float(row[3]) if row[3] else None,
                "fetch_time": row[4]
            })
        
        # Calculate average temperature for color coding
        temps = [f["max_temp"] for f in forecasts if f["max_temp"] is not None]
        avg_temp = sum(temps) / len(temps) if temps else 20.0
        
        location_data = {
            "name": location,
            "city": coords["city"],
            "lat": coords["lat"],
            "lon": coords["lon"],
            "avg_temp": round(avg_temp, 1),
            "forecast_count": len(forecasts),
            "forecasts": forecasts
        }
        
        data["locations"].append(location_data)
    
    conn.close()
    
    # Write to JSON file
    output_file = 'weather_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Data exported successfully to {output_file}")
    print(f"  Total locations: {len(data['locations'])}")
    print(f"  Generated at: {data['generated_at']}")
    
    # Create standalone HTML with embedded data
    create_standalone_html(data)

def create_standalone_html(data):
    """Create self-contained HTML file with embedded JSON data."""
    print("\nCreating standalone HTML file...")
    
    # Read the original map.html
    with open('map.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Embed the JSON data as a JavaScript variable
    json_data = json.dumps(data, ensure_ascii=False, indent=2)
    embedded_script = f"""<script>
    // Embedded weather data - no external fetch needed
    const EMBEDDED_WEATHER_DATA = {json_data};
    </script>"""
    
    # Insert the embedded data before the map.js script
    html_content = html_content.replace(
        '<script src="map.js"></script>',
        f'{embedded_script}\n    <script src="map_standalone.js"></script>'
    )
    
    # Write standalone HTML
    with open('map_standalone.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Create modified JavaScript for standalone version
    with open('map.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Replace the fetch call with direct data usage
    js_modified = js_content.replace(
        """async function loadWeatherData() {
    try {
        const response = await fetch('weather_data.json');
        
        if (!response.ok) {
            throw new Error('Failed to load weather data');
        }
        
        weatherData = await response.json();""",
        """async function loadWeatherData() {
    try {
        // Use embedded data instead of fetching
        weatherData = EMBEDDED_WEATHER_DATA;"""
    )
    
    with open('map_standalone.js', 'w', encoding='utf-8') as f:
        f.write(js_modified)
    
    print("✓ Created map_standalone.html (can be opened directly in browser)")
    print("✓ Created map_standalone.js")
    print("\nUsage:")
    print("  - Double-click map_standalone.html to open in browser")
    print("  - No server needed!")

if __name__ == "__main__":
    export_weather_data()
