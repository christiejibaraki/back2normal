import os
import pandas as pd
from data import data_transformations


def get_zillow_zori_data():
    desired_zip = data_transformations.get_chicago_zipcodes()
    all_rents = pd.read_csv(os.path.join("resources", "Zillow",
                                         "Zip_ZORI_AllHomesPlusMultifamily_SSA (1).csv"))
    chicago_area_rents = all_rents[all_rents["MsaName"] == "Chicago, IL"]
    chicago_city_rents = all_rents[all_rents["RegionName"].isin(desired_zip)]
    return chicago_area_rents, chicago_city_rents
