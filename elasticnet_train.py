import numpy as np

y_list = []
with open("output.labels") as lbl_file:
    for line in lbl_file:
        age, Fage = line.rstrip().split(',')
        y_list.append(Fage)
y_train = np.array(y_list, dtype=np.float)
X_train_norm = np.genfromtxt('output.csv', delimiter=',')
#Dimensions of the normalized data
N = X_train_norm.shape[0]
D = X_train_norm.shape[1]
#Initialize the gradient descent and learning rate
beta = np.random.randn(D) / np.sqrt(D)
learning_rate = 0.0000001
#L1 regularization term alpha
l1 = 0.5
#L2 regularization term lambda
l2 = 0.02255706
costs_enet = []

intercept = np.sum(y_train - np.dot(X_train_norm, beta))/N
#Let's iterate for 500 times to see after how many iterations it is reaching convergence
for i in range(80000):
    Yhat = X_train_norm.dot(beta)
    delta = Yhat - y_train
    beta = beta - (learning_rate *(X_train_norm.T.dot(delta) + l1*np.sign(beta) + l2*2*beta))
    mse = delta.dot(delta)/N
    print(mse)
    costs_enet.append(mse)
intercept = np.sum(y_train - np.dot(X_train_norm, beta))/N

np.save('enet_betas.npy', beta)
np.save('enet_intercept.npy', intercept)

#print(str(sum(beta != 0)) + " Variables and Neglected " +  str(sum(beta == 0)) + " Variables")