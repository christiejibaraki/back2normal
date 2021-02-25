
class SodaData:

    def __init__(self, dataset_name, table_name, identifier, desired_attr_lst=None):

        self.dataset_name = dataset_name
        self.table_name = table_name
        self.identifier = identifier
        self.base_url = f"https://data.cityofchicago.org/resource/{identifier}.json"

        # if empty or None, will use all available fields
        self.desired_attr_lst = desired_attr_lst

datasets = []

############################################
######## COVID-19 Vaccinations by ZIP Code
############################################

# https://dev.socrata.com/foundry/data.cityofchicago.org/553k-3xzc

datasets.append(SodaData("COVID-19 Vaccinations by ZIP Code",
                         "VACCINATIONS_DAILY",
                         "553k-3xzc",
                         ["zip_code", "date",
                          "total_doses_daily", "total_doses_cumulative",
                          "vaccine_series_completed_daily",
                          "vaccine_series_completed_percent_population",
                          "population"]))

############################################
######## COVID-19  Cases, Tests, and Deaths by ZIP Code
############################################

#https://dev.socrata.com/foundry/data.cityofchicago.org/yhhz-zm2v

datasets.append(SodaData("COVID-19 Cases, Tests, and Deaths by ZIP Code",
                         "CASES_WEEKLY",
                         "yhhz-zm2v",
                         ["zip_code", "week_number", "week_start", "week_end",
                          "cases_weekly", "cases_cumulative", "case_rate_weekly",
                          "tests_weekly", "tests_cumulative", "test_rate_weekly",
                          "percent_tested_positive_weekly",
                          "deaths_weekly", "deaths_cumulative", "death_rate_weekly",
                          "row_id"]))

############################################
######## Traffic Crashes - Crashes
############################################

# https://dev.socrata.com/foundry/data.cityofchicago.org/85ca-t3if

datasets.append(SodaData("Traffic Crashes - Crashes",
                         "TRAFFIC_CRASHES",
                         "85ca-t3if",
                         ["CRASH_DATE", "POSTED_SPEED_LIMIT", "TRAFFIC_CONTROL_DEVICE",
                          "FIRST_CRASH_TYPE", "PRIM_CONTRIBUTORY_CAUSE",
                          "STREET_NO", "STREET_DIRECTION", "STREET_NAME",
                          "MOST_SEVERE_INJURY", "CRASH_HOUR",
                          "LATITUDE", "LONGITUDE"]))
