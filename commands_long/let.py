from errors import *
from helper_functions import *

reserved = [
    "let",
    "fn",
    "if",
    "else",
    "while",
    "for",
    "return",
    "update",
    "set",
    "del",
    "log",
    "shalt",
    "halt",
    "get", 
    "true",
    "false",
    "int",
    "str",
    "bool",
    "list",
    "float"
]


def let(parts, definitions, additional_definitions=None, inputs=None):
    try:
        name = parts[1]
        value = parts[2]
        _type = parts[3].rstrip(";")
    except IndexError:
        raise ClopenSyntaxError(f"[Line {Error_line}] Invalid let statement: " + " ".join(parts))

    if not is_valid_name(name):
        raise ClopenNameError(f"[Line {Error_line}] Invalid variable name: " + name)

    # Convert value
    if _type == "int":
        value = int(value)

    elif _type == "float":
        value = float(value)

    elif _type == "bool":
        if value == "true":
            value = True
        elif value == "false":
            value = False
        else:
            raise ClopenValueError(f"[Line {Error_line}] Invalid bool value: " + value)

    elif _type == "str":
        pass

    elif _type == "list":
        value = value[1:-1]
        value_temp = [list(parse_literal_with_type(x.strip())) for x in value.split(",")]
        value = {}
        for i in range(len(value_temp)):
            value[f"{i}"] = value_temp[i]



    # Inputs cannot be overwritten
    if inputs is not None and name in inputs:
        raise ClopenValueError(f"[Line {Error_line}] Cannot overwrite function input: " + name)


    # Function local variable
    if additional_definitions is not None:

        if name in additional_definitions:
            raise ClopenNameError(f"[Line {Error_line}] Variable already exists: " + name)

        additional_definitions[name] = [value, _type]
        return


    # Global variable
    if name in definitions:
        raise ClopenNameError(f"[Line {Error_line}] Variable already exists: " + name)

    definitions[name] = [value, _type]

def parse_literal_with_type(value):
    if value == "true":
        return True, "bool"

    if value == "false":
        return False, "bool"

    if value.startswith('"') and value.endswith('"'):
        return value[1:-1], "str"

    try:
        return int(value), "int"
    except ValueError:
        pass

    try:
        return float(value), "float"
    except ValueError:
        pass

    return value

def is_valid_name(name):

    if not name.isidentifier():
        return False

    if name in reserved:
        return False

    if name.startswith("__") and name.endswith("__"):
        return False

    if name.startswith("$"):
        return False

    if name.startswith('"') and name.endswith('"'):
        return False

    if "#" in name or "\\\\" in name:
        return False
    
    return True