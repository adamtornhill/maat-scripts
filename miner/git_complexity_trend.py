######################################################################
## This program calulcates the complexity trend over a range of 
## revisions in a Git repo.
######################################################################

#!/bin/env python
import argparse
import git_interactions
import desc_stats
import complexity_calculations
	
######################################################################
## Statistics from complexity
######################################################################

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
		complexity_by_line = complexity_calculations.calculate_complexity_in(historic_version)
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
