# OptionMetrics coding assignment

## Usage
1. Clone the repository.
2. Optionally, create a virtual environment and activate it.
3. Install the required packages using `pip install -r requirements.txt`.
4. In the root directory, run the script with `python -m main --ingest`.

## Thoughts about the overall design of the solution:
Ideally, in production the incoming data would come in via a streaming service like AWS Kinesis or Kafka, and the data 
ingestion module would be a consumer of that stream. However, for the sake of this assignment, we are assuming that the 
data magically shows up in a staging area.

In the event the data is polled once per day via some data retrieval API, lambda functions could be triggered to start 
the data ingestion module when the data arrives. The data ingestion module would then be responsible for extracting 
the data from an S3 bucket, transforming it into a structured format, and loading it into the appropriate storage 
location. In my example, I have assumed a temporary staging table in a database for each data source since it is likely 
the schema would be different for each one.

### Possible process flow

![high-level-process.svg](high-level-process.svg)