import pandas as pd
import build_db
from core.data import dbclient
from core.util import basic_io
from core.data import data_transformations


def get_demographic_data(output_file):
    db = dbclient.DBClient()
    query = f"select * from {build_db.CENSUS_TBL}"
    census_df = pd.read_sql_query(query, db.conn)
    demographic_data = []
    for i, zipc in enumerate(census_df.ZIPCODE):
        for cat in census_df.columns:
            demographic_data.append({"ZIPCODE": zipc, "CATEGORY": cat, 
                                     "VALUE": census_df[cat][i]})
    #basic_io.write_dict_to_json(output_file, demographic_data)


def get_vaccine_data(output_file):
    db = dbclient.DBClient()
    query = f"select * from {build_db.VACC_TBL}"
    vacc_df = pd.read_sql_query(query, db.conn)
    vacc_records = vacc_df.to_dict(orient='records')
    basic_io.write_dict_to_json(output_file, vacc_records)


def get_covid_and_vaccine_data(output_file):
    db = dbclient.DBClient()

    query = (f"select case_data.{data_transformations.STD_ZIP_COL_NAME},"
             f" case_data.{data_transformations.STD_DATE_COL_NAME},"
             f" vacc_data.{data_transformations.STD_ZIP_COL_NAME} ZIPB,"
             f" vacc_data.{data_transformations.STD_DATE_COL_NAME} DATEB,"
             f" case_data.AVG7DAY_confirmed_cases,"
             f" vacc_data.AVG7DAY_total_doses_daily, vacc_data.AVG7DAY_vaccine_series_completed_daily"
             f" from {build_db.CASE_TBL} case_data left join {build_db.VACC_TBL} vacc_data"
             f" on case_data.{data_transformations.STD_ZIP_COL_NAME} = vacc_data.{data_transformations.STD_ZIP_COL_NAME}"
             f" and case_data.{data_transformations.STD_DATE_COL_NAME} = vacc_data.{data_transformations.STD_DATE_COL_NAME}"
             f" where case_data.{data_transformations.STD_ZIP_COL_NAME} is not null")
    case_and_vacc_df = pd.read_sql_query(query, db.conn)
    case_and_vacc_df['AVG7DAY_total_doses_daily'].fillna(0, inplace=True)
    case_and_vacc_df['AVG7DAY_vaccine_series_completed_daily'].fillna(0, inplace=True)
    records = case_and_vacc_df.to_dict(orient='records')
    basic_io.write_dict_to_json(output_file, records)


def get_groundtruth_data(output_file):
    db = dbclient.DBClient()
    query = f"select * from {build_db.FOOT_TRAFF_TBL}"
    groundtruth_df = pd.read_sql_query(query, db.conn)
    gt_records = groundtruth_df.to_dict(orient='records')
    basic_io.write_dict_to_json(output_file, gt_records)
