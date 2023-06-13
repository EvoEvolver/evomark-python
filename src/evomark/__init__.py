from core import EvoCore
EvolverInstance = EvoCore()

from core._E import show, let, update, retake
from model.openai import ask, answer
from data_type.key_value import question, topic
from output._O import out, out_cl, set_out_path

