class CommitListPrinter:
    # TODO test boundary cases
    # - empty commits array
    # - single commit
    # - two commits
    def print(self, commits):
        for commit in commits[:-1]:
            print(str(commit))
            print()
        print(str(commits[-1]))
