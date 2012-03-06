#!/usr/bin/env python

#Copyright 2011 Brown University, Providence, RI.

                         #All Rights Reserved

#Permission to use, copy, modify, and distribute this software and its
#documentation for any purpose other than its incorporation into a
#commercial product is hereby granted without fee, provided that the
#above copyright notice appear in all copies and that both that
#copyright notice and this permission notice appear in supporting
#documentation, and that the name of Brown University not be used in
#advertising or publicity pertaining to distribution of the software
#without specific, written prior permission.

#BROWN UNIVERSITY DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
#INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ANY
#PARTICULAR PURPOSE.  IN NO EVENT SHALL BROWN UNIVERSITY BE LIABLE FOR
#ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#http://cs.brown.edu/people/braphael/software.html

import sys
import os

import random
import math

def measure(genes_collection1, genes_collection2):
	#coverage of genes in genes_collection1
	out1 = 0
	#total number of mutations in genes_collection1
	inside1 = 0
	#coverage of genes_collection2
	out2 = 0
	#total number of mutations in genes_collection2
	inside2 = 0
	for sampleID in sample_mutatedGenes:
		genes_in_sample = sample_mutatedGenes[sampleID]
		inside_genes1 = genes_collection1.intersection(genes_in_sample)
		if len(inside_genes1)>0:
			out1 += 1
		num_ig1 = len(inside_genes1)
		inside1 += num_ig1
		inside_genes2 = genes_collection2.intersection(genes_in_sample)
		if len(inside_genes2)>0:
			out2 += 1
		num_ig2 = len(inside_genes2)
		inside2 += num_ig2
	c = 0.5
	return c*float(2*out1 - inside1 - (2*out2 - inside2))

if len(sys.argv)<8:
	print "Usage: python Dendrix.py mutations_file K minFreqGene number_iterations analyzed_genes_file num_exper step_length"
	print "mutations_file: input file with mutation matrix (see README.txt for description)"
	print "K: size of the sets to be sampled"
	print "minFreqGene: minimum frequency of mutation for a gene to be considered in the analysis"
	print "number_iterations: number of iterations of the MCMC"
	print "analyzed_genes_file: file with list of analyzed genes (see README.txt for description)"
	print "num_exper: number of times the experiment is going to be run (see README.txt for description)"
	print "step_length: number of iterations of the MCMC between two samples"
	exit(0)

genes = list()

gene_mutatedSamples = dict()

sample_mut_f = open(sys.argv[1] ,'r')

K = int(sys.argv[2])

mAS_perGene=int(sys.argv[3])

num_iterations = int(sys.argv[4])

analyzed_genes_file = open(sys.argv[5],'r')

all_samples = set()

sample_mutatedGenes = dict()

num_exper = int(sys.argv[6])

step_length = int(sys.argv[7])

print "Load genes..."
for line in analyzed_genes_file:
	v =line.split()
	genes.append(v[0])
	gene_mutatedSamples[v[0]]=set()
analyzed_genes_file.close()

print "Loading mutations..."

for line in sample_mut_f:
	v = line.split("\t")
	sampleID = v[0]
	all_samples.add( sampleID )
	sample_mutatedGenes[sampleID]=set()
	for i in range(len(v) - 1):
		gene = v[i+1].strip("\n")
		if gene in genes:
			if gene not in gene_mutatedSamples:
				gene_mutatedSamples[gene]=set()
			gene_mutatedSamples[gene].add(sampleID)
			sample_mutatedGenes[sampleID].add(gene)

sample_mut_f.close()

sample_numMut = dict()
for sampleID in sample_mutatedGenes:
	tmp_numMut = len(sample_mutatedGenes[sampleID])
	sample_numMut[sampleID] = float(tmp_numMut)

genes_toRemove = set()
for gene in gene_mutatedSamples:
	if len(gene_mutatedSamples[gene])<mAS_perGene:
		genes_toRemove.add(gene)

for gene in genes_toRemove:
	del gene_mutatedSamples[gene]
	genes.remove(gene)

print "Number of genes: "+str(len(genes))

print "Cleaning sample_mutatedGenes table..."
for sampleID in sample_mutatedGenes:
	for gene in genes_toRemove:
		if gene in sample_mutatedGenes[sampleID]:
			sample_mutatedGenes[sampleID].remove(gene)

random.seed()

for exp_n in range(num_exper):
	
	solution=random.sample(genes, K)
	
	genes_set = set(genes)
	
	avg = 0
		
	num_visits = dict()
	
	for itera in range(num_iterations):

		next_gene = random.sample(genes_set,1)
		
		if next_gene[0] in set(solution):
			to_exchange = next_gene
		else:
			to_exchange = random.sample( solution, 1)
		
		next_solution = (set(solution).difference(to_exchange)).union(next_gene)

		expon = measure(next_solution , set(solution))
		
		if expon > 0:
			expon = 0

		prob = min(1.0, math.exp(expon))
		coin = random.random()
		if coin <= prob:
			solution = next_solution
			
		if (itera+1) % step_length ==0:
			frozen_tmp = frozenset(solution)
			if frozen_tmp not in num_visits:
				num_visits[frozen_tmp]=0
			num_visits[frozen_tmp]+=1
			del frozen_tmp
	
	to_sort=list()
	most_visited_file = open("sets_frequencyOrder_experiment"+str(exp_n)+".txt",'w')
	for frozen_tmp in num_visits:
		to_sort.append([num_visits[frozen_tmp], frozen_tmp])
	to_sort.sort()
	most_visited_file.write("Total visited: "+str(len(to_sort))+"\n")
	to_sort_weight = list()
	#only the 1000 most sampled sets are reported
	for i in range(len(to_sort)):
		if i < 1000:
			most_visited_file.write(str(to_sort[-(i+1)][0])+"\t")
		genes_list=list(to_sort[-(i+1)][1])
		genes_list.sort()
		tmp_tot = set()
		sum = 0
		tmp_str = ""
		for j in range(len(genes_list)):
			tmp_tot.update(gene_mutatedSamples[genes_list[j]])
			sum += len(gene_mutatedSamples[genes_list[j]])
			tmp_str = tmp_str+genes_list[j]+"\t"
			if i < 1000:
				most_visited_file.write(genes_list[j]+"\t")
		tmp_weight = 2 * len(tmp_tot) - sum
		to_sort_weight.append([tmp_weight, tmp_str, str(to_sort[-(i+1)][0])])
		if i < 1000:
			most_visited_file.write(str(tmp_weight)+"\n")
	most_visited_file.close()

	#only the 1000 sets with highest weight are reported
	to_sort_weight.sort()
	highest_weight_file = open("sets_weightOrder_experiment"+str(exp_n)+".txt",'w')
	for i in range(min(len(to_sort_weight),1000)):
		highest_weight_file.write(str(to_sort_weight[-(i+1)][0])+"\t"+to_sort_weight[-(i+1)][1]+"\t"+to_sort_weight[-(i+1)][2]+"\n")
	highest_weight_file.close()
