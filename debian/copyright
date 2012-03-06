Copyright 2010,2011 Brown University, Providence, RI.

                         All Rights Reserved

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose other than its incorporation into a
commercial product is hereby granted without fee, provided that the
above copyright notice appear in all copies and that both that
copyright notice and this permission notice appear in supporting
documentation, and that the name of Brown University not be used in
advertising or publicity pertaining to distribution of the software
without specific, written prior permission.

BROWN UNIVERSITY DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ANY
PARTICULAR PURPOSE.  IN NO EVENT SHALL BROWN UNIVERSITY BE LIABLE FOR
ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
http://cs.brown.edu/people/braphael/software.html

README file for Dendrix:

Software for De novo discovery of mutated driver pathways

Version: 0.1
Version Date: July 1 2011

contact: dendrix@cs.brown.edu

-------------------------------------------------------------------------------
Requirements to run Dendrix:
1. Python

-------------------------------------------------------------------------------

USAGE ======================================================

1. Build the mutation matrix file: the mutation matrix must contain one line
per patient. The first token is the patientID, then the IDs of mutated
genes/groups follow, separated by spaces.

2. Run Dendrix: 

	* python Dendrix.py mutations_file K minFreqGene number_iterations analyzed_genes_file num_exper step_length

	INPUT files:
	* mutations_file: input file with mutation matrix (format above)
	* K: size of the sets to be sampled
        * minFreqGene: minimum frequency of mutation for a gene/group to be considered in the analysis
        * number_iterations: number of iterations of the MCMC
        * analyzed_genes_file: file with list of analyzed genes, one per line
        * num_exper: number of times the experiment is going to be run. For each experiment, a random solution is used as initial state for the MCMC
        * step_length: number of iterations of the MCMC between two samples

	OUTPUT files:
	* sets_frequencyOrder_experiment$j.txt: for each experiment, the 1000 sets sampled with highest frequency by the MCMC. One set per line, and the corresponding weight is reported. $j denote the number of the experiment (starting from 0).
	* sets_weightOrder_experiment$j.txt: for each experiment, the 1000 sets of highest weight sampled by the MCMC. One set per line, and the corresponding weight is reported. $j denote the number of the experiment (starting from 0).

EXAMPLE

python Dendrix.py example/mutation_matrix.txt 3 1 1000000 example/analyzed_genes.txt 1 1000

Runs the MCMC for 1000000 iterations, sampling sets of size 3 every 1000
iterations. Produces two files  (since 1 experiment is run):
sets_frequencyOrder_experiment0.txt and sets_weightOrder_experiment0.txt. 
The first lines of set_frequencyOrder_experiment0.txt look like the following:

13	FGFR2	PTEN	RB1	48
10	FGFR2	MTAP	PTEN	47
10	FGFR2	PTCH1	PTEN	47
10	MTAP	PTEN	TRIM2	47
10	MTAP	PDGFRA	PTEN	47

In each line: the first number is the number of times the set has been
sampled; the following K tokens are the genes in the set; the last number is
the weight of the set.

The first lines of set_wrightOrder_experiment0.txt file look like the following:

48	FGFR2	PTEN	RB1	13
47	FGFR2	MTAP	PTEN	10
47	FGFR2	PTCH1	PTEN	10
47	MTAP	PTEN	TRIM2	10
47	MTAP	PDGFRA	PTEN	10

The format is as the set_frequencyOrder_experiment0.txt file, but with the
first and last token switched.

NOTES:

- what we call "genes" can be any group of mutations
- the analyzed_genes_file can be used to remove genes from the analysis without
  the need of modifying the mutation matrix.
- example/ contains the small example described above, and two mutations tables assembled from real data:
  a) GBM_mutationsAndCN.txt: assembled from somatic mutations (single
nucleotide mutations and small indels) and focal copy number aberrations
described in: The Cancer Genome Atlas Network. (2008) Comprehensive genomic
characterization defines human glioblastoma genes and core pathways.
Nature 455, 1061-1068. (The 7 hypermutated samples have been removed from
the mutation table.)
  b) Lung_mutations.txt: assembled from somatic mutations (single nucleotide
mutations and small indels) described in: L. Ding et al. (2008) Somatic
mutations affect key pathways in lung adenocarcinoma. Nature 455, 1069-1075.


REFERENCES:

If you use Dendrix in your research, please cite:

F. Vandin, E. Upfal, and B.J. Raphael. (2011) De novo Discovery of Mutated
Driver Pathways in Cancer. Genome Research, in press.

WEBSITE:
http://cs.brown.edu/people/braphael/software.html
