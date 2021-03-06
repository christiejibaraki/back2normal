import os
import requests
import pandas as pd
from util import api_util, basic_io


zip_lst = basic_io.read_json_to_dict('resources/chicago_zips_59.json')
ZIPS = ",".join(zip_lst)
CENSUS_API_KEY = api_util.get_census_key()
VARIABLE_LST = 'NAME,DP02_0017PE,DP02_0001E'
# ACS API Documentation:
# https://www.census.gov/content/dam/Census/library/publications/2020/acs/acs_api_handbook_2020.pdf
# VARIABLE_LST
# The “Variable List” includes the variable(s) you are
# requesting. You can include up to 50 variables in
# a single API query (separated by commas). In this
# data set, the variable called NAME provides the
# name of the geographic area(s) that you are using
# to limit your search.

# We're using the 2019 ACS 5-year data profiles
# Full list of variables: https://api.census.gov/data/2019/acs/acs5/profile/variables.html

query_url = f"https://api.census.gov/data/2019/acs/acs5/profile?get={VARIABLE_LST}&for=zip%20code%20tabulation%20area:{ZIPS}&in=state:17&key={CENSUS_API_KEY}"

resp = requests.get(query_url)
data_df = pd.DataFrame.from_dict(resp.json())


# Vars of interest
# DP02_0017PE -- Percent!!HOUSEHOLDS BY TYPE!!Total households!!Average family size
#