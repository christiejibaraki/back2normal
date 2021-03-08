import os
import requests
from datetime import datetime, timedelta
from util import basic_io
import pandas as pd

# https://strftime.org/ python datetime formats
DAYS_IN_WEEK = 7
SATURDAY_INDEX = 5
SOCRATA_STR_DT_FORMAT = '%Y-%m-%d'

# data sourced from https://ibis.health.state.nm.us/resource/MMWRWeekCalendar.html#part3
# created from script sandbox/data/create_cdc_mmwr_lookup.py
WEEK_END_TO_CDC_WEEK = basic_io.read_json_to_dict("resources/cdc_week.json")

# hard coded moving avg values
MOVING_AVG_WINDOW = 7
MOVING_AVG_COL_PREFIX = 'AVG7DAY_'

#standarizing zipcode and date columns
ZIP_COL_NAME = 'ZIPCODE'
DATE_COL_NAME = 'STD_DATE'


def get_chicago_zipcodes():
    """
    read resource json to list of 59 chicago zipcodes

    :return: list of (str) where each str is zipcode of chicago
    """
    return basic_io.read_json_to_dict(os.path.join(
        "resources", "chicago_zips_59.json"))


def get_zipcode_from_mapbox(long, lat, access_token):
    """
    get zipcode for geo coords via mapbox api

    :param long: longitude
    :param lat: latitude
    :param access_token: mapbox api access token
    :return: (int) zipcode for input long, lat
    """
    request_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{long},{lat}.json"
    params = {"types": "postcode", "access_token": access_token}
    response = requests.get(url=request_url, params=params)

    return int(response.json()['features'][0]['text'])


def get_next_saturday(YYYY_MM_DD_str):
    """
    get date obj representing nearest saturday AFTER input date

    :param YYYY_MM_DD_str: (str) date in format 'YYYY-MM-DD'
    :return: datetime object representing the next saturday
    """
    date_obj = datetime.strptime(YYYY_MM_DD_str, SOCRATA_STR_DT_FORMAT)
    days_until_saturday = timedelta((SATURDAY_INDEX - date_obj.weekday()) % DAYS_IN_WEEK)
    return date_obj + days_until_saturday


def get_cdc_mmwr_week(YYY_MM_DD_str):
    """
    get CDC MMWR week for input date string (weeks are Sun-Sat)
    See https://ibis.health.state.nm.us/resource/MMWRWeekCalendar.html#part3

    :param YYY_MM_DD_str: (str) date
    :return: CDC week number
    """
    next_saturday = get_next_saturday(YYY_MM_DD_str)
    next_sat_str = next_saturday.strftime(SOCRATA_STR_DT_FORMAT)
    return WEEK_END_TO_CDC_WEEK[next_sat_str]


def compute_moving_avg_from_daily_data(daily_data_df, zipcode_col_name, date_col_name, cols_to_avg):
    """
    computes a 7 day average for input columns in cols_to_avg

    functions takes a pandas dataframe, the name of the column containing zipcode,
    the name of the column containing date, and a list of variables to be averaged.

    returns the dataframe with appended average columns
    (there will be one new column for every col in cols_to_avg, which
    represents the 7 day moving average for that col on that day)

    new columns names 'AVG7DAY_' + orig col name

    input:
        daily_data_df: pandas DataFrame
        zipcode_col_name (str) name of col containing zipcode
        date_col_name: (str) name of col containing date
        cols_to_avg: (list) of (str) where each item is name of col to be averaged

    returns:
        NA, appends cols to dataframe
    """

    daily_data_df.sort_values(date_col_name, inplace=True)

    for col_name in cols_to_avg:
        new_col_name = MOVING_AVG_COL_PREFIX + col_name
        daily_data_df[new_col_name] = (
            daily_data_df.groupby(zipcode_col_name)[col_name].
            rolling(window=MOVING_AVG_WINDOW).mean().reset_index(level=0, drop=True))


def convert_df_dtypes(data_df):
    """
    Updates the data types in data_df.
    If API returns data as str, use this function to convert numeric types.

        1. Attempts to convert all fields to numeric types (float or integer)
        2. Then converts non numeric types back to string

    input: pandas DataFrame
    returns: pandas DataFrame with modified dtypes

    """
    data_df = data_df.apply(pd.to_numeric, errors='ignore')
    data_df = data_df.convert_dtypes(convert_integer=False)
    return data_df


def verify_chicago_zip(zip_str):
    """
    For running inside of standardize_zip_code apply function
    """
    if not zip_str or zip_str[0] != '6':
        return False

    return True

def standardize_zip_code(df, original_zip_col_name):
    df.rename({original_zip_col_name: ZIP_COL_NAME},inplace=True)
    df.ZIP_COL_NAME = df.ZIP_COL_NAME.astype(str)
    mask = df.ZIP_COL_NAME.apply(verify_chicago_zip)
    df.ZIP_COL_NAME[mask == False] = None
