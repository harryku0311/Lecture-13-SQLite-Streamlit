# Project Context

## Purpose
A Python-based weather data crawler that fetches agricultural weather forecasts from Taiwan's Central Weather Administration (CWA) OpenData API and stores the data in a local SQLite database for analysis and historical tracking.

## Tech Stack
- **Language**: Python 3.x
- **HTTP Client**: `requests` library
- **Database**: SQLite 3
- **Data Format**: JSON (from CWA API)
- **Key Libraries**: 
  - `urllib3` (SSL handling)
  - `sqlite3` (database operations)
  - `datetime` (timestamp handling)

## Project Conventions

### Code Style
- Use descriptive function names with verb prefixes (e.g., `fetch_`, `save_`, `init_`)
- Document functions with docstrings explaining purpose
- Use snake_case for variables and functions
- Constants in UPPER_CASE (e.g., `DB_NAME`)
- Include print statements for user feedback on operations

### Architecture Patterns
- **Single-file script architecture**: Main logic in `crawler.py`
- **Database initialization pattern**: Check/create tables before operations
- **Error handling**: Wrap API calls in try-except blocks
- **Data transformation pipeline**: Fetch → Parse → Save
- **Two-table schema**: 
  - `weather_summary` for general weather profiles (text)
  - `daily_forecasts` for location-specific daily data

### Testing Strategy
- Manual testing by running the script and inspecting database contents
- JSON file output (`cwa_weather_data.json`) for verification
- Console output for debugging and progress tracking

### Git Workflow
- Simple workflow for lecture/demo project
- Direct commits to main branch
- Descriptive commit messages

### OpenSpec Change Naming Convention
- **Required Format**: All change IDs MUST use zero-padded sequential numbering prefix
- **Pattern**: `[NN]-[verb]-[description]` where NN is 01, 02, 03, etc.
- **Examples**: 
  - `01-add-streamlit-dashboard`
  - `02-update-database-schema`
  - `03-remove-deprecated-api`
- **Auto-numbering**: Start from 01 and increment for each new change
- **Purpose**: Provides chronological tracking and easier reference to change order

## Domain Context
- **Weather Forecasting**: Agricultural weather forecast data from CWA
- **Data Structure**: Nested JSON with locations, dates, and weather elements (Wx, MaxT, MinT)
- **Time-series Data**: Daily forecasts with timestamps
- **Taiwan Geography**: Location-based forecasts for agricultural regions

## Important Constraints
- **API Rate Limits**: Be mindful of CWA API usage
- **SSL Verification**: Currently disabled (`verify=False`) - should be addressed for production
- **Data Freshness**: No automatic scheduling - manual execution required
- **Database Size**: Accumulates historical data without cleanup/archival strategy

## External Dependencies
- **CWA OpenData API**: `https://opendata.cwa.gov.tw/`
  - Endpoint: Agricultural Weather Forecasts (F-A0010-001)
  - Authentication: API key required (currently embedded in URL)
  - Format: JSON
  - Update Frequency: Check CWA documentation
