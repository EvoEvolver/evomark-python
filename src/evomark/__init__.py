from evomark.core import EvoCore
EvolverInstance = EvoCore()

from evomark.core._E import show, let, evolve, retake
from evomark.model.openai import answer
from evomark.data_type.key_value import question, topic
from evomark.io.out import out, out_cl, set_out_path
from evomark.io.input import read