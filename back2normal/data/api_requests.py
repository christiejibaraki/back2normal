import os
import requests
import sqlite3
import pandas as pd
from util import basic_io
import sys


class RequestResponse:

    def __init__(self, request_url, params, query=""):

        self._session = requests.Session()
        self.request = None
        self.response = None
        self.data_df = None

        # for reviewing datatypes
        self.header_fields = None
        self.header_dtypes = None
        self.df_dtypes = None

        self._get_request(request_url, params)

    def _get_request(self, request_url, params, query=""):
        # need to implement query
        # https://dev.socrata.com/docs/queries/

        # For header codes included in response object: 
        # https://dev.socrata.com/docs/response-codes.html

        # Difference between a Request and a Response object:
        # https://requests.readthedocs.io/en/master/user/advanced/#request-and-response-objects
        # ()
       
        self.request = requests.Request(request_url, params)
        self.response = self._session.get(url, params)
        #self.request = self.response.request

        self.data_df = pd.DataFrame.from_dict(self.response.json())
        self.df_dtypes = self.data_df.dtypes

        self.header_fields = self.response.headers['X-SODA2-Fields']
        self.header_dtypes = self.response.headers['X-SODA2-Types']

    def print_request(self):
        # doesn't work, but for debugging queries
        print('{}{}{}'.format(
            self.request.method, self.request.url,
            ''.join('{}={}'.format(k, v) for k, v in self.request.headers.items())
        ))

    def convert_types(self):
        # making this a method that's not called by constructor for now
        # but eventually probably makes sense to have constructor do
        # converting itself or call this method
        self.data_df = self.data_df.apply(pd.to_numeric, errors='ignore')
        self.data_df = self.data_df.convert_dtypes(convert_integer=False)

