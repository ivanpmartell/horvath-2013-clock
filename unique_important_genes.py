gene_set = set()
with open('data/trained_all/important_sk_genes.bed') as bed_genes_file:
    for line in bed_genes_file:
        split_line = line.rstrip().split('\t')
        gene_set.add(split_line[9])

with open('data/trained_all/important_sk_genes.txt', 'w') as txt_genes_file:
    for gene in gene_set:
        txt_genes_file.write(f"{gene}\n")