import streamlit as st
import sqlite3
import pandas as pd
import os

# Database filename
DB_NAME = 'sqlitedata.db'

def check_database_exists():
    """Check if the database file exists."""
    return os.path.exists(DB_NAME)

def get_all_locations():
    """Fetch all unique locations from the database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        query = "SELECT DISTINCT location FROM daily_forecasts ORDER BY location"
        locations = pd.read_sql_query(query, conn)
        conn.close()
        return locations['location'].tolist()
    except Exception as e:
        st.error(f"Error fetching locations: {e}")
        return []

def get_weather_by_location(location):
    """Fetch weather data for a specific location."""
    try:
        conn = sqlite3.connect(DB_NAME)
        query = """
        SELECT date, weather, max_temp, min_temp, fetch_time
        FROM daily_forecasts
        WHERE location = ?
        ORDER BY date
        """
        df = pd.read_sql_query(query, conn, params=(location,))
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return pd.DataFrame()

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Weather Dashboard",
        page_icon="🌤️",
        layout="wide"
    )
    
    st.title("🌤️ Taiwan Agricultural Weather Forecast Dashboard")
    st.markdown("---")
    
    # Check if database exists
    if not check_database_exists():
        st.error("⚠️ Database not found!")
        st.info("Please run `python crawler.py` first to fetch weather data.")
        return
    
    # Get all locations
    locations = get_all_locations()
    
    if not locations:
        st.warning("📭 No weather data available in the database.")
        st.info("Please run `python crawler.py` to fetch weather data from CWA API.")
        return
    
    # Location selector
    st.sidebar.header("📍 Location Selection")
    selected_location = st.sidebar.selectbox(
        "Choose a location:",
        locations,
        help="Select a location to view weather forecasts"
    )
    
    # Display weather data for selected location
    if selected_location:
        st.header(f"Weather Forecast for {selected_location}")
        
        df = get_weather_by_location(selected_location)
        
        if df.empty:
            st.warning(f"No forecast data available for {selected_location}")
        else:
            # Display data in a nice table format
            st.subheader("📅 Daily Forecasts")
            
            # Rename columns for better display
            display_df = df.copy()
            display_df.columns = ['Date', 'Weather', 'Max Temp (°C)', 'Min Temp (°C)', 'Last Updated']
            
            # Display as table
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Display summary statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="📊 Total Forecast Days",
                    value=len(df)
                )
            
            with col2:
                if not df['max_temp'].isna().all():
                    avg_max = df['max_temp'].astype(float).mean()
                    st.metric(
                        label="🌡️ Avg Max Temp",
                        value=f"{avg_max:.1f}°C"
                    )
            
            with col3:
                if not df['min_temp'].isna().all():
                    avg_min = df['min_temp'].astype(float).mean()
                    st.metric(
                        label="🌡️ Avg Min Temp",
                        value=f"{avg_min:.1f}°C"
                    )
    
    # Footer
    st.markdown("---")
    
    # Add link to interactive map
    st.subheader("🗺️ Interactive Taiwan Weather Map")
    st.markdown("""
    View weather locations on an interactive map with temperature time-series charts!
    """)    
    
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("🌐 Open Interactive Map", "http://localhost:8000/map.html", type="primary")
    with col2:
        st.link_button("📱 Open Standalone Map", "map_standalone.html", type="secondary", help="No server needed - can be opened directly")
    
    st.markdown("---")
    st.caption("Data source: Taiwan Central Weather Administration (CWA) OpenData API")

if __name__ == "__main__":
    main()
