import os
import re


class LanguagePreprocessor:
    def process(self, source) -> str:
        pass


class PassThrough(LanguagePreprocessor):
    def process(self, source) -> str:
        return source


class RemoveLeadingHashCharactersFromXpo(LanguagePreprocessor):
    regex = re.compile(r'^(\s*)#', re.MULTILINE)

    def process(self, source) -> str:
        return re.sub(self.regex, '\\1', source)


def create_for(file_name) -> LanguagePreprocessor:
    _, extension = os.path.splitext(file_name)
    if extension == ".xpo":
        return RemoveLeadingHashCharactersFromXpo()

    return PassThrough()
