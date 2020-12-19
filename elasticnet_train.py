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
                if item.startswith("GSE4"):
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
#Dimensions of the normalized data
N = X_train.shape[0]
D = X_train.shape[1]
#Initialize the gradient descent and learning rate
beta = np.random.randn(D) / np.sqrt(D)
learning_rate = 0.000000001
#L1 regularization term alpha
l1 = 0.5
#L2 regularization term lambda
l2 = 0.02255706

#TODO: Improve elasticnet training algo to do batches of 10
for i in range(500000):
    Yhat = X_train.dot(beta)
    delta = Yhat - y_train
    beta = beta - (learning_rate *(X_train.T.dot(delta) + l1*np.sign(beta) + l2*2*beta))
    mse = delta.dot(delta)/N
    print(mse)
intercept = np.sum(y_train - np.dot(X_train, beta))/N

np.save('data/trained/enet_betas.npy', beta)
np.save('data/trained/enet_intercept.npy', intercept)

#print(str(sum(beta != 0)) + " Variables and Neglected " +  str(sum(beta == 0)) + " Variables")