from evomark import EvolverInstance
from evomark.io.utils import get_abs_path

class Stream:
    def __init__(self, contents: list):
        self.contents = contents
        self.index = 0

    def read_next(self) -> str:
        if self.index >= len(self.contents):
            return None
        else:
            self.index += 1
            return self.contents[self.index - 1]

    def read_back(self) -> str:
        if self.index <= 0:
            return None
        else:
            self.index -= 1
            return self.contents[self.index]

    def go_to_beginning(self):
        self.index = 0

def read(file_path) -> Stream:
    """
    :param file_path: The path to the file to read.
    :return: A stream of paragraphs by splitting the file by two newlines.
    """
    caller_path = EvolverInstance.get_context()[2][0].filename
    abs_path = get_abs_path(file_path, caller_path)
    src = open(abs_path, "r").read()
    paragraphs = src.split("\n\n")
    return Stream(paragraphs)