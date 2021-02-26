import requests
import dbclient
import csv
import pandas as pd

#excessive commenting is for my own benefit

#citation:
#https://stackoverflow.com/questions/35371043/use-python-requests-to-download-csv

CSV_URL = 'https://il-covid-zip-data.s3.us-east-2.amazonaws.com/latest/zips.csv'
#TEST_URL = 

with requests.Session() as s:
    download = s.get(CSV_URL)

    decoded_content = download.content.decode('utf-8') # this is the entire csv as one string

    readout = csv.reader(decoded_content.splitlines(), delimiter=',') #readout is a _csv.reader object
    mylist = list(readout) #mylist is a list of lists--each list a row, first row is header
    headers = mylist[0:1]
    df = pd.DataFrame(mylist[1:],columns=headers)

    #select columns to keep
    select_columns = ['date','zipcode','confirmed_cases',
                      'confirmed_cases_change','total_tested',
                      'total_tested_change']
    select_df = df.loc[:, select_columns]
