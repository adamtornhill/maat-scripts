######################################################################
## This program calulcates the complexity trend over a range of 
## revisions in a Git repo.
######################################################################

#!/bin/env python
import sys, subprocess, re
from collections import defaultdict
import argparse
import git_interactions
import desc_stats

######################################################################
## Complexity calcualations
######################################################################

leading_tabs_expr = re.compile(r'^(\t+)')
leading_spaces_expr = re.compile(r'^( +)')
empty_line_expr = re.compile(r'^\s*$')

def n_log_tabs(line):
	pattern = re.compile(r' +')
	wo_spaces = re.sub(pattern, '', line)
	m = leading_tabs_expr.search(wo_spaces)
	if m:
		tabs = m.group()
		return len(tabs)
	return 0
		
def n_log_spaces(line):
	pattern = re.compile(r'\t+')
	wo_tabs = re.sub(pattern, '', line)
	m = leading_spaces_expr.search(wo_tabs)
	if m:
		spaces = m.group()
		return len(spaces)
	return 0

def contains_code(line):
	return not empty_line_expr.match(line)
		
def complexity_of(line):
	return n_log_tabs(line) + (n_log_spaces(line) / 4) # hardcoded indentation
	
######################################################################
## Statistics from complexity
######################################################################
	
def calculate_complexity_in(source):
	return [complexity_of(line) for line in source.split("\n") if contains_code(line)]

def as_stats(revision, complexity_by_line):
	return desc_stats.DescriptiveStats(revision, complexity_by_line)
    
######################################################################
## Output
######################################################################

def as_csv(result):
    print 'rev,n,total,mean,sd'
    for stats in result:
    	fields_of_interest = [stats.name, stats.n_revs, stats.total, round(stats.mean(),2), round(stats.sd(),2)]
    	printable = [str(field) for field in fields_of_interest]
    	print ','.join(printable)

######################################################################
## Main
######################################################################

def calculate_complexity_over_range(file_name, revision_range):
	start_rev, end_rev = revision_range
	revs = git_interactions.read_revs_for(file_name, start_rev, end_rev)
	complexity_by_rev = []
	for rev in revs:
		historic_version = git_interactions.read_version_matching(file_name, rev)
		complexity_by_line = calculate_complexity_in(historic_version)
		complexity_by_rev.append(as_stats(rev, complexity_by_line))
	return complexity_by_rev

def run(args):
	revision_range = args.start, args.end
	complexity_trend = calculate_complexity_over_range(args.file, revision_range)
	as_csv(complexity_trend)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Calculates whitespace complexity trends over a range of revisions.')
	parser.add_argument('--start', required=True, help='The first commit hash to include')
	parser.add_argument('--end', required=True, help='The last commit hash to include')
	parser.add_argument('--file', required=True, type=str, help='The file to calculate complexity on')
	
	args = parser.parse_args()
	run(args)
