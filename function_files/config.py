from datetime import datetime

today = datetime.today().strftime("%Y-%m-%d")

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

sheet_url = "https://docs.google.com/spreadsheets/d/1vx8Vcv_WCwhyde1Cy4a2EbRMRXdBvW0tB0UzdnV6tT4/edit?resourcekey#gid=1727258913"

gcp_bucket = "proj_creds"
creds_file = "ornate-reef-332816-9c1cd45c201e.json"

dataset_id = "google_forms_responses"
table_id = "pipeline_product_survey"

schema = [
    {"name": "timestamp", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "product_type_response", "type": "STRING", "mode": "NULLABLE"},
    {"name": "content_type_response", "type": "STRING", "mode": "NULLABLE"},
    {"name": "product_help_response", "type": "STRING", "mode": "NULLABLE"},
    {"name": "dt_updated", "type": "TIMESTAMP", "mode": "NULLABLE"}
]
