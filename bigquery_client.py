# bigquery_client.py
# This file handles the connection to BigQuery and runs SQL queries.
# It has ONE job: take a SQL string, run it, return the results.
# We keep this separate from llm.py because connecting to a database
# and generating SQL are two different responsibilities.

from google.cloud import bigquery
import pandas as pd

# This creates a BigQuery client using the credentials you set up
# with gcloud auth application-default login.
# It automatically finds the credentials file on your machine —
# you don't need to pass any keys manually.
client = bigquery.Client(project="dbt-ecommerce-496202")


def run_query(sql: str) -> pd.DataFrame:
    """
    Runs a SQL query on BigQuery and returns the results as a DataFrame.
    
    Args:
        sql: A valid BigQuery SQL string
        
    Returns:
        A pandas DataFrame with the query results
        
    Raises:
        Exception: If the query fails, returns the error message
    """
    try:
        query_job = client.query(sql)      # sends the query to BigQuery
        result = query_job.result()        # waits for it to finish
        df = result.to_dataframe()         # converts result to pandas DataFrame
        return df
    except Exception as e:
        raise Exception(f"BigQuery error: {str(e)}")