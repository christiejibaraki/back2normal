
class SodaData:

    def __init__(self, dataset_name, table_name, identifier,
                 desired_attr_lst,
                 group_by=None,
                 where=None):

        self.dataset_name = dataset_name
        self.table_name = table_name
        self.identifier = identifier
        self.base_url = f"https://data.cityofchicago.org/resource/{identifier}.json"
        self.desired_attr_lst = desired_attr_lst
        self.group_by_lst = group_by
        self.where_lst = where
        self.request_url = self._build_soql_query()

    def _build_soql_query(self):
        
        query =  f"?$query=SELECT {', '.join(self.desired_attr_lst)} "
        if self.where_lst:
            #Multiple clauses AND
            query += f"WHERE {'AND '.join(self.where_lst)} "
        if self.group_by_lst:
            query += f"GROUP BY {', '.join(self.group_by_lst)}"

        return self.base_url + query

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
                          