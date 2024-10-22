import sys
import os
import numpy as np

directory = sys.argv[1]
precision = int(sys.argv[2])
beta = np.load(os.path.join(directory, "enet_sk_betas.npy"))
intercept = np.load(os.path.join(directory, "enet_sk_intercept.npy"))
beta_rounded = np.round_(beta, decimals=precision)
intercept_rounded = np.round_(intercept, decimals=precision)
print(str(sum(beta_rounded != 0)) + " Variables and Neglected " +  str(sum(beta_rounded == 0)) + " Variables")
print(str(intercept_rounded) + " Intercept")
with np.printoptions(threshold=np.inf):
    print(intercept)
    print(beta)


