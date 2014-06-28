from operator import itemgetter

## Functions for calculating proximity/distance

def pdistance(positions):
    return sum([j-i for i,j in zip(positions[:-1], positions[1:])])

def calc_proximity(changes):
    return dict([(name, pdistance(change)) for name, change in changes.iteritems()])

def record_change_to(file_name, change, acc):
    if not change:
        return

    existing = []
    if file_name in acc:
        existing = acc[file_name]
    existing.append(change)
    acc[file_name]=existing

def sum_proximities(all_proximities):
    all = {}
    for one_rev_proximity in all_proximities:
        for (one_file, proximity) in one_rev_proximity.iteritems():
            existing = 0
            if one_file in all:
                existing = all[one_file]
            all[one_file] = existing + proximity
    return all

def sorted_on_proximity(summed_proximities):
    return sorted(summed_proximities.iteritems(), key=itemgetter(1), reverse=True)