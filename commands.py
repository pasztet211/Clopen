from commands_long.let import let
from errors import *
from commands_long.update import update

def cmd_let(parts,definitions,additional_definitions=None,inputs=None):
    let(parts, definitions, additional_definitions, inputs)

def cmd_update(parts,definitions,additional_definitions=None,inputs=None):
    update(parts,definitions,additional_definitions,inputs)

def cmd_log(parts,definitions,additional_definitions=None,inputs=None):
    name = parts[1]
    if "[" in name and name.endswith("]"):

        name, index = name[:-1].split("[", 1)

        if name not in definitions or (additional_definitions is not None and name not in additional_definitions):
            raise ClopenNameError("Variable does not exist: " + name)

        index = int(index)

        if additional_definitions is not None and name in additional_definitions:
            print(additional_definitions[name][0][index])
        else:
            print(definitions[name][0][index])
    else:
        if name.startswith("\"") and name.endswith("\""):
            print(name[1:-1])
            return
        
        elif name.startswith("$"):
            get_value(name[1:], definitions, additional_definitions, inputs)
            return
        else:
            if inputs is not None and name in inputs:
                print(inputs[name][0])

            elif additional_definitions is not None and name in additional_definitions:
                print(additional_definitions[name][0])

            elif name in definitions:
                print(definitions[name][0])
            
            else:
                if name == "\\n":
                    print()
                    return
                print(name)

def cmd_set(parts, definitions, additional_definitions=None, inputs=None):
    name = parts[1]
    expression = parts[2]
    _type = parts[3]

    if inputs is not None and name in inputs:
        target = inputs

    elif additional_definitions is not None and name in additional_definitions:
        target = additional_definitions

    elif name in definitions:
        target = definitions

    else:
        raise ClopenNameError("Variable does not exist: " + name)


    if _type == "bool":
        value = eval_bool(
            expression,
            definitions,
            additional_definitions,
            inputs
        )
    else:
        value = eval_expr(
            expression,
            definitions,
            additional_definitions,
            inputs
        )


    target[name][0] = value
    target[name][1] = _type

def cmd_get(parts,definitions,additional_definitions=None,inputs=None):

    name = parts[1]
    message = None
    if len(parts) == 3:
        message = parts[2]

    if name not in definitions:
        raise ClopenNameError("Variable does not exist: " + name)

    if message != None:
        value = input(message)
    else:
        value = input("> ")

    _type = definitions[name][1]

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
            raise ClopenValueError("Invalid bool value")

    definitions[name][0] = value

def eval_expr(expression, definitions, additional_definitions=None, inputs=None):

    variables = {}

    if len(expression) == 1:
        return get_value(expression, definitions, additional_definitions, inputs)

    # globals
    for name, data in definitions.items():
        variables[name] = data[0]

    # function locals
    if additional_definitions is not None:
        for name, data in additional_definitions.items():
            variables[name] = data[0]

    # function inputs
    if inputs is not None:
        for name, data in inputs.items():
            variables[name] = data[0]

    try:
        return eval(expression, {"__builtins__": {}}, variables)

    except Exception:
        raise ClopenSyntaxError("Invalid expression: " + expression)

def get_value(value,definitions, additional_definitions=None, inputs=None):

    if value in definitions:
        return definitions[value][0]
    elif additional_definitions is not None and value in additional_definitions:
        return additional_definitions[value][0]
    elif inputs is not None and value in inputs:
        return inputs[value][0]


    if "." in value:
        return float(value)

    return int(value)

def eval_bool(expression, definitions, additional_definitions=None, inputs=None):

    if inputs is not None and expression in inputs:
        value = inputs[expression][0]

        if inputs[expression][1] == "bool":
            return value

    if additional_definitions is not None and expression in additional_definitions:
        value = additional_definitions[expression][0]

        if additional_definitions[expression][1] == "bool":
            return value

    if expression in definitions:
        value = definitions[expression][0]

        if definitions[expression][1] == "bool":
            return value

    if expression == "true":
        return True

    if expression == "false":
        return False

    operators = [
        ">=",
        "<=",
        "==",
        "!=",
        ">",
        "<"
    ]

    for op in operators:
        if op in expression:

            left, right = expression.split(op, 1)

            left = eval_expr(
                left.strip(),
                definitions,
                additional_definitions,
                inputs
            )

            right = eval_expr(
                right.strip(),
                definitions,
                additional_definitions,
                inputs
            )

            if op == ">=":
                return left >= right
            elif op == "<=":
                return left <= right
            elif op == "==":
                return left == right
            elif op == "!=":
                return left != right
            elif op == ">":
                return left > right
            elif op == "<":
                return left < right

    raise ClopenSyntaxError("Invalid bool expression: " + expression)

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

def cmd_return(parts, definitions, additional_definitions=None, inputs=None):
    value = parts[1]

    try:
        value = eval_expr(
            value,
            definitions,
            additional_definitions,
            inputs
        )
    except Exception:
        pass

    if additional_definitions is not None:
        additional_definitions["__return__"] = value

def read_block(program, i):

    block = []
    depth = 1

    while i < len(program):

        line = program[i].strip()

        if "{" in line:
            depth += 1

        if line == "}":
            depth -= 1

            if depth == 0:
                return block, i

        block.append(program[i])
        i += 1

    raise ClopenSyntaxError("Missing closing brace")

def cmd_del(parts, definitions, additional_definitions=None, inputs=None):
    name = parts[1]

    # inputs cannot be deleted
    if inputs is not None and name in inputs:
        raise ClopenValueError("Cannot delete function input: " + name)

    # locals first
    if additional_definitions is not None and name in additional_definitions:
        del additional_definitions[name]
        return

    # globals
    if name in definitions:
        del definitions[name]
        return

    raise ClopenNameError("Variable does not exist: " + name)

def cmd_shalt(in_loop):
    if in_loop:
        return True
    else:
        raise ClopenRuntimeError("Cannot shalt outside of a loop")