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
    get zipcode for geo coords via mapbox api

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

