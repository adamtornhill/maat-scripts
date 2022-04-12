from commit import Commit


def group_lines_by_commit(lines):
    """Group lines into "commit_groups" which are not separated by a blank line.
    Every commit is a group of lines.
    Two commits are separated by a blank line.

    Returns a list of string lists. Each string list represents a commit.
    """

    commit_groups = []
    current_commit_group = []
    for line in lines:
        if line != '':
            current_commit_group.append(line)
        else:
            commit_groups.append(current_commit_group)
            current_commit_group = []

    # If the file does not end with an empty line, the last commit group must be added here.
    if len(current_commit_group) > 0:
        commit_groups.append(current_commit_group)

    return commit_groups


class CommitHistoryFile:
    def __init__(self, path):
        self.path = path

    def parse(self, contents):
        if contents == '':
            return []

        # split the file contents by line
        lines = contents.split('\n')

        commit_groups = group_lines_by_commit(lines)

        commits = []
        for commit_group in commit_groups:
            commit = Commit()
            commit.first_line = commit_group[0]
            commit.change_lines = commit_group[1:]
            commits.append(commit)

        return commits

    def read(self):
        with open(self.path, 'rt') as f:
            contents = f.read().splitlines()
        return contents
