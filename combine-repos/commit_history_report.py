class CommitHistoryReport:

    @staticmethod
    def generate(commits):
        if len(commits) == 0:
            return ''

        lines = []
        for commit in commits[:-1]:
            lines.append(str(commit))

            if not commit.is_merge:
                lines.append('')

        lines.append(str(commits[-1]))
        return '\n'.join(lines)
