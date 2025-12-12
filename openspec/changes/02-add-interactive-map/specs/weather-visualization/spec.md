## MODIFIED Requirements

### Requirement: Location Selection
The dashboard SHALL provide multiple methods for selecting locations, including a dropdown selector and an interactive map.

#### Scenario: Location list display
- **WHEN** the dashboard loads
- **THEN** all unique location names from the `daily_forecasts` table are displayed in a dropdown selector
- **AND** the dropdown is populated with distinct location values

#### Scenario: Map-based selection
- **WHEN** the dashboard loads
- **THEN** an interactive Taiwan map is displayed with clickable location markers
- **AND** clicking a marker selects that location

#### Scenario: Empty database handling
- **WHEN** the database has no forecast data
- **THEN** the dashboard displays a message indicating no data is available
- **AND** no errors are raised

### Requirement: Temperature Data Display
The dashboard SHALL display weather forecast information through both tabular data and interactive time-series charts.

#### Scenario: Display forecast table
- **WHEN** a user selects a location
- **THEN** the dashboard displays the date, weather description, max temperature, and min temperature in a table format

#### Scenario: Display temperature chart
- **WHEN** a user selects a location
- **THEN** an interactive line chart shows maximum and minimum temperature trends over time
- **AND** the chart is clearly labeled with axes, legend, and units

#### Scenario: Multiple days forecast
- **WHEN** multiple forecast days exist for a location
- **THEN** all forecast days are displayed in both the table and the chart
- **AND** data is presented in chronological order
