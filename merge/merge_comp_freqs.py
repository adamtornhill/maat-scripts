## Merges two CSV documents.
##

import csv
import sys

p1 = {}
p2 = {}

def cache_complexity(name, complexity):
	default_size_metric = 0
	p1[name] = complexity,default_size_metric

def extend_with(name, freqs):
	if name in p1:
		complexity, _ = p1[name]
		p2[name] = freqs, complexity
	
def skip_heading(f):
	next(f)
	
def parse_csv(filename, parse_action):
	with open(filename, 'rb') as csvfile:
		r = csv.reader(csvfile, delimiter=',')
		skip_heading(r)
		for row in r:
			parse_action(row)

def write_csv(stats):
	print 'module,revisions,code'
	# Sort on descending order:
	ordered = sorted(stats.items(), key=lambda item: item[1][0], reverse=True)
	for s in ordered:
		name, (f,c) = s
		print name + ',' + f + ',' + c
	
def parse_complexity(row):
	name = row[1][2:]
	complexity = row[4]
	cache_complexity(name, complexity)

def parse_freqs(row):
	name = row[0]
	freqs = row[1]
	extend_with(name, freqs)

# TODO: check!
revs_file = sys.argv[1]
comp_file = sys.argv[2]

parse_csv(comp_file, parse_complexity)
parse_csv(revs_file, parse_freqs)
write_csv(p2)
