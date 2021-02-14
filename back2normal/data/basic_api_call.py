import os
import pandas as pd
from sodapy import Socrata
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from util import basic_io

# in .config/ create socrata_chicago_keys.json with contents:
'''
{"api_key":"<your-api-key>",
 "api_secret_key":"<your-secret-key>",
 "app_token":"<your-app-token>"}
 '''

API_KEY_STR = "api_key"
API_SECRET_KEY_STR = "api_secret_key"
APP_TOKEN_STR = "app_token"

path_to_keys = os.path.join('config', 'socrata_chicago_keys.json')
keys = basic_io.read_json_to_dict(path_to_keys)

DOMAIN = "data.cityofchicago.org"

# documentation for sodapy
# https://github.com/xmunoz/sodapy/blob/master/sodapy/socrata.py
client = Socrata(
        DOMAIN,
        keys[APP_TOKEN_STR],
        timeout=10
    )

#### vaccination data
# what we'd actually implement (assuming a live website)
# (1) get existing (historical) obs for all datasets
# (2) store in lightweight db
# (3) request for each relevant dataset per day
# (4) update db with daily data
# ??
dataset_identifier = "553k-3xzc"
results = client.get(dataset_identifier, limit=2000)
results_df = pd.DataFrame.from_records(results)
print(results_df)