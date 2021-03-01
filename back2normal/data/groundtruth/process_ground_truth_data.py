import os
import pandas as pd
from util import basic_io

ground_truth_file_path = os.path.join("resources", "GroundTruth")
df_list = []

for dirName, subdirList, fileList in os.walk(ground_truth_file_path):
    fileList.remove(".DS_Store")
    for fname in fileList:
        df = pd.read_csv("resources/GroundTruth/" + fname)
        #remove index line
        df = df.drop([0])
        #create time stamp header
        df.rename(columns = {"Category": "Time Stamp"})
        #create zip code column + header
        df.insert(1, "ZIP Code", fname.split(".")[0])
        #append to dataframe list
        df_list.append(df)

#merged groundtruth dataframe
gt_df = pd.concat(df_list)