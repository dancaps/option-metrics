import unittest
import pandas as pd
from sqlalchemy import create_engine, text
from src.analysis.analyzer import Analyzer

class DummyLogger:
    def __init__(self):
        self.messages = []
    def info(self, msg):
        self.messages.append(msg)

class TestVolumeOpenInterestAnalysis(unittest.TestCase):
    def setUp(self):
        self.DB_URL = "postgresql+psycopg2://postgres:password@localhost:5432/postgres"
        self.engine = create_engine(self.DB_URL)
        # Clean up tables if they exist
        with self.engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS test_volumeio"))
            conn.execute(text("DROP TABLE IF EXISTS test_volumeio_analysis"))

        # Sample data
        data = [
            {"OptionID": "A", "Date": "2024-06-01", "Volume": 10, "OpenInterest": 100, "Strike": 100, "T": 10, "Expiration": "2024-06-10"},
            {"OptionID": "A", "Date": "2024-06-02", "Volume": 25, "OpenInterest": 160, "Strike": 100, "T": 9, "Expiration": "2024-06-10"},  # Volume outlier, OI +60%
            {"OptionID": "B", "Date": "2024-06-01", "Volume": 5, "OpenInterest": 50, "Strike": 150, "T": 10, "Expiration": "2024-06-10"},
            {"OptionID": "B", "Date": "2024-06-02", "Volume": 6, "OpenInterest": 20, "Strike": 150, "T": 9, "Expiration": "2024-06-10"},   # OI -60%
        ]
        df = pd.DataFrame(data)
        self.source_table = "test_volumeio"
        self.output_table = "test_volumeio_analysis"
        df.to_sql(self.source_table, self.engine, index=False, if_exists="replace")
        self.logger = DummyLogger()

    def tearDown(self):
        # Clean up tables
        with self.engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS test_volumeio"))
            conn.execute(text("DROP TABLE IF EXISTS test_volumeio_analysis"))
            conn.commit() # Comment out if you want to inspect the DB after tests
        self.engine.dispose()

    def test_analyze_volume_open_interest(self):
        Analyzer.analyze_volume_open_interest(self.DB_URL, self.source_table, self.output_table, self.logger)
        df_out = pd.read_sql_table(self.output_table, self.engine)

        # Check outlier flags
        # OptionID A, 2024-06-02: VolumeOutlier should be False, OIOutlier should be True
        row_a = df_out[(df_out["OptionID"] == "A") & (df_out["Date"] == "2024-06-02")].iloc[0]
        self.assertFalse(row_a["VolumeOutlier"])
        self.assertTrue(row_a["OIOutlier"])

        # OptionID B, 2024-06-02: OIOutlier should be True, VolumeOutlier should be False
        row_b = df_out[(df_out["OptionID"] == "B") & (df_out["Date"] == "2024-06-02")].iloc[0]
        self.assertFalse(row_b["VolumeOutlier"])
        self.assertTrue(row_b["OIOutlier"])

if __name__ == "__main__":
    unittest.main()