from sklearn.linear_model import ElasticNetCV
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
            if item.endswith(".csv"):
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
y_train = np.array(y_list, dtype=np.float)


regr = ElasticNetCV(cv=5, random_state=0, l1_ratio=[.1, .25, .5, .7, .9, .95, .99, 1])
regr.fit(X_train, y_train)

np.save('data/trained_all/enet_cv_betas.npy', regr.coef_)
np.save('data/trained_all/enet_cv_intercept.npy', regr.intercept_)
print(regr.alpha_)
print(regr.l1_ratio_)
print(regr.n_iter_)
print(regr.mse_path_)