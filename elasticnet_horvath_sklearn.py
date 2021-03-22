from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
import sys
import os
import numpy as np

input_file = sys.argv[1]
input_file_labels = input_file[:-4] + ".labels"
adult_age = 20 #Humans

def median_absolute_difference(y, y_hat):
    return np.median(np.abs(y-y_hat))

def inverseF(age):
    if age < 0:
        return (1. + adult_age)*np.exp(age) - 1.
    else:
        return (1. + adult_age)*age + adult_age



y_list = []
with open(input_file_labels) as lbl_file:
    for line in lbl_file:
        age, Fage = line.rstrip().split(',')
        y_list.append(age)

betas = []
with open("data/horvath_cgs.txt") as ids_file:
    intercept_line = next(ids_file)
    intercept_num = float(intercept_line.split(',')[2])
    intercept = np.array([intercept_num])
    for line in ids_file:
        split_line = line.rstrip().split(',')
        beta_num = float(split_line[2])
        betas.append(beta_num)
beta = np.array(betas)

#y_valid = np.array(y_list, dtype=np.float)
X_valid = np.genfromtxt(input_file, delimiter=',')
scaler = StandardScaler()
X_valid = scaler.fit_transform(X_valid)

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
