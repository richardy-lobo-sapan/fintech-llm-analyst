# bigquery_client.py
# Handles BigQuery connection and query execution.
# Locally: uses gcloud application default credentials
# On Streamlit Cloud: uses service account from st.secrets

from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import streamlit as st
import os

def get_client():
    """
    Creates BigQuery client.
    - On Streamlit Cloud: uses service account credentials from secrets
    - Locally: uses gcloud application default credentials
    """
    try:
        # Streamlit Cloud — secrets exist
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        return bigquery.Client(
            credentials=credentials,
            project="dbt-ecommerce-496202"
        )
    except Exception:
        # Local — fall back to gcloud credentials
        return bigquery.Client(project="dbt-ecommerce-496202")


def run_query(sql: str) -> pd.DataFrame:
    """
    Runs a SQL query on BigQuery and returns results as DataFrame.
    """
    client = get_client()
    try:
        query_job = client.query(sql)
        result = query_job.result()
        df = result.to_dataframe()
        return df
    except Exception as e:
        raise Exception(f"BigQuery error: {str(e)}")