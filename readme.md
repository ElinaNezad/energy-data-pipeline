# Energy Data Pipeline

This project is an end-to-end data pipeline that fetches energy market data from an external API, stores it in Azure Cosmos DB, and visualizes it using a Streamlit dashboard.

---

## Architecture

The solution includes three main components:

### Azure Function (Timer Trigger)

- Runs on a configurable schedule (e.g., every 5 minutes)
- Fetches data from the external API
- Processes and stores the data in Cosmos DB

### Azure Cosmos DB (NoSQL)

- Stores structured data using the SQL API
- Supports historical data storage
- Enables efficient querying

### Streamlit Dashboard

- Reads data from Cosmos DB
- Provides interactive filtering and visualization
- Displays near real-time insights

**Data Flow:**

API → Azure Function → Cosmos DB → Dashboard

---

## Features

- Scheduled data ingestion (Timer Trigger)
- Cloud-based storage using Cosmos DB
- Interactive dashboard with:
  - Latest data view
  - Last week filtering
  - Custom date range selection
  - Area filtering (DK1 / DK2)
  - Time-series visualization
  - Timezone conversion (UTC → local time)
  - Manual refresh button
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
"FUNCTIONS*WORKER_RUNTIME": "python",
"TIMER_SCHEDULE": "0 */5 \* \* \* \*",
"COSMOS_ENDPOINT": "your_endpoint",
"COSMOS_KEY": "your_key"

}
}
example: timer is every 5 minutes

### 4. Run Azure Function

in the second terminal :
func start

### 5. Run Streamlit Dashboard

in the third terminal:
streamlit run dashboard.py

### 6. Run Tests

pytest -v
