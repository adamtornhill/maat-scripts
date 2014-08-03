#!/bin/env python
import sys, subprocess, re
from collections import defaultdict
import argparse
import git_interactions
import desc_stats
import complexity_calculations
	
######################################################################
## Statistics from complexity
######################################################################

class AggregatedStats(object):
	""" Aggregates statistics for added and removed complexity.
	"""
	def __init__(self, added, removed):
		self.added = self._stats_for(added)
		self.removed = self._stats_for(removed)
	
	def _stats_for(self, all_values):
		relevant = [r for r in all_values if r != 0]
		return desc_stats.DescriptiveStats('aggregate', relevant)
	
def parse_complexity_changes_in(revision, git_diff):
	cadded = []
	cremoved = []
	 
	# Queries on the lines in the diff:
	def marks_empty(line):
		return not line
	def marks_file_hunk(line):
		return (len(line) >= 4) and line[:3] in ('---', '+++')
	def marks_added(line):
		return not marks_empty(line) and line[0] == '+'
	def marks_removed(line):
		return not marks_empty(line) and line[0] == '-'
	# Extractors:
	def complexity_from_modified(line):
		return ccomplexity_calculations.omplexity_of(line[1:])

	for line in git_diff.split("\n"):
		if marks_empty(line):
			continue
		elif marks_file_hunk(line):
			continue
		elif marks_added(line):
			cadded.append(complexity_from_modified(line))
		elif marks_removed(line):
			cremoved.append(complexity_from_modified(line))
			
	stats = AggregatedStats(cadded, cremoved)
	return (revision, stats)
    
def delta_complexity_of(aggregated_stats):
	added_complexity = aggregated_stats.added.total
	removed_complexity = aggregated_stats.removed.total
	return added_complexity - removed_complexity

#print 'date, rev1, rev2, nAdded, totalAdded, meanAdded, nRemoved, totalRemoved, meanRemoved, totalDelta, meanDelta'

######################################################################
## Output
######################################################################

def as_csv(result):
    print 'rev,growth,nadded,addedtotal,addedmean,sd,nremoved,removedtotal,removedmean'
    for rev, stats in result:
    	added = stats.added
    	removed = stats.removed
    	growth = delta_complexity_of(stats)
    	fields_of_interest = [rev, growth, added.n_revs, added.total, round(added.mean(),2), round(added.sd(),2), 
    					      removed.n_revs, removed.total, round(removed.mean(), 2)]
    	printable = [str(field) for field in fields_of_interest]
    	print ','.join(printable)

######################################################################
## Main
######################################################################

def parse_complexity_delta_in(file_name, revision_range):
	start_rev, end_rev = revision_range
	revs = git_interactions.read_revs_for(file_name, start_rev, end_rev)
	complexity_by_rev = []
	for i in range(len(revs) - 1):
		first_revision = revs[i]
		revision_to_compare = revs[i+1]
		git_diff = git_interactions.read_file_diff_for(file_name, first_revision, revision_to_compare)
		complexity_in_one_rev = parse_complexity_changes_in(first_revision,git_diff)
		complexity_by_rev.append(complexity_in_one_rev)
	return complexity_by_rev

def run(args):
	revision_range = args.start, args.end
	complexity_delta_in_revs = parse_complexity_delta_in(args.file, revision_range)
	as_csv(complexity_delta_in_revs)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Calculates whitespace complexity trends over a range of revisions.')
	parser.add_argument('--start', required=True, help='The first commit hash to include')
	parser.add_argument('--end', required=True, help='The last commit hash to include')
	parser.add_argument('--file', required=True, type=str, help='The file to calculate complexity on')
	
	args = parser.parse_args()
	run(args)
