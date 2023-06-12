import hashlib
import inspect
import json
import os
from typing import Dict, Optional

from evomark.core.src_manager import SrcManager
from evomark.core.src_manager import comment_delimiter


class EvoCache:
    def __init__(self, value, hash: str, input: str, type: str, meta: Optional[Dict] = None):
        self.value = value
        self.hash: str = hash
        self.input: str = input
        self.type: str = type
        self.meta = meta

    def get_self_dict(self):
        return {
            "value": self.value,
            "hash": self.hash,
            "input": self.input,
            "type": self.type,
            "meta": self.meta
        }


class EvoCacheTable:
    def __init__(self):
        self.cache_table: Dict[str, EvoCache] = {}


def serialize_cache_table(cache_table: Dict[str, EvoCache]):
    res = []
    for key, cache in cache_table.items():
        res.append(cache.get_self_dict())
    return json.dumps(res, indent=1)


class EvoCore:
    def __init__(self):
        # Map from the file path to the SrcManager
        self.file_src_keeper: Dict[str, SrcManager] = {}
        # Map from the file path to the cache table
        self.cache_table_map: Dict[str, EvoCacheTable] = {}
        # Map from the file path to the output content
        self.file_outputs: Dict[str, list] = {}
        # Map from the file path to the default output path for it
        self.default_out_path: Dict[str, str] = {}

    def get_out_path(self, caller_path):
        if caller_path in self.default_out_path:
            return self.default_out_path[caller_path]
        return caller_path + ".out"

    def append_output(self, filepath: str, content: any):
        if filepath not in self.file_outputs:
            self.file_outputs[filepath] = []
        self.file_outputs[filepath].append(str(content))

    def save_all_output_to_file(self):
        for filepath, outputs in self.file_outputs.items():
            with open(filepath, "w") as f:
                f.write("".join(outputs))

    def get_file_manager(self, filepath: str) -> SrcManager:
        if filepath not in self.file_src_keeper:
            self.file_src_keeper[filepath] = SrcManager(open(filepath).read())
        return self.file_src_keeper[filepath]

    def get_context(self):
        stack = inspect.stack()[2:]
        caller_stack = stack[0]
        filepath = caller_stack.filename
        line_i = caller_stack.lineno - 1
        manager = self.get_file_manager(filepath)
        return manager, line_i, stack

    def update_all_file(self):
        for filepath, manager in self.file_src_keeper.items():
            curr_src = manager.get_curr_src()
            with open(filepath, "w") as f:
                f.write(curr_src)

    def save_all_cache_to_file(self):
        for filepath, cache_table in self.cache_table_map.items():
            with open(filepath + ".ec.json", "w") as f:
                f.write(serialize_cache_table(cache_table.cache_table))

    def hash(self, obj):
        if isinstance(obj, str):
            return hashlib.sha1(str(obj).encode("utf-8")).hexdigest()
        else:
            return hashlib.sha1(json.dumps(obj).encode("utf-8")).hexdigest()

    def read_cache(self, key: str, filepath: str, create_cache=True) -> EvoCache:
        if filepath not in self.cache_table_map:
            self.cache_table_map[filepath] = load_cache_table(filepath)
        cache_table = self.cache_table_map[filepath]
        if key not in cache_table.cache_table:
            if create_cache:
                new_cache = EvoCache(None, key, None, None)
                cache_table.cache_table[key] = new_cache
                return new_cache
            else:
                return None
        return cache_table.cache_table[key]


def load_cache_table(filepath: str) -> EvoCacheTable:
    cache_path = filepath + ".ec.json"
    if not os.path.exists(cache_path):
        # Create file if not exists
        with open(cache_path, "w") as f:
            f.write("[]")
        return EvoCacheTable()
    with open(filepath + ".ec.json", "r") as f:
        cache_list = json.load(f)
    cache_table = EvoCacheTable()
    for cache_dict in cache_list:
        cache = EvoCache(cache_dict["value"], cache_dict["key"], cache_dict["input"], cache_dict["type"], cache_dict["meta"])
        cache_table.cache_table[cache.hash] = cache
    return cache_table


EvolverInstance = EvoCore()


def delete_old_comment_output(manager: SrcManager, caller_id, line_i: int, evolver_id: str):
    # Check whether it's the last line
    # Or the next line isn't generated by the evolver
    if line_i >= manager.src_len - 1 or manager.src_list[line_i + 1].strip() != f'{comment_delimiter}{evolver_id}':
        return
    start = line_i + 1
    end = -1
    for i in range(start + 1, manager.src_len):
        if comment_delimiter in manager.src_list[i]:
            end = i
            break
    # illegal case: no ending block
    if end == -1:
        return
    manager.del_origin_lines(caller_id, start, end)
