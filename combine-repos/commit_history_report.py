class CommitHistoryReport:

    # TODO test boundary cases
    # - single commit
    # - two commits
    @staticmethod
    def print(commits):
        if len(commits) == 0:
            return

        for commit in commits[:-1]:
            print(str(commit))
            print()
        print(str(commits[-1]))
