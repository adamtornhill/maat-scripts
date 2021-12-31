import desc_stats

# Functions for calculating proximity/distance


def _pdistance(positions):
    return sum([j - i for i, j in zip(positions[:-1], positions[1:])])


def calc_proximity(changes):
    return dict([(name, _pdistance(change))
                 for name, change in changes.items()])


def record_change_to(file_name, change, acc):
    if not change:
        return

    existing = []
    if file_name in acc:
        existing = acc[file_name]
    existing.append(change)
    acc[file_name] = existing


def _as_stats(all_proximities):
    return [desc_stats.DescriptiveStats(name, proximities_for_one)
            for name, proximities_for_one in all_proximities.items()]


def _group_by(one_file, proximity, all_grouped):
    existing = []
    if one_file in all_grouped:
        existing = all_grouped[one_file]
    existing.append(proximity)
    return existing


def sum_proximity_stats(all_proximities):
    """ Received all proximities as a list of dictionaries.
        Each dictionary represents the proximities in the changed
        in one revision.
        Take this list and group all changes per item.
    """
    all_grouped = {}
    for one_rev_proximity in all_proximities:
        for (one_file, proximity) in one_rev_proximity.items():
            all_grouped[one_file] = _group_by(one_file, proximity, all_grouped)
    return _as_stats(all_grouped)


def sorted_on_proximity(proximity_stats):
    return sorted(proximity_stats, key=lambda p: p.total, reverse=True)
