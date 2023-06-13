from __future__ import annotations

import hashlib
import inspect
import json
import os
from typing import Dict, Optional, Tuple
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data_type.var_types import ValueByInput

from evomark.core.src_manager import SrcManager
from evomark.core.src_manager import comment_delimiter

def get_hash(input: any, type: str) -> str:
    return hashlib.sha1(json.dumps([input, type]).encode("utf-8")).hexdigest()

class EvoCache:
    def __init__(self, value, hash: str, input: any, type: str, meta: Optional[Dict] = None):
        self.value = value
        self.hash: str = hash
        self.input: any = input
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

    def set_cache(self, value: any, meta: Optional[Dict] = None):
        assert self.value is None
        assert self.hash is not None
        assert self.input is not None
        self.value = value
        self.meta = meta


class EvoCacheTable:
    def __init__(self):
        self.map: Dict[str, EvoCache] = {}

    def __setitem__(self, key, value):
        self.map[key] = value


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
        """
        Get the context of the caller
        Assuming that this function is called directly at the codes of the caller

        :return: The SrcManager, the line number and stack of where the caller is called.
        """
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
                f.write(serialize_cache_table(cache_table.map))

    def read_cache(self, input: any, type:str, filepath: str, create_cache=True) -> EvoCache:
        hash = get_hash(input, type)
        if filepath not in self.cache_table_map:
            self.cache_table_map[filepath] = load_cache_table(filepath)
        cache_table = self.cache_table_map[filepath]
        if hash not in cache_table.map:
            if create_cache:
                new_cache = EvoCache(None, hash, input, type)
                cache_table.map[hash] = new_cache
                return new_cache
            else:
                return None
        return cache_table.map[hash]

    def set_cache(self, var: ValueByInput, filepath: str):
        cache_table = self.cache_table_map[filepath]
        cache_table[var.input_hash] = EvoCache(var.value, var.input_hash, var.input, var.type)


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
        cache = EvoCache(cache_dict["value"], cache_dict["hash"], cache_dict["input"], cache_dict["type"], cache_dict["meta"])
        cache_table.map[cache.hash] = cache
    return cache_table


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
