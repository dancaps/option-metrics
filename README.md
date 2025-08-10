# OptionMetrics coding assignment

## Usage
1. Clone the repository.
2. Optionally, create a virtual environment and activate it.
3. Install the required packages using `python -m pip install -r requirements.txt`.
4. Environment variables can be set in a `.env` file in the root directory. If no .env is available, default values will 
be assigned. To see a list of all variables and their defaults, look in the [env_setup.py](src/env_setup.py) file. 
5. In the root directory, run the module with `python -m main` to get the available flags. 

Example usage:
   ```bash 
     python -m main --ingest
   ```

Tests can be run with:
   ```bash
     python -m unittest discover -s tests
   ```

### Data processing flow
Based on the provided information (and for demonstration purposes), the data processing flow is outlined in the diagram 
below.

![high-level-process.svg](high-level-process.svg)

## Data Ingestion Module
The data ingestion module handles the extraction, transformation, and loading (ETL) of data from various sources into a 
structured format suitable for analysis.

Note the use of the strategy pattern to handle different datasources. Each datasource can have its own implementation 
of the schema, allowing for flexibility and extensibility.

#### Assumptions
- The data magically shows up in the staging area. The thought is the retrival process would drop the data into a folder
in a S3 bucket which would trigger a lambda function with the specific run configuration for that datasource.
- The data is differential, meaning that the magical data retrieval step is filtered in some way to include only new 
data.
- If the ingest is run more than once it will overwrite the existing data in the staging table.
- The module needs to be extensible to accommodate a new datasource and potentially new schemas in the future.
- The different datasources might require different processing logic which can be encapsulated in the corresponding 
strategy classes.
- The ingested data is temporarily stored in a staging table before being analyzed.

## Analysis Module

The methods in the analysis module perform various analyses on the ingested data and writing the results to output 
tables.

#### Put/Call Ratio Analysis:
- Groups data by Date, Expiration, and CallPut to aggregate volumes for calls and puts.
- Calculates the daily Put-Call Ratio as Put Volume divided by Call Volume.
- Computes the previous day's ratio and the change from the previous day for each expiration.
- Flags days with significant changes in the ratio (absolute change > 0.5).
- Saves the analysis results to the specified output table in the database.

#### Volume and Open Interest Analysis:
- Calculates average volume per option.
- Flags rows where volume is more than 2x average.
- Calculates day-over-day open interest change and flags >50% changes.
- Adds strike and expiration buckets for grouping.
- Saves the analysis results to the specified output table in the database.

## Thoughts about the overall design of the solution:
Ideally, in production the incoming data would come in via a streaming service like AWS Kinesis or Kafka, and the data 
ingestion module would be a consumer of that stream. However, for the sake of this assignment, I'm assuming that the 
data magically shows up in a staging area as a csv file.

In the event the data is polled once per day via some data retrieval API, lambda functions could be triggered to start 
the data ingestion module when the data arrives. The data ingestion module would then be responsible for extracting 
the data from an S3 bucket, transforming it into a structured format, and loading it into the appropriate storage 
location. In my example, I have assumed a temporary staging table in a database for each data source since it is likely 
the schema would be different for each one.

Using a tool like AWS batch to run a containerized version of this module is one possible solution to the analysis of 
the temporary tables. Runtime configurations can be passed in to change the behavior of the module. 