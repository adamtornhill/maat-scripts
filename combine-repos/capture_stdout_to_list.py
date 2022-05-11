import contextlib
import io


class CaptureStdoutToList(contextlib.redirect_stdout):
    """Redirect stdout and capture each line printed to stdout in target_list.

    Example
    -------
    >>> captured = []
    ... with CaptureStdoutToList(captured):
    ...     print('Hello World')
    ... captured
    ['Hello World']
    """
    def __init__(self, target_list):
        self.buffer = io.StringIO()
        self.target_list = target_list
        self.target_list.clear()
        super().__init__(self.buffer)

    def __exit__(self, exctype, excinst, exctb):
        captured_lines = self.buffer.getvalue().split('\n')

        # split inserts a blank line at the end, if the last line in the buffer ends with '\n'
        # remove this wrong indicator of a blank line where there is none
        captured_lines = captured_lines[:-1]

        self.target_list += captured_lines
        return super().__exit__(exctype, excinst, exctb)
