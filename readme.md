# Energy Data Pipeline

This project is an end-to-end data pipeline that fetches energy market data from an external API, stores it in Azure Blob Storage (or Azurite for local development), and visualizes it using a Streamlit dashboard.

---

## Architecture

The solution includes three main components:

- **Azure Function (Timer Trigger)**  
  Periodically fetches data from the API

- **Blob Storage (Azure / Azurite)**  
  Stores the latest data as a JSON file

- **Streamlit Dashboard**  
  Displays and visualizes the data

**Data Flow:**

API → Azure Function → Blob Storage → Dashboard

---

## Features

- Fetch data from external API
- Configurable timer trigger for periodic data fetching
- Store data in Blob Storage
- Local development using Azurite
- Interactive dashboard with:
  - Latest values (DK1 / DK2)
  - Filtering by area
  - Time-series chart
  - Last update indicator
- Basic error handling
- Unit testing with mocked API responses

---

## Setup & Installation

### 1. Clone repository

bash
git clone <repository_URL>
cd energy-data-pipeline

### 2.install dependencies

pip install -r requirements.txt and install Azurite in extensions

### 3. Configure local.settings.json

{
"IsEncrypted": false,
"Values": {
"AzureWebJobsStorage": "UseDevelopmentStorage=true",
"FUNCTIONS_WORKER_RUNTIME": "python",
"TIMER_SCHEDULE": "0 _/5 _ \* \* \*"
}
}
example: timer is every 5 minutes

### 4. Run Azurite (Local Storage)

in the first terminal:
azurite --skipApiVersionCheck

### 5. Run Azure Function

in the second terminal :
func start

### 6. Run Streamlit Dashboard

in the third terminal:
streamlit run dashboard.py

### 7. Run Tests

pytest -v
