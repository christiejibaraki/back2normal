import os
import requests
from util import basic_io


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


# example below to removed
path_to_keys = os.path.join('config', 'mapbox_keys.json')
keys = basic_io.read_json_to_dict(path_to_keys)
app_token = keys["app-token"]

long = -73.989
lat = 40.733

zip = get_zipcode_from_mapbox(long, lat, app_token)
print(zip)