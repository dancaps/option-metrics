import argparse

from src.analysis.analyzer import Analyzer
from src.data_ingestion.data_ingestor import DataIngestor
from src.env_setup import logger, DB_URL, FILE_PATH, DATASOURCE
from src.helpers import list_tables, drop_table


def main():
    parser = argparse.ArgumentParser(description="Main entry point for the project.")
    parser.add_argument('--ingest', action='store_true', help='Enable data ingestion')
    parser.add_argument('--putcall', action='store_true', help='Run Put-Call Ratio analysis')
    parser.add_argument('--listtables', action='store_true', help='List all tables in the database')
    parser.add_argument('--droptable', type=str, help='Drop the specified table from the database')
    parser.add_argument('--source_table', type=str, help='Source table for analysis')
    parser.add_argument('--output_table', type=str, help='Output table for analysis results')
    args = parser.parse_args()

    did_action = False

    if args.ingest:
        logger.info("Starting data ingestion...")
        DataIngestor.ingest_data(logger, DB_URL, FILE_PATH, DATASOURCE)
        logger.info("Data ingestion completed.")
        did_action = True

    if args.putcall:
        if not args.source_table or not args.output_table:
            logger.info("Both --source_table and --output_table must be specified for analysis.")
            return
        logger.info("Starting Put-Call Ratio analysis...")
        Analyzer.calculate_put_call_ratio(DB_URL, args.source_table, args.output_table, logger)
        logger.info("Put-Call Ratio analysis completed.")
        did_action = True

    if args.listtables:
        tables = list_tables(DB_URL)
        logger.info("Tables in the database:\n  %s", str.join("\n  ", tables))
        did_action = True

    if args.droptable:
        drop_table(DB_URL, args.droptable, logger)
        did_action = True

    if not did_action:
        parser.print_help()

if __name__ == "__main__":
    main()