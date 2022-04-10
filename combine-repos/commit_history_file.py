class CommitHistoryFile:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, 'rt') as f:
            contents = f.read().splitlines()
        return contents
