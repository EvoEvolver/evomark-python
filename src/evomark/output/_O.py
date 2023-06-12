"""
The file handles the output of the script.
"""

from evomark.core.core import EvolverInstance


def set_out_path(out_path):
    caller_path = EvolverInstance.get_context()[2][0].filename
    EvolverInstance.default_out_path[caller_path] = out_path


def out_cl(content, out_path=None):
    caller_path = EvolverInstance.get_context()[2][0].filename
    opath = out_path if out_path is not None else EvolverInstance.get_out_path(caller_path)
    EvolverInstance.append_output(opath, content)
    EvolverInstance.append_output(opath, "\n")


def out(content, out_path=None):
    caller_path = EvolverInstance.get_context()[2][0].filename
    opath = out_path if out_path is not None else EvolverInstance.get_out_path(caller_path)
    EvolverInstance.append_output(opath, content)
