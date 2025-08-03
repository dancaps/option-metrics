from sqlalchemy import create_engine, inspect, Table, MetaData

def list_tables(DB_URL):
    """
    Returns a list of all table names in the database and logs them to the console.
    """
    engine = create_engine(DB_URL)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    engine.dispose()
    return tables


def drop_table(DB_URL, table_name, logger):
    """
    Drops the specified table from the database.
    """
    engine = create_engine(DB_URL)
    metadata = MetaData()
    try:
        table = Table(table_name, metadata, autoload_with=engine)
        table.drop(engine)
        logger.info(f"Table [{table_name}] dropped successfully.")
    except Exception as e:
        logger.info(f"Error dropping table [{table_name}]: {e}")
    finally:
        engine.dispose()