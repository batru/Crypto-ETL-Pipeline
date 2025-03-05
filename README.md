# Crypto ETL Pipeline

## Overview
This project is an **Apache Airflow-based ETL pipeline** that extracts cryptocurrency price data from an API, transforms it, and loads it into an **Aiven PostgreSQL database** for further analysis. The pipeline is containerized using Docker to ensure scalability and reproducibility.

## Features
- **Automated Data Extraction**: Fetches real-time crypto price data.
- **Data Transformation**: Cleans and structures the data for storage.
- **PostgreSQL Integration**: Loads the processed data into Aiven PostgreSQL.
- **Airflow DAGs**: Manages and schedules the ETL pipeline.
- **Containerized Setup**: Uses Docker for easy deployment.

## Technologies Used
- **Apache Airflow** - Orchestrating ETL workflows
- **PostgreSQL** - Storing crypto price data
- **Psycopg2** - PostgreSQL adapter for Python
- **Docker** - Containerization for deployment
- **Python** - Core ETL scripting

## Architecture
1. **Extract**: Fetches crypto price data from an API.
2. **Transform**: Cleans and processes the data.
3. **Load**: Inserts structured data into PostgreSQL.
4. **Schedule**: Airflow DAG automates the process.

## Setup Instructions

### Prerequisites
- Docker & Docker Compose
- Apache Airflow
- Aiven PostgreSQL credentials

### Installation
```sh
# Clone the repository
git clone https://github.com/yourusername/crypto-etl.git
cd crypto-etl

# Start Airflow and dependencies
docker-compose up -d

# Initialize Airflow
docker-compose run airflow-init
```

### Configure Airflow Connection
1. In Airflow UI, go to **Admin** → **Connections**.
2. Add a new connection:
   - Conn ID: `aiven_postgres`
   - Conn Type: `Postgres`
   - Host, Schema, Login, Password from Aiven PostgreSQL.

### Running the DAG
```sh
# Trigger the DAG manually
airflow dags trigger Crypto_etl

# Check task logs
airflow tasks logs Crypto_etl load_to_postgres
```

## Troubleshooting
- **Airflow `aiven_postgres` not found**: Ensure you’ve configured the connection in Airflow UI.
- **Table `crypto_prices` does not exist**: Run the table creation SQL before loading data.

```sql
CREATE TABLE crypto_prices (
    id SERIAL PRIMARY KEY,
    crypto VARCHAR(50),
    price NUMERIC,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## License
MIT License

## Author
Batrudin Haji
