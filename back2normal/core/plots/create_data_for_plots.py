import pandas as pd
import build_db
from core.data import dbclient
from core.util import basic_io


def get_demographic_data(output_file):
    db = dbclient.DBClient()
    query = f"select * from {build_db.CENSUS_TBL}"
    census_df = pd.read_sql_query(query, db.conn)
    demographic_data = census_df.to_dict(orient="records")
    basic_io.write_dict_to_json(output_file, demographic_data)

get_demographic_data("demographic_data.js")
