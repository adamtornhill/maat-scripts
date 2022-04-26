import contextlib
import io


class CaptureStdoutToList(contextlib.redirect_stdout):

    def __init__(self, new_target, target_list):
        self.buffer = io.StringIO()
        self.target_list = target_list
        super().__init__(new_target)

    def __exit__(self, exctype, excinst, exctb):
        self.target_list.append(self.buffer.getvalue().split('\n'))

        # split inserts a blank line at the end, if the last line in the buffer ends with '\n'
        # remove this wrong indicator of a blank line where there is none
        #self.target_list

        # TODO assign captured output to target list in the tests

        return super().__exit__(exctype, excinst, exctb)
