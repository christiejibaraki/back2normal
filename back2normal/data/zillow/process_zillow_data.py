import os
import pandas as pd
from util import basic_io

desired_zip = ["60661", "60655", "60607", "60629", "60636", "60633", "60643", "60602", "60639", "60628", "60624", "60625", "60612", "60647", "60611", "60621", "60644", "60660", "60616", "60652", "60638", "60619", "60637", "60626", "60606", "60645", "60654", "60651", "60646", "60631", "60630", "60827", "60657", "60707", "60617", "60653", "60604", "60623", "60634", "60610", "60659", "60605", "60614", "60641", "60666", "60618", "60601", "60609", "60640", "60613", "60603", "60656", "60608", "60620", "60632", "60649", "60622", "60642", "60615"]

all_rents = pd.read_csv("resources/Zillow//Zip_ZORI_AllHomesPlusMultifamily_SSA (1).csv")
chicago_area_rents = all_rents[all_rents["MsaName"] == "Chicago, IL"]
chicago_city_rents = all_rents[all_rents["RegionName"].isin(desired_zip)]