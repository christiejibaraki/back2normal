import os
import pandas as pd

GROUND_TRUTH_FILE_PATH = os.path.join("resources", "GroundTruth")


def get_combined_ground_truth_data():
    df_list = []

    for dirName, subdirList, fileList in os.walk(GROUND_TRUTH_FILE_PATH):
        for fname in fileList:
            if '.csv' in fname:
                df = pd.read_csv(os.path.join(GROUND_TRUTH_FILE_PATH, fname))
                # remove index line
                df = df.drop([0])
                # create time stamp header
                df.rename(columns={"Category": "Time Stamp"}, inplace=True)
                # create zip code column + header
                df.insert(1, "ZIP Code", fname.split(".")[0])
                # append to dataframe list
                df_list.append(df)

    # merged groundtruth dataframe
    return pd.concat(df_list)
