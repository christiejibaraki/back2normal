import os
import pandas as pd
import re

GROUND_TRUTH_FILE_PATH = os.path.join("resources", "GroundTruth")


def get_combined_ground_truth_data():
    """
    Process GroundTruth zipcode files and merge into single dataframe
    If orig zipcode level file does not contain a column,
        the value should be zero

    :return: merged_data (pandas DataFrame)
    """
    df_list = []

    for dirName, subdirList, fileList in os.walk(GROUND_TRUTH_FILE_PATH):
        for fname in fileList:
            if '.csv' in fname:
                df = pd.read_csv(os.path.join(GROUND_TRUTH_FILE_PATH, fname))
                # remove index line
                df = df.drop([0])
                # create time stamp header
                df.rename(columns={"Category": "Time Stamp"}, inplace=True)
                df = df.apply(pd.to_numeric, errors='ignore')
                # create zip code column + header
                df.insert(1, "ZIP Code", fname.split(".")[0])
                # append to dataframe list
                df_list.append(df)

    # merged groundtruth dataframe
    merged_data = pd.concat(df_list)
    merged_data.reset_index(drop=True, inplace=True)
    standard_col_names = create_col_name_map(merged_data.columns)
    merged_data.rename(columns=standard_col_names, inplace=True)
    return merged_data


def create_col_name_map(col_names):
    """
    create dict with key: orig col name, val formated col nam
    :param col_names:
    :return:
    """
    return {x: clean_col_name(x) for x in col_names}


def clean_col_name(col_name_str):
    """
    create standard column name from descriptive string
    
    replace non alphanumeric chars with whitespace
    remove multiple whitespace
    convert whitespace to underscore
    
    :param col_name_str: col name with spaces and special chars
    :return: standard col name
    """""
    clean_str = re.sub('[^0-9a-zA-Z]+', ' ', col_name_str)
    clean_str = re.sub("\s\s+", " ", clean_str)
    col_name = re.sub(" ", "_", clean_str).upper()
    return col_name
