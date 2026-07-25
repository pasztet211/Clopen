import os
from errors import ClopenNoFileError
from clo_loader import load_clo
from parser import parse

def cmd_with(parts, definitions, additional_definitions, run):
    filename = parts[1]
    if filename.endswith(".clo"):
        raise ClopenNoFileError("File extension '.clo' is not allowed for import.")
    full_filename = filename + ".clo"

    module_path = os.path.join(os.getcwd(), full_filename)

    if not os.path.isfile(module_path):
        raise ClopenNoFileError(f"File '{full_filename}' does not exist.")
    else:
        program = load_clo(module_path)
        instructions = parse(program)
        definitions_imp = {}
        definitions_imp = run(instructions, definitions_imp)
        if definitions_imp is not None:
            if additional_definitions is not None:
                for key, value in definitions_imp.items():
                    additional_definitions[f"{filename}.{key}"] = value
            else:
                for key, value in definitions_imp.items():
                    definitions[f"{filename}.{key}"] = value