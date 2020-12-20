import numpy as np

beta = np.load('data/trained/enet_new_betas.npy')
intercept = np.load('data/trained/enet_new_intercept.npy')

beta_rounded = np.round_(beta, decimals=41)
intercept_rounded = np.round_(intercept, decimals=41)

print(str(sum(beta_rounded != 0)) + " Variables and Neglected " +  str(sum(beta_rounded == 0)) + " Variables")
print(str(intercept_rounded) + " Intercept")
with np.printoptions(threshold=np.inf):
    print(intercept)
    print(beta)