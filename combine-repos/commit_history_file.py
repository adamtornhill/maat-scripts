from commit import Commit


class CommitHistoryFile:
    def __init__(self, path):
        self.path = path

    def parse(self, contents):
        if contents == '':
            return []

        commits = []
        commit = Commit()

        lines = contents.rstrip().split('\n')

        index = 0
        has_first_line = False
        while index < len(lines):
            line = lines[index]

            if line == '':
                commits.append(commit)
                commit = Commit()
                has_first_line = False

            elif not has_first_line:
                commit.first_line = line
                has_first_line = True

            else:
                commit.change_lines.append(line)

            index += 1

        commits.append(commit)

        return commits

    def read(self):
        with open(self.path, 'rt') as f:
            contents = f.read().splitlines()
        return contents
