import requests
import pandas as pd


class RequestResponse:

    def __init__(self, request_url, params, select_field_list=None,
                 group_by_field_list=None):

        self.request_url = None
        self.response = None
        self.data_df = None

        # for reviewing datatypes
        self.header_fields = None
        self.header_dtypes = None
        self.df_dtypes = None

        self._get_request(request_url, params, select_field_list,
                          group_by_field_list)

    def _get_request(self, request_url, params, select_field_list,
                     group_by_field_list):
        # socrata query: https://dev.socrata.com/docs/queries/

        # For header codes included in response object: 
        # https://dev.socrata.com/docs/response-codes.html

        # Difference between a Request and a Response object:
        # https://requests.readthedocs.io/en/master/user/advanced/#request-and-response-objects
        # ()

        # if select_field_list not empty or None, create select query
        if not not select_field_list:  #could this just be if select_field_list:
            select_statement = f"?$select={', '.join(select_field_list)}"
            request_url = request_url + select_statement
            if not not group_by_field_list: 
            # I nested this because there can only be a group_by query if
            # there is also a select query that specifies an aggregation method
            # group query documentation: https://dev.socrata.com/docs/queries/group.html
            # should add some error handling
                group_statement = f"&$group={', '.join(group_by_field_list)}"
                request_url = request_url + group_statement


        

        # get and parse response
        self.response = requests.get(request_url, params = params)
        self.request_url = self.response.request.url
        self.header_fields = self.response.headers['X-SODA2-Fields']
        self.header_dtypes = self.response.headers['X-SODA2-Types']

        # convert to pandas df
        self.data_df = pd.DataFrame.from_dict(self.response.json())
        self.df_dtypes = self.data_df.dtypes

    def convert_types(self):
        # making this a method that's not called by constructor for now
        # but eventually probably makes sense to have constructor do
        # converting itself or call this method
        self.data_df = self.data_df.apply(pd.to_numeric, errors='ignore')
        self.data_df = self.data_df.convert_dtypes(convert_integer=False)
        self.df_dtypes = self.data_df.dtypes
