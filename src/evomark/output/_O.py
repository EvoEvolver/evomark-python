"""
The file handles the output of the script.
"""
import os

from evomark import EvolverInstance


def set_out_path(out_path):
    caller_path = EvolverInstance.get_context()[2][0].filename
    EvolverInstance.default_out_path[caller_path] = get_abs_path(out_path, caller_path)

def get_abs_path(out_path, caller_path):
    if os.path.isabs(out_path):
        abs_path = out_path
    else:
        abs_path = os.path.join(os.path.dirname(caller_path), out_path)
    abs_path = os.path.normpath(abs_path)
    return abs_path

def out_cl(content):
    caller_path = EvolverInstance.get_context()[2][0].filename
    _out_cl(content, EvolverInstance.get_out_path(caller_path))


def _out_cl(content, out_path):
    EvolverInstance.append_output(out_path, content)
    EvolverInstance.append_output(out_path, "\n")


def out(content):
    caller_path = EvolverInstance.get_context()[2][0].filename
    _out(content, EvolverInstance.get_out_path(caller_path))


def _out(content, out_path):
    EvolverInstance.append_output(out_path, content)

def new_out_file(out_path):
    caller_path = EvolverInstance.get_context()[2][0].filename
    return OutputFile(get_abs_path(out_path, caller_path))

class OutputFile:
    def __init__(self, abs_path: str):
        self.abs_path = os.path.normpath(abs_path)

    def out(self, content):
        _out(content, self.abs_path)

    def out_cl(self, content):
        _out_cl(content, self.abs_path)