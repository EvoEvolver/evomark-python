
def to_space(s: str):
    # Replace underscore with space
    return s.replace("_", " ")

class KeyValue:
    def __init__(self, main_key, main_value):
        self._predicates = {}
        self._main_key = to_space(main_key)
        self._main_value = main_value

    def __setattr__(self, key, value):
        if key.startswith("_"):
            self.__dict__[key] = value
        else:
            self._predicates[to_space(key)] = value

    def __str__(self):
        res = [f"{self._main_key}: {self._main_value}"]
        for key, value in self._predicates.items():
            res.append(f"{key}: {value}")
        return "\n".join(res)

def topic(content):
    return KeyValue("topic", content)

def question(content):
    return KeyValue("question", content)

