from evomark.core.utils import get_stringified_string


class ValueByInputHash:
    """
    Class for variables whose value is meaningful only with a certain key
    """

    def __init__(self, value, hash: str, input: any):
        self.input_hash: str = hash
        self.value = (value, hash)
        self.input = input
        self.meta = {}

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


class CachedValue(ValueByInputHash):
    def __init__(self, value, hash: str):
        super().__init__(value, hash)
