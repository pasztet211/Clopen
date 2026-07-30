import os
import importlib.util

from errors import ClopenNoFileError, Error_line
from clo_loader import load_clo
from parser import parse

def load_py(path, name):
    spec = importlib.util.spec_from_file_location(name, path)

    if spec is None or spec.loader is None:
        raise ClopenNoFileError(f"[Line {Error_line}] Could not load Python module '{name}'.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "definitions"):
        raise ClopenNoFileError(
            f"[Line {Error_line}] Python module '{name}' does not have a definitions dictionary."
        )

    return module.definitions


def cmd_with(parts, definitions, run, additional_definitions=None):
    command = None
    inputs = []
    filename = parts[1]

    if len(parts) != 2:
        command = parts[2]
        inputs = parts[3:]

    if filename.endswith(".clo") or filename.endswith(".py"):
        raise ClopenNoFileError(f"[Line {Error_line}] File extension is not allowed for import.")

    if command is not None and command == "from":
        base_name = inputs[0]
    else:
        base_name = filename

    py_filename = base_name + ".py"
    clo_filename = base_name + ".clo"

    py_path = os.path.join("C:\\Clopen\\stdlib\\", py_filename)
    clo_path = os.path.join(os.getcwd(), clo_filename)

    if os.path.isfile(py_path):
        module_type = "py"
        module_path = py_path

    elif os.path.isfile(clo_path):
        module_type = "clo"
        module_path = clo_path

    else:
        raise ClopenNoFileError(f"[Line {Error_line}] Module '{base_name}' does not exist.")

    if module_type == "py":
        definitions_imp = load_py(module_path, base_name)

    else:
        program = load_clo(module_path)
        instructions = parse(program)

        definitions_imp = {}
        definitions_imp = run(instructions, definitions_imp)

    from_used = False

    if command is not None:
        if command == "from":
            filename, inputs = str(inputs[0]), filename.split(",")
            from_used = True

        elif command == "as":
            filename = inputs[0]

    target = additional_definitions if additional_definitions is not None else definitions

    for key, value in definitions_imp.items():
        if from_used:
            if key in inputs:
                target[key] = value
        else:
            target[f"{filename}.{key}"] = value