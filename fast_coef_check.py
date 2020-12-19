import numpy as np

beta = np.load('data/trained/enet_sk_betas.npy')
intercept = np.load('data/trained/enet_sk_intercept.npy')

beta_rounded = np.round_(beta, decimals=10)
intercept_rounded = np.round_(intercept, decimals=5)

print(str(sum(beta_rounded != 0)) + " Variables and Neglected " +  str(sum(beta_rounded == 0)) + " Variables")
print(str(intercept_rounded) + " Intercept")