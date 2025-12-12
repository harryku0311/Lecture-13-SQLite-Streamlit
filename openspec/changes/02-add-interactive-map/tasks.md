## 1. Data Export Setup

### 1.1 Create Data Export Script
- [x] 1.1.1 Create `data_export.py` to export weather data to JSON
- [x] 1.1.2 Query all locations and their weather data from database
- [x] 1.1.3 Structure data with location coordinates and temperature info
- [x] 1.1.4 Export to `weather_data.json` file
- [x] 1.1.5 Test data export works correctly

## 2. Create HTML Structure

### 2.1 Build Base HTML Page
- [x] 2.1.1 Create `map.html` file
- [x] 2.1.2 Add HTML5 boilerplate structure
- [x] 2.1.3 Include Tailwind CSS via CDN
- [x] 2.1.4 Include Leaflet.js CSS and JavaScript
- [x] 2.1.5 Include Chart.js for time-series charts
- [x] 2.1.6 Create layout: header, map container, chart container

### 2.2 Style with Tailwind CSS
- [x] 2.2.1 Style page header and title
- [x] 2.2.2 Create responsive grid layout for map and chart
- [x] 2.2.3 Style map container with appropriate dimensions
- [x] 2.2.4 Style chart container and controls
- [x] 2.2.5 Add loading states and animations

## 3. Implement JavaScript Map Logic

### 3.1 Initialize Leaflet Map
- [x] 3.1.1 Create `map.js` file
- [x] 3.1.2 Initialize Leaflet map centered on Taiwan (23.5°N, 121°E)
- [x] 3.1.3 Set appropriate zoom level and tile layer
- [x] 3.1.4 Add OpenStreetMap or similar tile provider

### 3.2 Load and Display Data
- [x] 3.2.1 Fetch `weather_data.json` using JavaScript fetch API
- [x] 3.2.2 Parse location data with coordinates
- [x] 3.2.3 Create map markers for each location
- [x] 3.2.4 Add temperature info to marker popups/tooltips
- [x] 3.2.5 Style markers based on temperature (color coding)

### 3.3 Implement Interactivity
- [x] 3.3.1 Add click event listeners to markers
- [x] 3.3.2 Display location name and current temperature on click
- [x] 3.3.3 Load temperature time-series data for clicked location
- [x] 3.3.4 Highlight selected marker

## 4. Implement Temperature Charts

### 4.1 Create Chart.js Visualization
- [x] 4.1.1 Initialize Chart.js line chart
- [x] 4.1.2 Configure x-axis for dates
- [x] 4.1.3 Configure y-axis for temperature (°C)
- [x] 4.1.4 Add two datasets: max temp and min temp
- [x] 4.1.5 Style chart with labels, legend, and tooltips

### 4.2 Connect Chart to Map Selection
- [x] 4.2.1 Update chart when location marker is clicked
- [x] 4.2.2 Animate chart transitions
- [x] 4.2.3 Handle empty data gracefully

## 5. Testing and Refinement
- [x] 5.1 Test page loads correctly in browser
- [x] 5.2 Verify map displays Taiwan with all location markers
- [x] 5.3 Test clicking markers shows temperature info
- [x] 5.4 Verify time-series chart displays correctly
- [ ] 5.5 Test responsive design on different screen sizes
- [ ] 5.6 Add link from Streamlit dashboard to standalone map page (optional)
