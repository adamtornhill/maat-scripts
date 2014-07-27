#!/bin/env python
import sys, subprocess, re
from collections import defaultdict
import proximity

## Calculates the proximity between changes over a range of commits.
##
## Run the program as:
##
##  python git_proximity_analysis.py 540e8de d804759
##
## where the two arguments are the range of revisions of interest.
## Note that you must run the program from within a git repo.
##
## Expect a proper command line interface soon...
 
######################################################################
## Git interaction
######################################################################

# git log --pretty=format:"%cd  %h  %s" --date=short
# =>
# 2013-12-13  1c2f3c1  Introduced layers

def read_revs(rev_start, rev_end):
	""" Returns a list of all commits in the given range.
	"""
	rev_range = rev_start + '..' + rev_end
	git_log = subprocess.Popen(['git', 'log', rev_range, '--oneline'], stdout=subprocess.PIPE).communicate()[0]
	revs = []
	# match a line like: d804759 Documented tree map visualizations
	# ignore everything except the commit number:
	rev_expr = re.compile(r'([^\s]+)')
	for line in git_log.split("\n"):
		m = rev_expr.search(line)
		if m:
			revs.append(m.group(1))
	return revs[::-1]
 
def read_diff_for(rev1, rev2):
	return subprocess.Popen(['git', 'diff', rev1, rev2], stdout=subprocess.PIPE).communicate()[0]
 
new_module_expr = re.compile(r'^--- a\/(.+)')

def maybe_new_module(line):
	""" Search for a line like:
			--- a/src/code_maat/analysis/authors.clj
		Return the file name (sans the pre-fix) if found.
	"""
	m = new_module_expr.search(line)
	if m:
		return m.group(1)

change_line_expr = re.compile(r'@@ -(\d+),')

def changed_line(line):
	""" Search for a line like:
			@@ -65,7 +65,7 @@ 
		This is a diff on the unified format. We extract 
		the line number of the modification from the original 
		file and return it.
	"""
	m = change_line_expr.search(line)
	if m:
		offset = m.group(1)
		return int(offset)

def parse_changes_per_file_in(git_diff):
	files_with_changes = {}
	file_name = None

	for line in git_diff.split("\n"):
		# read ahead until we note the diff for a file:
		new_file = maybe_new_module(line)
		if new_file:
			file_name=new_file
		# one we have the diff of a file, accumulate the changes:
		if file_name:
			change = changed_line(line)
			proximity.record_change_to(file_name, change,files_with_changes)
	return files_with_changes
    
######################################################################
## Output
######################################################################

def as_csv(result):
    print 'file,revs,total,mean,sd,max'
    for p in result:
    	fields_of_interest = [p.name, p.n_revs, p.total, round(p.mean(),2), round(p.sd(),2), p.max_value()]
    	printable = [str(field) for field in fields_of_interest]
    	print ','.join(printable)

######################################################################
## Main
######################################################################

def read_proximities_from(revision_range):
	start_rev, end_rev = revision_range
	revs = read_revs(start_rev, end_rev)
	proximities = []
	for i in range(len(revs) - 1):
		first_revision = revs[i]
		revision_to_compare = revs[i+1]
		git_diff = read_diff_for(first_revision, revision_to_compare)
		changes = parse_changes_per_file_in(git_diff)
		proximities.append(proximity.calc_proximity(changes))
	return proximities

if __name__ == "__main__":
	revision_range = (sys.argv[1], sys.argv[2])
	proximities = read_proximities_from(revision_range)
	summed = proximity.sum_proximities(proximities)
	presentation_order = proximity.sorted_on_proximity(summed)
	as_csv(presentation_order)
 
