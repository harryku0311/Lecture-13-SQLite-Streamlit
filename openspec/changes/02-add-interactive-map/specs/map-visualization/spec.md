## ADDED Requirements

### Requirement: Interactive Taiwan Map
The dashboard SHALL display an interactive map of Taiwan showing all weather forecast locations as clickable markers.

#### Scenario: Map initialization
- **WHEN** the dashboard loads
- **THEN** a map of Taiwan is displayed centered on Taiwan's geographical coordinates
- **AND** the map shows the entire island at an appropriate zoom level

#### Scenario: Location markers display
- **WHEN** the map is rendered
- **THEN** markers are placed at each location with available weather data
- **AND** each marker displays the location name on hover
- **AND** all 6 unique locations from the database are represented

#### Scenario: Location selection via map
- **WHEN** a user clicks on a location marker
- **THEN** that location is selected for detailed viewing
- **AND** the temperature time-series plot updates to show data for that location
- **AND** the location dropdown (if present) synchronizes to show the same selection

### Requirement: Temperature Time-Series Visualization
The dashboard SHALL display an interactive line chart showing temperature trends over time for the selected location.

#### Scenario: Display temperature trends
- **WHEN** a location is selected
- **THEN** a line chart displays both maximum and minimum temperatures over time
- **AND** dates are shown on the x-axis in chronological order
- **AND** temperature values (°C) are shown on the y-axis
- **AND** the chart includes a legend distinguishing max and min temperatures

#### Scenario: Interactive chart tooltips
- **WHEN** a user hovers over a data point on the chart
- **THEN** a tooltip displays the exact date, temperature value, and series type (max/min)
- **AND** the tooltip is clearly readable

#### Scenario: Multiple forecast days
- **WHEN** multiple forecast days exist for a location
- **THEN** all days are plotted on the time-series chart
- **AND** the trend line connects all data points chronologically

### Requirement: Map-Chart Integration
The dashboard SHALL maintain synchronized state between the map, dropdown selector, and time-series chart.

#### Scenario: Selection synchronization
- **WHEN** a user selects a location via the map
- **THEN** the dropdown selector updates to show the same location
- **AND** the time-series chart updates with that location's data

#### Scenario: Dropdown to map synchronization
- **WHEN** a user selects a location via the dropdown
- **THEN** the corresponding map marker is highlighted or centered
- **AND** the time-series chart updates accordingly
