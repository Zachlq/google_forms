import json
import gspread
from google.oauth2 import service_account
import pandas as pd
from gspread_dataframe import set_with_dataframe, get_as_dataframe
import logging
import google.cloud.logging
from google.cloud import storage 
from google.cloud import bigquery
from googleapiclient import discovery
import requests
import config as cfg
import time

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')

client = google.cloud.logging.Client()
client.setup_logging()

bq_client = bigquery.Client()
storage_client = storage.Client()

gcp_bucket = storage.Client().get_bucket(cfg.gcp_bucket)

gcp_blob = gcp_bucket.blob(cfg.creds_file)
KEY = gcp_blob.download_as_string()
KEY = json.loads(KEY)

def upload_to_bq(df: pd.DataFrame, dataset_id: str, table_id: str, write_dispo: str, schema: list):
    
    client = bigquery.Client()

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition=write_dispo
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.schema = schema
    job_config.ignore_unknown_values=True 

    job = client.load_table_from_dataframe(
    df,
    table_ref,
    location='US',
    job_config=job_config)
    
    return job.result()

def get_sheet():
    
    gc = gspread.authorize(service_account.Credentials.from_service_account_info(KEY, scopes=cfg.scope))
    
    sheet_name = []
    
    for sheet in gc.openall():
        if "Data_Education_Resource_Responses" in sheet.title:
            sheet_name.append(sheet)
    
    logging.info(f"Fetching data from sheet {sheet_name[0]}")
    
    sh = gc.open_by_url(cfg.sheet_url).sheet1
    
    df = pd.DataFrame(sh.get_all_records())
    
    return df

def format_df():

    logging.info("Creating data frame...")
    
    df=get_sheet()
    df.rename(columns={
        df.columns[0]: "timestamp",
        df.columns[1]: "product_type_response",
        df.columns[2]: "content_type_response",
        df.columns[3]: "product_help_response"
    }, inplace=True)
    
    df["dt_updated"] = pd.Timestamp.now(tz="US/Eastern")
    
    return df
    
def google_forms(event, context):
    
    df = format_df()
    
    if len(df) > 1:
        logging.info(f"Uploading to {cfg.dataset_id}.{cfg.table_id}...")
        upload_to_bq(df, cfg.dataset_id, cfg.table_id, "WRITE_TRUNCATE", cfg.schema)
        logging.info(f"Upload job processed. Data updated for {cfg.today}")
    else:
        logging.info(f"No new responses for {cfg.today}")

if __name__ == "__main__":
    logging.info(f"Fetching Google Forms responses for {cfg.today}...")
    google_forms("","")
