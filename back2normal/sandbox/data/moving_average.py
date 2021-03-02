import pandas as pd
from data import soda_data, api_requests


daily_vacc_data = soda_data.datasets[0]
response = api_requests.SocrataAPIClient(daily_vacc_data.request_url)
response.convert_types()
response.data_df

daily_data_df = response.data_df
print(daily_data_df.columns)
zipcode_col_name = 'zip_code'
date_col_name = 'date'

# sort on date
daily_data_df.sort_values(date_col_name, inplace=True)
pd.set_option('display.max_columns', None)
print(daily_data_df.head())

zipcode_subset_test = daily_data_df.loc[daily_data_df[zipcode_col_name]=="60657"]


# function to implement
def compute_moving_avg_from_daily_data(daily_data_df, zipcode_col_name, date_col_name, cols_to_avg):
    """
    computes a 7 day moving average for input columns in cols_to_avg

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
        nothing?? appends cols to dataframe
    """

    # 1. group by zipcode?
    # 2. sort by date
    # 2. then apply https://www.datacamp.com/community/tutorials/moving-averages-in-pandas?
    #       assume adjacent rows are 1 day apart, use rolling window = 7
    # 3. ????

    pass
