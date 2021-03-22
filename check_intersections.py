import sys
char_of_interest = sys.argv[1]
oncogene_set = set()
with open("data/oncogene_human.txt") as onc_file:
        #Ignore first line of the file
        next(onc_file)
        for line in onc_file:
            split_line = line.rstrip().split('\t')
            aliases = split_line[2]
            for alias in aliases.split('|'):
                oncogene_set.add(alias.upper())

GenesofInterest_genes_set = set()
with open(f"data/trained_{char_of_interest}/important_sk_gene_names.txt") as genes_file:
    for line in genes_file:
        g = line.rstrip()
        all_genes_set.add(g.upper())

CGofInterest_set = set()
with open(f"data/trained_{char_of_interest}/important_sk_variables.txt") as genes_file:
    for line in genes_file:
        cg = line.rstrip().split(',')[0]
        CGofInterest_set.add(cg.lower())

cg_horvath_set = set()
with open("data/horvath_cgs.txt") as genes_file:
    #Ignore first line of the file
    next(genes_file)
    for line in genes_file:
        cg = line.split(',')[0].rstrip()
        cg_horvath_set.add(cg.lower())
commonWithHorvath = CGofInterest_set.intersection(cg_horvath_set)

with open(f"data/trained_{char_of_interest}/important_sk_genes.bed") as translation_file:
    for line in translation_file:
        split_line = line.rstrip().split('\t')
        cgsite = split_line[3]
        gene_nm = split_line[9]
        tmp_set = set()
        tmp_set.add(cgsite)
        if len(tmp_set.intersection(commonWithHorvath)) > 0:
            print(gene_nm)