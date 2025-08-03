import argparse
from src.env_setup import logger, DB_URL, FILE_PATH, DATASOURCE
from src.data_ingestion.data_ingestion import ingest_data

def main():
    parser = argparse.ArgumentParser(description="Main entry point for the project.")
    parser.add_argument('--ingest', action='store_true', help='Enable data ingestion')
    args = parser.parse_args()

    if args.ingest:
        logger.info("Starting data ingestion...")
        ingest_data(logger, DB_URL, FILE_PATH, DATASOURCE)
        logger.info("Data ingestion completed.")
    else:
        logger.info("No action specified. Use --ingest to run data ingestion.")

if __name__ == "__main__":
    main()