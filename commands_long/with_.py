import os
from errors import ClopenNoFileError
from clo_loader import load_clo
from parser import parse

def cmd_with(parts, definitions, run, additional_definitions=None):
    command = None
    inputs = []
    filename = parts[1]
    if len(parts) != 2:
        command = parts[2]
        inputs = parts[3:]
    if filename.endswith(".clo"):
        raise ClopenNoFileError("File extension '.clo' is not allowed for import.")
    if command is not None:
        if command == "from":
            full_filename = inputs[0] + ".clo"
        else:
            full_filename = filename + ".clo"
    else:
        full_filename = filename + ".clo"

    module_path = os.path.join(os.getcwd(), full_filename)

    if not os.path.isfile(module_path):
        raise ClopenNoFileError(f"File '{full_filename}' does not exist.")
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
            if command == "as":
                filename = inputs[0]
        target = additional_definitions if additional_definitions is not None else definitions
        for key, value in definitions_imp.items():
            if from_used:
                if key in inputs:
                    target[key] = value
            else:
                target[f"{filename}.{key}"] = value