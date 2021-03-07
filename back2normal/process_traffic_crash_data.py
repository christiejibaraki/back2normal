from data import data_transformations
from data.socrata import soda_data, socrata_api_requests
from util import api_util

# Traffic Crashes
data_obj = soda_data.TRAFFIC_CRASH_DATA_OBJ  # 1
api_resp = socrata_api_requests.SocrataAPIClient(data_obj.request_url)  # 2

# convert location to zip
# compute count by zip
# compute weekly averages
# store table

data_df = api_resp.data_df
access_token = api_util.get_mapbox_app_token()
data_df['zipcode'] = data_df.apply(
    lambda x: data_transformations.get_zipcode_from_mapbox(
        x['longitude'], x['latitude'], access_token), axis=1)

