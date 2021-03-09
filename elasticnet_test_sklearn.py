from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
import sys
import os
import numpy as np

#input_folder = sys.argv[1]
input_folder = "data/training"
adult_age = 20 #Humans

def median_absolute_difference(y, y_hat):
    return np.median(np.abs(y-y_hat))

def inverseF(age):
    if age < 0:
        return (1. + adult_age)*np.exp(age) - 1.
    else:
        return (1. + adult_age)*age + adult_age



y_list = []
with open("data/testing/GSE38873.labels") as lbl_file:
    for line in lbl_file:
        age, Fage = line.rstrip().split(',')
        y_list.append(age)

id_dict = {}
with open("data/training/methylation_ids.txt") as ids_file:
    for line in ids_file:
        split_line = line.rstrip().split(',')
        id_val = int(split_line[1])
        cpg_id = split_line[0]
        id_dict[cpg_id] = id_val

indices = []
with open("data/trained_female/important_sk_variables.txt") as vars_file:
    for line in vars_file:
        variable = line.rstrip().split(',')[0]
        indices.append(id_dict[variable])

#y_valid = np.array(y_list, dtype=np.float)
X_valid = np.genfromtxt('data/testing/GSE38873.csv', delimiter=',')
#USE BELOW IF IMPORTANT betas and intercept are selected
X_valid = X_valid[:,indices]
scaler = StandardScaler()
X_valid = scaler.fit_transform(X_valid)
beta = np.load('data/trained_female/enet_important_betas.npy')
intercept = np.load('data/trained_female/enet_important_intercept.npy')


regr = ElasticNet(random_state=0, alpha=0.5, l1_ratio=0.02255706, normalize=False,
                    fit_intercept=True, max_iter=5000)
regr.coef_ = beta
regr.intercept_ = intercept
pred_valid = regr.predict(X_valid)

y_hat = []
for i in range(len(pred_valid)):
    tmp = inverseF(pred_valid[i])
    y_hat.append(tmp)
    print(f"{tmp},{y_list[i]}")

def median_absolute_difference(y, y_hat):
    return np.median(np.abs(y-y_hat))

def mean_squared_error(y, y_hat):
    delta = y_hat - y
    return delta.dot(delta)/len(y)

y = np.array(y_list, dtype=np.float)
y_h = np.array(y_hat, dtype=np.float)
mad = median_absolute_difference(y, y_h)
print(f"MAD: {mad}")
mse = mean_squared_error(y, y_h)
print(f"MSE: {mse}")
