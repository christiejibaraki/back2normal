import os
from util import basic_io

list_of_desired_cols = ['Bars']

ground_truth_file_path = os.path.join("resources", "GroundTruth")
for dirName, subdirList, fileList in os.walk(ground_truth_file_path):
    for fname in fileList:
        data = basic_io.read_csv_to_list(os.path.join(ground_truth_file_path, fname))
        header = data.pop(0)
        header_2 = data.pop(0)
        header[0] = header_2[0]# add 'Timestamp Date' to header
        print(fname)
        print(header)


