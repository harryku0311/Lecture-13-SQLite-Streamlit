## ADDED Requirements

### Requirement: Location Selection
The dashboard SHALL provide a dropdown selector that displays all unique locations available in the database.

#### Scenario: Location list display
- **WHEN** the dashboard loads
- **THEN** all unique location names from the `daily_forecasts` table are displayed in a dropdown selector
- **AND** the dropdown is populated with distinct location values

#### Scenario: Empty database handling
- **WHEN** the database has no forecast data
- **THEN** the dashboard displays a message indicating no data is available
- **AND** no errors are raised

### Requirement: Temperature Data Display
The dashboard SHALL display weather forecast information for the selected location, including date, weather description, maximum temperature, and minimum temperature.

#### Scenario: Display forecast for selected location
- **WHEN** a user selects a location from the dropdown
- **THEN** the dashboard retrieves all forecast records for that location
- **AND** displays the date, weather description, max temperature, and min temperature for each forecast day
- **AND** data is presented in a readable format (table or structured layout)

#### Scenario: Multiple days forecast
- **WHEN** multiple forecast days exist for a location
- **THEN** all forecast days are displayed in chronological order
- **AND** each day shows complete temperature information

### Requirement: Database Connectivity
The dashboard SHALL connect to the existing SQLite database (`sqlitedata.db`) in read-only mode to retrieve weather data.

#### Scenario: Successful database connection
- **WHEN** the dashboard starts
- **THEN** it successfully connects to `sqlitedata.db`
- **AND** can query the `daily_forecasts` table

#### Scenario: Database file missing
- **WHEN** the database file does not exist
- **THEN** the dashboard displays an error message
- **AND** provides instructions to run the crawler first

### Requirement: Web Interface Launch
The dashboard SHALL be launchable via the Streamlit CLI command and accessible through a web browser.

#### Scenario: Launch dashboard
- **WHEN** user runs `streamlit run dashboard.py`
- **THEN** the Streamlit server starts successfully
- **AND** the dashboard is accessible at the provided local URL (typically http://localhost:8501)
- **AND** the page title and header are displayed correctly
