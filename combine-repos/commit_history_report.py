class CommitHistoryReport:

    @staticmethod
    def generate(commits):
        if len(commits) == 0:
            return ''

        lines = []
        for commit in commits[:-1]:
            lines.append(str(commit))

            # Only insert the blank line, if the current commit is not a merge commit
            # merge commits can be recognized by not having the numstat entry - i.e. the change records in
            # the change_lines property
            if len(commit.change_lines) > 0:
                lines.append('')

        lines.append(str(commits[-1]))
        return '\n'.join(lines)
