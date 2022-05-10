import re
from datetime import date


class Commit:
    def __init__(self):
        self.first_line = ''
        self.change_lines = []
        pass

    @property
    def date(self):
        # Correct format of the first line:
        # [1234567] Some Name YYYY-MM-DD Some Comment
        if self.first_line is None:
            return None

        regex = '([0-9]{4}-[0-9]{2}-[0-9]{2})'
        date_search = re.search(regex, self.first_line)

        if date_search:
            date_str = date_search.group(1)
            return date.fromisoformat(date_str)

        return None

    @property
    def first_line(self):
        return self._first_line

    @first_line.setter
    def first_line(self, value):
        self._first_line = value

    @first_line.deleter
    def first_line(self):
        del self._first_line

    @property
    def change_lines(self):
        return self._change_lines

    @change_lines.setter
    def change_lines(self, value):
        self._change_lines = value

    @change_lines.deleter
    def change_lines(self):
        del self._change_lines

    @property
    def is_merge(self):
        # merge commits can be recognized by not having the numstat entry,
        # i.e. the change records in the change_lines property are empty
        return len(self.change_lines) == 0

    def __eq__(self, other):
        if not isinstance(other, Commit):
            return False
        return self.first_line == other.first_line and self.change_lines == other.change_lines

    def __repr__(self) -> str:
        representation = 'Commit("{0}", [ '.format(self.first_line)
        for change_line in self.change_lines:
            representation += '"{0}" '.format(change_line)
        representation += ']'
        return representation

    def __str__(self) -> str:
        result = self.first_line

        if not self.is_merge:
            result += '\n' + '\n'.join(self.change_lines)

        return  result
