from typing import Callable

from evomark.core.core import EvoCache
from evomark.core.utils import get_stringified_string


class ValueByInput:
    """
    Class for variables whose value is meaningful only with a certain key
    """

    def __init__(self, value, hash: str, input: any, type: str):
        self.input_hash: str = hash
        self.value = (value, hash)
        self.input = input
        self.type = type
        self.meta = {}
        # Should ensure that self.func(self.input) = self.value
        self.func = None

    def retake(self):
        assert self.func is not None
        res = ValueByInput(self.func(self.input), self.input_hash, self.input, self.type)
        res.meta = self.meta
        res.func = self.func
        return res

    @classmethod
    def from_cache(cls, cache: EvoCache, func: Callable):
        res = ValueByInput(cache.value, cache.hash, cache.input, cache.type)
        res.meta = cache.meta
        res.func = func
        return res

    override_assign = True

    def __setattr__(self, key, incoming_value):
        value = incoming_value
        if key == "value":
            if len(incoming_value) != 2:
                raise ValueError("ValueByInputHash's assigner must be a tuple of length 2")
            value_carried, key_to_be_matched = incoming_value
            if key_to_be_matched == self.input_hash:
                value = value_carried
            else:
                # Do nothing if the key does not match
                return
        super().__setattr__(key, value)

    def __str__(self):
        return str(self.value)

    def self_value_in_code(self):
        res = ["("]
        if isinstance(self.value, str):
            res.append(f'{get_stringified_string(self.value)}')
        else:
            res.append(f'{self.value}')
        res.append(",")
        res.append(f'"{self.input_hash}"')
        res.append(")")
        return "".join(res)