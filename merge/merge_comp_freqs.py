#!/usr/bin/env python3

# Merges two CSV documents.
##

import csv
import sys
import os


class MergeError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class Merged(object):
    def __init__(self):
        self._all_modules_with_complexity = {}
        self._merged = {}

    def sorted_result(self):
        # Sort on descending order:
        ordered = sorted(
            list(
                self._merged.items()), key=lambda item: int(
                item[1][0]), reverse=True)
        return ordered

    def extend_with(self, name, freqs):
        if name in self._all_modules_with_complexity:
            complexity = self._all_modules_with_complexity[name]
            self._merged[name] = freqs, complexity

    def record_detected(self, name, complexity):
        self._all_modules_with_complexity[name] = complexity


def skip_heading(f):
    next(f)


def read_heading_from(r):
    p = next(r)
    while p == []:
        p = next(r)
    return p


def validate_content_by(heading, expected):
    comparison = expected.split(',')
    stripped = heading[0:len(comparison)]  # allow extra fields
    if stripped != comparison:
        raise MergeError(
            'Erroneous content. Expected = ' +
            expected +
            ', got = ' +
            ','.join(heading))


def parse_csv(merged, filename, parse_action, expected_format):
    with open(filename, 'rt') as csvfile:
        r = csv.reader(csvfile, delimiter=',')
        heading = read_heading_from(r)
        validate_content_by(heading, expected_format)
        for row in r:
            parse_action(merged, row)


def write_csv(stats):
    print('module,revisions,code')
    for s in stats:
        name, (f, c) = s
        print(name + ',' + f + ',' + c)


def as_os_aware_path(name):
    return os.path.normpath(name)


def parse_complexity(merged, row):
    name = as_os_aware_path(row[1])
    complexity = row[4]
    merged.record_detected(name, complexity)


def parse_freqs(merged, row):
    name = as_os_aware_path(row[0])
    freqs = row[1]
    merged.extend_with(name, freqs)


def merge(revs_file, comp_file):
    merged = Merged()
    parse_csv(merged, comp_file, parse_complexity,
              expected_format='language,filename,blank,comment,code')
    parse_csv(merged, revs_file, parse_freqs, expected_format='entity,n-revs')
    write_csv(merged.sorted_result())


if __name__ == '__main__':
    if len(sys.argv) != 3:
        msg = ('Wrong arguments. Require one CSV file with frequencies and one'
               ' with the complexity')
        raise MergeError(msg)
    revs_file = sys.argv[1]
    comp_file = sys.argv[2]
    merge(revs_file, comp_file)
