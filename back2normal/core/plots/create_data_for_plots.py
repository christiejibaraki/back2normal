import pandas as pd
import build_db
from core.data import dbclient
from core.util import basic_io


def get_demographic_data(output_file):
    db = dbclient.DBClient()
    query = f"select * from {build_db.CENSUS_TBL}"
    census_df = pd.read_sql_query(query, db.conn)
    demographic_data = []
    for i, zipc in enumerate(census_df.ZIPCODE):
        for cat in census_df.columns:
            demographic_data.append({"ZIPCODE": zipc, "CATEGORY": cat, 
                                     "VALUE": census_df[cat][i]})
    basic_io.write_dict_to_json(output_file, demographic_data)

get_demographic_data("demographic_data.js")


