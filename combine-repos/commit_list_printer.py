class CommitListPrinter:

    def __init__(self) -> None:
        self.print_function = print

    # TODO test boundary cases
    # - empty commits array
    # - single commit
    # - two commits
    def print(self, commits):
        for commit in commits[:-1]:
            self.print_function(str(commit))
            self.print_function()
        self.print_function(str(commits[-1]))
