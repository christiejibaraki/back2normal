
class SodaData:

    def __init__(self, dataset_name, table_name, identifier,
                 desired_attr_lst,
                 group_by = None,
                 where = None):

        self.dataset_name = dataset_name
        self.table_name = table_name
        self.identifier = identifier
        self.base_url = f"https://data.cityofchicago.org/resource/{identifier}.json"
        self.request_url = self._build_soql_query()

        # if empty or None, will use all available fields
        self.desired_attr_lst = desired_attr_lst

    def _build_soql_query(self):
        
        query =  f"select {', '.join(select_field_list)} "

        # # if select_field_list not empty or None, create select query
        # if not not select_field_list:  # could this just be if select_field_list:
        #     select_statement = f"?$select={', '.join(select_field_list)}"
        #     request_url = request_url + select_statement
        #     if not not group_by_field_list:
        #         # I nested this because there can only be a group_by query if
        #         # there is also a select query that specifies an aggregation method
        #         # group query documentation: https://dev.socrata.com/docs/queries/group.html
        #         # should add some error handling
        #         group_statement = f"&$group={', '.join(group_by_field_list)}"
        #         request_url = request_url + group_statement


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


