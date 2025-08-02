Purpose:

The data ingestion module is designed to handle the extraction, transformation, and loading (ETL) of data from various 
sources into a structured format suitable for analysis.

Note the use of the strategy pattern to handle different ticker types. Each ticker type can have its own implementation 
of the schema, allowing for flexibility and extensibility.

Assumptions:
- The data magically shows up in the staging area.
- The data is differential, meaning that the magical data retrieval step is filtered in some way to include only new 
data.
- The module is extensible to accommodate new ticker types in the future.
- The different ticker types might require different schemas or processing logic which can be encapsulated in the 
corresponding strategy classes.
- The ingested data is temporarily stored in a staging table before being analyzed and moved to the final storage 
location.
