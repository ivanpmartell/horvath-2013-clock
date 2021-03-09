import sys
from soft import get_ids

#Use this function for a complete scan of all files (Very slow)
def get_files_in_subdirectories(base_dir):
    import os
    files = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            for nested_file in os.listdir(item_path):
                file_path = os.path.join (item_path, nested_file)
                if os.path.isfile(file_path):
                    files.append(file_path)
    return files

#Use this function for a scan of first files in each experiment (Fast but assumes all samples have the same cg ids)
def get_first_file_in_directories(base_dir):
    import os
    files = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            file_path = os.path.join (item_path, os.listdir(item_path)[0])
            files.append(file_path)
    return files

directory = sys.argv[1]

ids = set()
for sample in get_first_file_in_directories(directory):
    print(f"Processing file: {sample}")
    curr_ids = set()
    get_ids(sample, curr_ids)
    if len(ids) != 0:
        ids = ids.intersection(curr_ids)
        print(f"Current amount of ids: {len(ids)}")
    else:
        ids = curr_ids

id_dict = dict()
for num, sid in enumerate(ids):
    id_dict[sid] = num


with open("data/training/methylation_ids.txt", 'w') as methylids_file:
    for k, v in id_dict.items():
        methylids_file.write(f"{k},{v}\n")