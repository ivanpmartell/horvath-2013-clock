from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
import sys
import os
import numpy as np

#input_folder = sys.argv[1]
input_folder = "data/training"

def get_all_training_files_in_folder(directory):
    files = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            if item.endswith("_female.csv"):
                files.append((item_path, item_path[:-4] + ".labels"))
    return files

train_files = get_all_training_files_in_folder(input_folder)
y_list = []
X_list = []
for csv_f, lbl_f in train_files:
    with open(lbl_f) as lbl_file:
        for line in lbl_file:
            age, Fage = line.rstrip().split(',')
            y_list.append(Fage)
    with open(csv_f) as csv_file:
        X = np.genfromtxt(csv_file, dtype=float, delimiter=',')
        X_list.append(X)
X_train = np.concatenate(X_list)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
y_train = np.array(y_list, dtype=np.float)


regr = ElasticNet(random_state=0, alpha=0.5, l1_ratio=0.02255706, normalize=False,
                    fit_intercept=True, max_iter=10000)
regr.fit(X_train, y_train)

np.save('data/trained_female/enet_sk_betas.npy', regr.coef_)
np.save('data/trained_female/enet_sk_intercept.npy', regr.intercept_)

