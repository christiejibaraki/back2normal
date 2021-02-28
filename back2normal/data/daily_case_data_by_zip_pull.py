import os
import requests
import csv
import pandas as pd

#excessive commenting is for my own benefit

#citation:
#https://stackoverflow.com/questions/35371043/use-python-requests-to-download-csv

CSV_URL = 'https://il-covid-zip-data.s3.us-east-2.amazonaws.com/latest/zips.csv'
SELECT_COLUMNS = ['date', 'zipcode', 'confirmed_cases',
                  'confirmed_cases_change', 'total_tested',
                  'total_tested_change']
CSV_FILE_PATH = os.path.join("resources", "IDPH", "idph_covid_daily.csv")


def get_daily_covid_data_from_api(testing=False):
    """
    downloads historical IDPH daily covid case data by zipcode
    if testing is true, read data from csv instead

    returns pandas DataFrame with columns in SELECT_COLUMNS

    """

    if testing:
        return get_daily_covid_data_from_file()

    with requests.Session() as s:
        download = s.get(CSV_URL)

        # returns the entire csv as string
        decoded_content = download.content.decode('utf-8')

        # readout is a _csv.reader object
        readout = csv.reader(decoded_content.splitlines(), delimiter=',')

        # list of list, where each list is a row and 0th row is header
        data_list = list(readout)
        df = pd.DataFrame(data_list[1:], columns=data_list[0])

        #select columns to keep
        select_df = df.loc[:, SELECT_COLUMNS]
        return select_df


def get_daily_covid_data_from_file():
    """
    for use during testing (since the file download from s3 is slow)

    reads historical IDPH daily covid case data by zipcode from CSV
    returns data in pandas DataFrame
    """

    data = pd.read_csv(CSV_FILE_PATH)
    assert set(data.columns) == set(SELECT_COLUMNS)
    return data
