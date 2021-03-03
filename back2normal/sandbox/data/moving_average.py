import pandas as pd
from data import soda_data, api_requests




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
    # 3. Profit?
    daily_data_df.sort_values(date_col_name, inplace = True)

    for col_name in cols_to_avg:
        new_col_name = 'AVG7DAY' + col_name
        daily_data_df[new_col_name] = daily_data_df.groupby(zipcode_col_name)[col_name].rolling(window = 7).mean().reset_index(level = 0, drop=True)



daily_vacc_data = soda_data.datasets[0]
response = api_requests.SocrataAPIClient(daily_vacc_data.request_url)
response.convert_types()
response.data_df

daily_data_df = response.data_df
# daily_data_df.sort_values(date_col_name, inplace = True)

# zipcode_col_name = 'zip_code'
# date_col_name = 'date'
# cols_to_avg = ['total_doses_daily']
# col_name = 'total_doses_daily'



# daily_data_df.groupby(zipcode_col_name)[col_name].rolling(window = 7).mean()
# daily_data_df.groupby(zipcode_col_name)[col_name].rolling(window = 7).mean()
# daily_data_df[new_col_name] = daily_data_df.groupby(zipcode_col_name)[col_name].rolling(window = 7).mean().reset_index(level = 0, drop=True)


compute_moving_avg_from_daily_data(daily_data_df, 'zip_code', 'date',['total_doses_daily'])