import numpy as np

adult_age = 20 #Humans

def predict(X, coef_, intercept_): 
    y = np.dot(X, coef_)
    y += intercept_*np.ones(len(y))
    return y

def inverseF(age):
    if age <= adult_age:
        return np.log(age+1.)-np.log(adult_age+1.)
    else:
        return (age-adult_age)/(adult_age+1.)

y_list = []
with open("output.labels") as lbl_file:
    for line in lbl_file:
        age, Fage = line.rstrip().split(',')
        y_list.append(Fage)
y_train = np.array(y_list, dtype=np.float)
X_valid_norm = np.genfromtxt('output.csv', delimiter=',')

beta = np.load('enet_betas.npy')
intercept = np.load('enet_intercept.npy')

pred_valid = predict(X_valid_norm, beta, intercept)
print(inverseF(pred_valid))