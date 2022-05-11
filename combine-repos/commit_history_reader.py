from commit import Commit


class CommitHistoryReader:
    def read(self, path):
        with open(path) as f:
            contents = f.read()
        return self.parse(contents)

    def parse(self, contents):
        if contents == '':
            return []

        # split the file contents by line
        lines = contents.split('\n')

        commit_groups = self.__group_lines_by_commit(lines)
        commits = self.__convert_commit_groups_to_commits(commit_groups)

        return commits

    @staticmethod
    def __group_lines_by_commit(lines):
        """Group lines into "commit_groups" which are not separated by a blank line.
        Every commit is a group of lines.
        Two commits are separated by a blank line.

        Returns a list of string lists. Each string list represents a commit.
        """

        commit_groups = []
        current_commit_group = []
        for line in lines:
            if len(current_commit_group) == 0:
                # This is the first line of the file or after the previous commit group has been closed.
                # This line is (usually) not empty but the header of the next commit.
                current_commit_group.append(line)

            elif line != '' and line[0] != '[':
                # This is the "numstat" line for a file modified in the commit.
                current_commit_group.append(line)

            elif line != '' and line[0] == '[':
                # The opening bracket shows that this is a new commit.
                # Having no blank line between this commit and the previous commit
                # shows that the previous commit was a merge commit.
                # This implies that the previous commit should not have any file modifications.
                commit_groups.append(current_commit_group)
                current_commit_group = [line]

            else:
                # This is a blank line.
                # Blank lines separate an ordinary commit from the next commit.
                commit_groups.append(current_commit_group)
                current_commit_group = []

        # If the file does not end with an empty line, the last commit group must be added here.
        if len(current_commit_group) > 0:
            commit_groups.append(current_commit_group)

        return commit_groups

    @staticmethod
    def __convert_commit_groups_to_commits(commit_groups):
        commits = []
        for commit_group in commit_groups:
            commit = Commit()
            commit.first_line = commit_group[0]
            commit.change_lines = commit_group[1:]
            commits.append(commit)
        return commits
