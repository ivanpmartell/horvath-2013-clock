import os
import sys
import math
from soft import SampleSoft

adult_age = 20 #Humans
dir = sys.argv[1]
geo_accession = sys.argv[2]
methylation_ids_file = sys.argv[3]
char_of_interest = sys.argv[4]
# input in lowercase!
char_1, char_2 = sys.argv[5].split(',')

def get_all_files_in_directory(directory, accession):
    full_dir = os.path.join(directory, accession)
    files = []
    for item in os.listdir(full_dir):
        item_path = os.path.join(full_dir, item)
        if os.path.isfile(item_path):
            files.append(item_path)
    return files

#Use this if all metadata is formatted the same
def get_all_folders_in_directory(directory):
    folders = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            folders.append(item)
    return folders

def F(age):
    if age <= adult_age:
        return math.log(age+1.)-math.log(adult_age+1.)
    else:
        return (age-adult_age)/(adult_age+1.)

def _list_str(lst):
    n = len(lst)
    if n == 0:
        return ""
    else:
        y = [str(lst[0])]
        for i in range(1, n):
            y.append(",")
            y.append(str(lst[i]))
        y.append("\n")
        return ''.join(y)

id_dict = dict()
with open(methylation_ids_file) as methylids_file:
    next(methylids_file)
    for line in methylids_file:
        arrid, cgid = line.rstrip().split(',')[0:2]
        id_dict[cgid] = int(arrid)

#for geo_accession in get_all_folders_in_directory(dir):
csv_file = open(f"data/training/{geo_accession}_{char_of_interest}-{char_1}.csv", 'w')
out_file = open(f"data/training/{geo_accession}_{char_of_interest}-{char_1}.labels", 'w')
csv2_file = open(f"data/training/{geo_accession}_{char_of_interest}-{char_2}.csv", 'w')
out2_file = open(f"data/training/{geo_accession}_{char_of_interest}-{char_2}.labels", 'w')
for sample in get_all_files_in_directory(dir, geo_accession):
    print(f"Processing file: {sample}")
    soft_data = SampleSoft()
    for s_acc in soft_data.load_file(sample):
        data, age, char = soft_data.get_data(id_dict, s_acc, char_of_interest)
        if age == -1:
            print("Skipping...")
            continue
        if char.lower() == char_1:
            out_file.write(f"{age},{F(age)}\n")
            csv_file.write(_list_str(data))
        elif char.lower() == char_2:
            out2_file.write(f"{age},{F(age)}\n")
            csv2_file.write(_list_str(data))
        else:
            print(f"WARNING: UNKNOWN CHARACTERISTIC {char}")
csv_file.close()
out_file.close()
csv2_file.close()
out2_file.close()