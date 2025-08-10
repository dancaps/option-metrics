import unittest
import pandas as pd
from sqlalchemy import create_engine, text
from src.analysis.analyzer import Analyzer

class DummyLogger:
    def __init__(self):
        self.messages = []
    def info(self, msg):
        self.messages.append(msg)

class TestPutCallRatio(unittest.TestCase):
    def setUp(self):
        self.DB_URL = "postgresql+psycopg2://postgres:password@localhost:5432/postgres"
        self.engine = create_engine(self.DB_URL)
        # Clean up tables if they exist
        with self.engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS test_putcall"))
            conn.execute(text("DROP TABLE IF EXISTS test_putcall_analysis"))
        # Sample data
        data = [
            {"Date": "2024-06-01", "Expiration": "2024-06-15", "CallPut": "C", "Volume": 100},
            {"Date": "2024-06-01", "Expiration": "2024-06-15", "CallPut": "P", "Volume": 50},
            {"Date": "2024-06-02", "Expiration": "2024-06-15", "CallPut": "C", "Volume": 80},
            {"Date": "2024-06-02", "Expiration": "2024-06-15", "CallPut": "P", "Volume": 120},
        ]
        self.df = pd.DataFrame(data)
        self.source_table = "test_putcall"
        self.output_table = "test_putcall_analysis"
        self.df.to_sql(self.source_table, self.engine, index=False, if_exists="replace")
        self.logger = DummyLogger()

    def tearDown(self):
        # Clean up tables
        with self.engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS test_putcall"))
            conn.execute(text("DROP TABLE IF EXISTS test_putcall_analysis"))
            conn.commit()  # Comment out if you want to inspect the DB after tests
        self.engine.dispose()

    def test_put_call_ratio(self):
        Analyzer.calculate_put_call_ratio(self.DB_URL, self.source_table, self.output_table, self.logger)
        # Read output table
        result = pd.read_sql_table(self.output_table, self.engine)
        expected_cols = {"Date", "Expiration", "C", "P", "PutCallRatio", "PrevRatio", "RatioChange", "SignificantChange"}
        self.assertTrue(expected_cols.issubset(result.columns))
        row = result[result["Date"] == "2024-06-01"].iloc[0]
        self.assertAlmostEqual(row["PutCallRatio"], 0.5)
        row2 = result[result["Date"] == "2024-06-02"].iloc[0]
        self.assertAlmostEqual(row2["PutCallRatio"], 1.5)
        self.assertTrue(any("Put-Call Ratio analysis saved" in msg for msg in self.logger.messages))

if __name__ == "__main__":
    unittest.main()