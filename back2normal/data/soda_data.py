
class SodaData:

    def __init__(self, dataset_name, table_name, identifier, desired_attr_lst=None):

        self.dataset_name = dataset_name
        self.table_name = table_name
        self.identifier = identifier
        self.base_url = f"https://data.cityofchicago.org/resource/{identifier}.json"

        # if empty or None, will use all available fields
        self.desired_attr_lst = desired_attr_lst

datasets = {}

############################################
######## COVID-19 Vaccinations by ZIP Code
############################################

# https://dev.socrata.com/foundry/data.cityofchicago.org/553k-3xzc

datasets["COVID-19 Vaccinations by ZIP Code"] = \
    SodaData("COVID-19 Vaccinations by ZIP Code",
             "VACCINATION_BY_ZIP",
             "553k-3xzc"
             )

############################################
######## Traffic Crashes - Crashes
############################################

# https://dev.socrata.com/foundry/data.cityofchicago.org/85ca-t3if

datasets["Traffic Crashes - Crashes"] = \
    SodaData("Traffic Crashes - Crashes",
             "TRAFFIC_CRASHES",
             "85ca-t3if",
             ["CRASH_DATE", "POSTED_SPEED_LIMIT", "TRAFFIC_CONTROL_DEVICE",
             "FIRST_CRASH_TYPE", "PRIM_CONTRIBUTORY_CAUSE",
             "STREET_NO", "STREET_DIRECTION", "STREET_NAME",
             "MOST_SEVERE_INJURY", "CRASH_HOUR",
             "LATITUDE", "LONGITUDE", "LOCATION"])
