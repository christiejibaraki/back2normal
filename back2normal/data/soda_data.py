
class SodaData:

    def __init__(self, dataset_name, sql_table_name, identifier,
                 desired_attr_lst,
                 week_avg_attr_lst=None,
                 group_by=None,
                 where=None,
                 limit=None):

        self.dataset_name = dataset_name
        self.sql_table_name = sql_table_name
        self.identifier = identifier

        # constructing api query
        self.base_url = f"https://data.cityofchicago.org/resource/{identifier}.json"
        self.desired_attr_lst = desired_attr_lst
        self.group_by_lst = group_by
        self.where_lst = where
        self.limit = limit

        # api request url
        self.request_url = self._build_soql_query()

        # variables for which weekly averages will be computed
        self.week_avg_attr_list = week_avg_attr_lst

    def _build_soql_query(self):
        """
        builds a soql query to append to base request url.

        :return: (str) socrata api request url
        """

        # soql docs: https://dev.socrata.com/docs/queries/
        
        query =  f"?$query=SELECT {', '.join(self.desired_attr_lst)} "
        if self.where_lst:
            query += f"WHERE {'AND '.join(self.where_lst)} "
        if self.group_by_lst:
            query += f"GROUP BY {', '.join(self.group_by_lst)}"
        if self.limit:
            query += f"LIMIT {self.limit}"

        return self.base_url + query


datasets = {}

############################################
######## COVID-19 Vaccinations by ZIP Code
############################################

# https://dev.socrata.com/foundry/data.cityofchicago.org/553k-3xzc

datasets["COVID-19 Vaccinations by ZIP Code"] = \
    SodaData("COVID-19 Vaccinations by ZIP Code",
             "VACCINATIONS_DAILY",
             "553k-3xzc",
             ["zip_code", "date",
              "total_doses_daily", "total_doses_cumulative",
              "vaccine_series_completed_daily",
              "vaccine_series_completed_percent_population",
              "population"],
             ["total_doses_daily", "vaccine_series_completed_daily"],
             None,
             None,
             5000)
