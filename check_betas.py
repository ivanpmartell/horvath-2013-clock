import numpy as np

beta = np.load('data/trained/enet_sk_betas.npy')
intercept = np.load('data/trained/enet_sk_intercept.npy')

beta_rounded = np.round_(beta, decimals=10)
intercept_rounded = np.round_(intercept, decimals=5)

print(str(sum(beta_rounded != 0)) + " Variables and Neglected " +  str(sum(beta_rounded == 0)) + " Variables")
print(str(intercept_rounded) + " Intercept")
with np.printoptions(threshold=np.inf):
    print(intercept)
    print(beta)

inv_id_dict = {}
with open("data/training/methylation_ids.txt") as ids_file:
    for line in ids_file:
        split_line = line.rstrip().split(',')
        id_val = int(split_line[1])
        cpg_id = split_line[0]
        inv_id_dict[id_val] = cpg_id

non_zeros = np.nonzero(beta_rounded)[0]

important_vars = {}
max_beta = 0
min_beta = 9999
with open("data/trained/important_sk_variables.txt", 'w') as vars_file:
    for i in range(len(non_zeros)):
        if beta[non_zeros[i]] < min_beta:
            min_beta = beta[non_zeros[i]]
        if beta[non_zeros[i]] > max_beta:
            max_beta = beta[non_zeros[i]]
        important_vars[inv_id_dict[non_zeros[i]]] = beta[non_zeros[i]]
        vars_file.write(f"{inv_id_dict[non_zeros[i]]},{beta_rounded[non_zeros[i]]}\n")

with open("data/trained/important_sk_variables.bed", 'w') as important_file:
    important_file.write(f"chrom\tchromStart\tchromEnd\tname\tscore\tstrand\n")
    with open("data/cgids_to_locations.csv") as loc_file:
        #Ignore first line
        next(loc_file)
        for line in loc_file:
            split_line = line.rstrip().split(',')
            try:
                score = int((important_vars[split_line[4]] - min_beta) / (max_beta - min_beta) * 1000)
                important_file.write(f"{split_line[1]}\t{split_line[2]}\t{split_line[3]}\t{split_line[4]}\t{score}\t{split_line[6]}\n")
            except:
                continue

#np.save('enet_important_betas.npy', beta_rounded)
#np.save('enet__important_intercept.npy', intercept_rounded)