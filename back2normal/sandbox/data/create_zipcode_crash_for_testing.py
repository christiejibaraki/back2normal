from data import data_transformations
from data.socrata import soda_data, socrata_api_requests
from util import api_util, basic_io
import pandas as pd
import requests

#######################################################
####### SCRIPT FOR CREATING TEST SET ########
#######################################################

loc_to_zip_dict = basic_io.read_json_to_dict(data_transformations.LOC_ZIP_FILE_PATH)


def get_zip_from_dict(lat, long):
    location = repr((long, lat))
    if location in loc_to_zip_dict:
        return loc_to_zip_dict[location]
    return None


data_df = pd.read_csv("historical_traffic_1_1_2019-3_7_20201.csv")

data_df['zipcode'] = data_df.apply(
    lambda x: get_zip_from_dict(x['latitude'],
                                x['longitude']),
    axis=1)

pd.set_option('display.max_columns', None)
data_df.zipcode.isna().sum()
data_df_subset = data_df.loc[data_df.zipcode.isna() == False, ]

data_df_subset['SHORT_DATE'] = data_df_subset['CRASH_DATE'].apply(lambda x: x[0:x.find("T")])
data_df_subset.to_csv("subset_zipcode_crashes.csv", index=False)

zipcode_crash_counts = pd.DataFrame(data_df_subset.value_counts(subset=['SHORT_DATE', 'zipcode']))
zipcode_crash_counts.reset_index(inplace=True)
zipcode_crash_counts.columns = ['SHORT_DATE', 'zipcode', 'crash_count']
zipcode_crash_counts.to_csv("zipcode_crash_data_testing.csv", index=False)
