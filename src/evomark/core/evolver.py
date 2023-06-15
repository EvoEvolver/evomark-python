import ast
import warnings

from evomark.data_type.var_types import ValueByInput
from evomark.core.core import delete_old_comment_output
from evomark import EvolverInstance
from evomark.core.utils import get_stringified_string, get_stringified_string_with_indent


def show(var):
    evolver_id = "show"
    manager, line_i, stacks = EvolverInstance.get_context()
    caller_id = get_caller_id(stacks[0])
    manager.clear_ops_for_caller(caller_id)
    if check_if_stand_alone_call(stacks[0]) is None:
        return
    delete_old_comment_output(manager, caller_id, line_i, evolver_id)
    lines_to_insert = str(var).splitlines()
    manager.insert_comment_with_same_indent_after(caller_id, line_i, lines_to_insert, evolver_id)


def __warn_not_stand_alone_call(stack):
    print("Warning: \n" + stack.filename + ":" + str(stack.lineno) + ": \"" + stack.code_context[
        0].lstrip().strip() + "\" is not a stand-alone call. Ignored.")


def check_if_stand_alone_call(stack):
    code_line = stack.code_context[0].lstrip()
    arg_names = []
    try:
        tree = ast.parse(code_line)
        if len(tree.body) != 1:
            __warn_not_stand_alone_call(stack)
            return
        expr = tree.body[0]
        if not isinstance(expr, ast.Expr):
            __warn_not_stand_alone_call(stack)
            return
        value = expr.value
        if not isinstance(value, ast.Call):
            __warn_not_stand_alone_call(stack)
            return
        for arg in value.args:
            if isinstance(arg, ast.Name):
                arg_names.append(arg.id)
            else:
                arg_names.append(None)
    except:
        __warn_not_stand_alone_call(stack)
        return None
    return arg_names


def get_caller_id(stack):
    caller_id = stack.filename + ":" + str(stack.lineno)
    return caller_id


def let(var):
    manager, line_i, stacks = EvolverInstance.get_context()
    args = check_if_stand_alone_call(stacks[0])
    caller_id = get_caller_id(stacks[0])
    manager.clear_ops_for_caller(caller_id)
    if args is None:
        return
    assert len(args) == 1
    var_id = args[0]
    if var_id is None:
        warnings.warn("The argument of let() is not a direct variable. Ignored.")
        return
    LHS_value = args[0]
    if hasattr(var, "override_assign") and var.override_assign:
        LHS_value += ".value"
    # Delete the let(...) line
    manager.del_origin_lines(caller_id, line_i, line_i)

    stringified_var = None
    if isinstance(var, str):
        # stringified_var = get_stringified_string_with_indent(var, manager.get_indent(line_i))
        stringified_var = get_stringified_string()
    elif hasattr(var, "self_value_in_code"):
        stringified_var = var.self_value_in_code()
    else:
        raise NotImplementedError()

    manager.insert_with_same_indent_after(caller_id, line_i, [f'{LHS_value} = {stringified_var}'])

def retake(var: ValueByInput):
    manager, line_i, stacks = EvolverInstance.get_context()
    filepath = stacks[0].filename
    #caller_id = get_caller_id(stacks[0])
    #manager.del_origin_lines(caller_id, line_i, line_i)
    new_var = var.retake()
    EvolverInstance.set_cache(new_var, filepath)
    var.__dict__["value"] = new_var.value

def _gen(var: ValueByInput):
    pass

def evolve(output_path=None):
    _, _, stacks = EvolverInstance.get_context()
    if stacks[0].frame.f_locals["__name__"] != "__main__":
        # warnings.warn("update() is not called in __main__. Ignored.")
        return
    EvolverInstance.update_all_file()
    EvolverInstance.save_all_cache_to_file()
    EvolverInstance.save_all_output_to_file()
