# horvath-2013-clock

Steps:

1 Run GEOquery.seq to download accession samples for both training and testing datasets.

2 Run common_methylation_ids.seq to get common ids from all accession samples.

3 Run preprocessing.seq on each accession to create the training files.

4 Run elasticnet_train.seq with the folder containing your training files.

5 Check learned coefficients by running fast_coef_check.seq and choose the appropriate precision for selecting important coefficients.

6 Use check_betas.seq to get the important coefficients from the learned model with the previously chosen precision.

7 Test the model on the testing dataset using elasticnet_test.seq with the important coefficients only.

8 With the bed file of important CpG sites and UCSC genes bed file, run bedtools closest (get_closest_genes.sh) to find the closest genes to the cpG sites. 

9 Run unique_important_genes.seq to select the important genes created by bedtools in UCSC refSeq accession format.

10 (Optional) Use http://biotools.fr/human/refseq_symbol_converter to convert refSeq accessions to HUGO gene nomenclature symbol (HGNC)

The project contains a Seq helper class for dealing with SOFT text format from NCBI accessions in soft.seq. It also contains a script to validate the inverse function for age in the case a custom function that transforms age is needed.