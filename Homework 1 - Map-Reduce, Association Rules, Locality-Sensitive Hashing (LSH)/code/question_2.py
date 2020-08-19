# CS550 Massive Data Mining
# HW1Q2 Product Recommendation
# kd706 - Keya Desai

import os
import itertools

def prune(items_count_dict, support):

	freq = {}
	for item,count in items_count_dict.items():
		if count >= support:
			freq.update({item:count})

	return freq

def candidate_counts(baskets, frequent_items, k):

	combinations = itertools.combinations(sorted(frequent_items),k)
	candidates = {}

	for c in combinations:
		candidates[c] = 0
	
	for basket in baskets:
		basket_items = []
		for item in basket:
			if item in frequent_items:
				basket_items.append(item)
		basket_items = sorted(basket_items)
		item_tuples = itertools.combinations(basket_items, k)
		for item_tuple in item_tuples:
			if item_tuple in candidates:
				candidates[item_tuple] += 1

	return candidates


def confidence(frequent_subset, frequent_tuple, k):

	conf = []
	k -= 1
	for tuple_, count in frequent_tuple.items():

		if(k==1):
			key = (tuple_[0],tuple_[1])
			c = count/frequent_subset[tuple_[0]]
			# conf(A->B)
			conf.append((key,c))					

			key = (tuple_[1],tuple_[0])
			c = count/frequent_subset[tuple_[1]]
			# conf(B->A)
			conf.append((key,c))

		else: 	
			subsets = itertools.combinations(tuple_, k)
			for subset in subsets:
				if subset in frequent_subset:
					conf.append((tuple(list(subset) + list(set(tuple_)-set(subset))),  count/frequent_subset[subset]))


	return conf


if __name__ == "__main__":

	file_path = os.getcwd()
	
	# Change the directory name here
	file_path += '/data/browsing.txt'
	
	# change support if needed. 
	support = 100

	# read the data
	f = open(file_path,"r")

	singles = {}
	baskets = []

	for line in f:
		basket = line.strip().split(' ')
		for item in basket:
			if item in singles:
				singles[item] += 1
			else:
				singles[item] = 1
		baskets.append(set(basket))

	# Generating frequent pairs
	frequent_items = prune(singles, support)
	candidate_pairs = candidate_counts(baskets, frequent_items, 2)
	frequent_pairs = prune(candidate_pairs, support)
	confidence_pairs = confidence(frequent_items, frequent_pairs, 2)
	confidence_pairs.sort(key = lambda x:(-x[1], x[0]))

	print('-'*35)
	print("Top 5 pairs with support =",support)
	print('-'*35)
	for pair in confidence_pairs[:5]:
		print("{} -> {} {}".format(pair[0][0], pair[0][1], pair[1]))


	# Generating frequent triples
	frequent_items = []
	for pair in frequent_pairs:
		for item in pair:
			if item not in frequent_items:
				frequent_items.append(item)

	candidate_triples = candidate_counts(baskets, frequent_items, 3)
	frequent_triples = prune(candidate_triples, support)
	confidence_triples = confidence(frequent_pairs, frequent_triples, 3)
	confidence_triples.sort(key = lambda x:(-x[1],x[0]))

	print('-'*35)
	print("Top 5 triples with support =", support)
	print('-'*35)
	for triple in confidence_triples[:5]:
		 print("{}, {} -> {} {}".format(triple[0][0], triple[0][1], triple[0][2], triple[1]))







	
