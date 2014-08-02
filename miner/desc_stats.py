## Basic mathematical statistics (yes, I know - NumPy would be better, 
## but I want to make the scripts stand-alone for now).

class DescriptiveStats(object):
    def __init__(self, name, all_values):
        self.name = name
        self._all_values = all_values
        self.total = sum(all_values)
        self.n_revs = len(all_values)

    def mean(self):
        return self.total / float(self._protected_n())

    def max_value(self):
        return max(self._all_values)

    def min_value(self):
        return min(self._all_values)

    def sd(self):
        from math import sqrt
        std = 0
        mean = self.mean()
        for a in self._all_values:
            std = std + (a - mean)**2
        std = sqrt(std / float(self._protected_n()))
        return std

    def _protected_n(self):
        n = self.n_revs
        return max(n, 1)