from errors import *

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
    "false"
]


def let(parts, definitions, additional_definitions=None, inputs=None):

    name = parts[1]
    value = parts[2]
    _type = parts[3].rstrip(";")

    if not is_valid_name(name):
        raise ClopenNameError("Invalid variable name: " + name)

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
            raise ClopenValueError("Invalid bool value: " + value)

    elif _type == "str":
        pass

    elif _type == "list":
        value = value[1:-1]
        value = [parse_literal(x.strip()) for x in value.split(",")]


    # Inputs cannot be overwritten
    if inputs is not None and name in inputs:
        raise ClopenValueError("Cannot overwrite function input: " + name)


    # Function local variable
    if additional_definitions is not None:

        if name in additional_definitions:
            raise ClopenNameError("Variable already exists: " + name)

        additional_definitions[name] = [value, _type]
        return


    # Global variable
    if name in definitions:
        raise ClopenNameError("Variable already exists: " + name)

    definitions[name] = [value, _type]

def parse_literal(value):

    if value == "true":
        return True

    if value == "false":
        return False

    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
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

    if name.startswith("\"") and name.endswith("\""):
        return False
    
    return True