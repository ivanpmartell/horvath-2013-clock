import numpy as np

beta = np.load('enet_betas.npy')
intercept = np.load('enet_intercept.npy')

beta_rounded = np.round_(beta, decimals=2)
intercept_rounded = np.round_(intercept, decimals=2)

print(str(sum(beta_rounded != 0)) + " Variables and Neglected " +  str(sum(beta_rounded == 0)) + " Variables")
print(str(intercept_rounded) + " Intercept")
with np.printoptions(threshold=np.inf):
    print(intercept)
    print(beta)

inv_id_dict = {}
with open("methylation_ids.txt") as ids_file:
    for line in ids_file:
        split_line = line.rstrip().split(',')
        id_val = int(split_line[1])
        cpg_id = split_line[0]
        inv_id_dict[id_val] = cpg_id

non_zeros = np.nonzero(beta_rounded)[0]
with open("important_variables.txt", 'w') as vars_file:
    for i in range(len(non_zeros)):
        vars_file.write(f"{inv_id_dict[non_zeros[i]]},{beta_rounded[non_zeros[i]]}\n")

#np.save('enet_important_betas.npy', beta_rounded)
#np.save('enet__important_intercept.npy', intercept_rounded)