# Predicting age: DNA methylation clock differences between sexes

Summarized steps:

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

Scripts details:

1 GEOquery.seq
  
  This script downloads all samples contained in a Gene Expression Omnibus (GEO) Series as `Simple Omnibus Format in Text' (SOFT) format, obtaining its metadata and table data for use in subsequent steps. Each GEO Series (GSE) is given a folder with all samples of that series contained within it.
  
2 common_methylation_ids.seq
  
  This script creates a set of all common CpG sites in different datasets. Since each of the GEO Series contain different CpG sites, this will create a set of all CpG sites that appear in every sample from the GEO Series. This is achieved using set intersection for the CpG sites in the first sample of each series. It is assumed that every sample will contain the same CpG sites within the series, as most samples within an experiment are done using the same equipment.
  
3 preprocessing.seq
  
  This script utilizes a Seq helper class contained in another file (soft.seq). The helper class deals with the SOFT format from NCBI's GEO accession viewer. For now, this script only works for tables from Illumina's methylation profiling by array. This includes both Infinium 27k and 450k Human Methylation Beadchip.
  
  Here, the script scans for all the GSE folders and creates a csv file containing the beta values of the Illumina assay as a matrix. Every row corresponds to a sample, while the columns correspond to a specific CpG site from the set of common CpG sites. The script also creates a label file containing the age of the individual from which the sample was obtained. Additionally, we separated the created data as male and female for further processing.
  
4 elasticnet_train.seq OR elasticnet_train_sklearn.seq
  
  These scripts create a linear regression model using Elastic net regularization. The elasticnet_train.seq script is a reimplementation of the Elastic net training algorithm using NumPy, while elasticnet_train_sklearn.seq uses Scikit-learn's open source algorithms with more functionality than my naive reimplementation, including data normalization. Both scripts save the learned coefficients using NumPy's save function, which creates a binary file that can be easily loaded by NumPy afterwards.
  
  
  Elastic net minimizes a loss function that includes L1 and L2 regularization using gradient descent. More information on Elastic net and its equation can be found on page 458 of Machine Learning: A probabilistic perspective, where $\boldsymbol{y} = F(\alpha)$ is the vector of transformed ages for all samples. $\boldsymbol{w}$ is the vector of coefficients that will be learned during gradient descent, including the intercept. $\boldsymbol{X}$ is the vector of beta values for the common CpG sites selected previously; $\lambda_1 \ge 0$ and $\lambda_2 \ge 0$ are user specified hyperparameters regarding the amount of $L_1$ and $L_2$ regularization that should be used. Horvath specified $\alpha_1 = 0.5$ and $\alpha_2 = 0.02255706$ after applying 10 fold cross validation on his complete training data.
  
5 fast_coef_check.seq
  
  This is a quick script made to examine the learned coefficients of the trained linear model. It allows for the selection of the numerical precision where a coefficient could be deemed irrelevant. Specifically, it allows a user to test coefficient values by rounding down to a certain precision and returning the amount of non-zero coefficients left.
  
6 check_betas.seq
  
  This uses the previously selected precision to select important (non-zero) coefficient and create four files. The first file contains CpG sites relating to the important coefficients and coefficient values. The second file creates a bed file with the following fields: chromosome, start position, end position, strand, score, and name of the important CpG sites. This bed file will be necessary for bedtools to indicate the closest genes to these sites. Finally, it creates the binary files containing the intercept and important coefficients to be used for testing.

7 elasticnet_test.seq OR elasticnet_test_sklearn.seq
  
  Similar to the training scripts, the testing scripts contain my implementation of the testing algorithm for linear regression in NumPy and Scikit-learn's implementation. It also uses $F^{-1}(\alpha)$ to convert the predicted ages into years, and returns a list of predicted years and true years to visually analyze where the regression model made a mistake. Finally, it returns the Median Absolute Difference (MAD) of the predicted years and true years to compare with Horvath's results.

8 bedtools closest (get_closest_genes.sh)
  
  With the bed files obtained from step 6 and a bed file containing genes and their locations in hg19 reference genome, bedtools associates CpG sites to their closest downstream genes. The genes file can be obtained through UCSC's mySQL database. There are multiple ways of obtaining nearby genes using bedtools, but for reproducibility purposes, we include a bash script with the specific bedtools command that we utilized.
  
9 unique_important_genes.seq
  
  Here, the script takes bedtools output to create a set of unique and important genes. Depending on the genes bed file used in step 8, the genes could be in different naming formats. We utilized a file with UCSC refSeq accession format (NM_, NR_) and thus obtained a list set of genes in this format we denote as refSeq.
  
10 (Optional) biotools (https://biotools.fr/human/refseq_symbol_converter)
  
  If the set of important genes obtained previously are in refSeq format, one can optionally convert the names into HUGO nomenclature gene symbols using biotools web application. This process could be automated or made into a Seq script in the future.

The project contains a Seq helper class for dealing with SOFT text format from NCBI accessions in soft.seq. It also contains a script to validate the inverse function for age in the case a custom function that transforms age is needed.