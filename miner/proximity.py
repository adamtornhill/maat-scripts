import collections
from operator import itemgetter

## Functions for calculating proximity/distance

def _pdistance(positions):
    return sum([j-i for i,j in zip(positions[:-1], positions[1:])])

def calc_proximity(changes):
    return dict([(name, _pdistance(change)) for name, change in changes.iteritems()])

def record_change_to(file_name, change, acc):
    if not change:
        return

    existing = []
    if file_name in acc:
        existing = acc[file_name]
    existing.append(change)
    acc[file_name]=existing

def _recorded_changed_files_by_rev(all_proximities):
    return [file_name for file_name, _ in all_proximities]

def _files_with_number_of_revs(all_proximities):
    """ To calculate statistics we need to keep track of 
        the total number of recorded changes for each file.
        We count a change as anything that happened in a revision.
    """
    files_by_rev = _recorded_changed_files_by_rev(all_proximities)
    return collections.Counter(files_by_rev)

def sum_proximities(all_proximities):
    all = collections.Counter()
    for one_rev_proximity in all_proximities:
        for (one_file, proximity) in one_rev_proximity.iteritems():
            all[one_file] += proximity
    return all

def sorted_on_proximity(summed_proximities):
    return sorted(summed_proximities.iteritems(), key=itemgetter(1), reverse=True)