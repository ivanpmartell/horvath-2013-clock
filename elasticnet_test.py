import numpy as np

adult_age = 20 #Humans

def predict(X, coef_, intercept_): 
    y = np.dot(X, coef_)
    y += intercept_*np.ones(len(y))
    return y

#def inverseF(age):
#    return (age*adult_age) + age + adult_age

def inverseF(age):
    if age < 0:
        return (1. + adult_age)*np.exp(age) - 1.
    else:
        return (1. + adult_age)*age + adult_age

y_list = []
with open("data/training/GSE41826_male.labels") as lbl_file:
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
with open("data/trained/important_sk_variables.txt") as vars_file:
    for line in vars_file:
        variable = line.rstrip().split(',')[0]
        indices.append(id_dict[variable])

#y_valid = np.array(y_list, dtype=np.float)
X_valid_norm = np.genfromtxt('data/training/GSE41826_male.csv', delimiter=',')
X_valid_norm = X_valid_norm[:,indices]

beta = np.load('data/trained/enet_sk_betas.npy')
beta = beta[indices]
intercept = np.load('data/trained/enet_sk_intercept.npy')
#beta = np.load('enet_important_betas.npy')
#beta = beta[indices]
#intercept = np.load('enet__important_intercept.npy')


pred_valid = predict(X_valid_norm, beta, intercept)
y_hat = []
for i in range(len(pred_valid)):
    tmp = inverseF(pred_valid[i])
    y_hat.append(tmp)
    print(tmp)

def median_absolute_difference(y, y_hat):
    return np.median(np.abs(y-y_hat))

print(median_absolute_difference(np.array(y_list, dtype=np.float),np.array(y_hat, dtype=np.float)))