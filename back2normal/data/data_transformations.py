import os
import requests
from datetime import datetime, timedelta
from util import basic_io

# https://strftime.org/ python datetime formats
DAYS_IN_WEEK = 7
SATURDAY_INDEX = 5
SOCRATA_STR_DT_FORMAT = '%Y-%m-%d'

# data sourced from https://ibis.health.state.nm.us/resource/MMWRWeekCalendar.html#part3
# created from script sandbox/data/create_cdc_mmwr_lookup.py
WEEK_END_TO_CDC_WEEK = basic_io.read_json_to_dict("data/cdc_week.json")


def get_zipcode_from_mapbox(long, lat, access_token):
    """
    :param long: longitude
    :param lat: latitude
    :param access_token: mapbox api access token
    :return: (int) zipcode for input long, lat
    """
    request_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{long},{lat}.json"
    params = {"types": "postcode", "access_token": access_token}
    response = requests.get(url=request_url, params = params)

    return int(response.json()['features'][0]['text'])


def get_next_saturday(YYYY_MM_DD_str):
    """
    :param YYYY_MM_DD_str: (str) date in format 'YYYY-MM-DD'
    :return: datetime object representing the next saturday
    """
    date_obj = datetime.strptime(YYYY_MM_DD_str, SOCRATA_STR_DT_FORMAT)
    date_obj.weekday()
    t = timedelta((SATURDAY_INDEX - date_obj.weekday()) % DAYS_IN_WEEK)
    return date_obj + t


def get_cdc_mmwr_week(YYY_MM_DD_str):

    next_saturday = get_next_saturday(YYY_MM_DD_str)
    next_sat_str = next_saturday.strftime(SOCRATA_STR_DT_FORMAT)
    return WEEK_END_TO_CDC_WEEK[next_sat_str]

################################################################
################################################################
#          examples below to be removed
################################################################
################################################################

## zip code from long, lat
from util import basic_io
path_to_keys = os.path.join('config', 'mapbox_keys.json')
keys = basic_io.read_json_to_dict(path_to_keys)
app_token = keys["app-token"]

long = -73.989
lat = 40.733
zip = get_zipcode_from_mapbox(long, lat, app_token)
print(zip)

### date of next saturday
## (because CDC MMWR weeks end on Saturdays)
input = "2020-04-28T17:56:00.000" # answer is 5/2/2020, week 18
yyyymmdd_str = input[0:input.find("T")]

print(get_next_saturday(yyyymmdd_str))
print(get_cdc_mmwr_week(yyyymmdd_str))
