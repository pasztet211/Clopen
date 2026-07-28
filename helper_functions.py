from errors import *

def get_index_value(name, definitions, additional_definitions=None, inputs=None):
    name_, index = name[:-1].split("[", 1)

    if name_ not in definitions or (additional_definitions is not None and name_ not in additional_definitions):
        raise ClopenNameError("Variable does not exist: " + name_)

    index = str(int(index))

    if additional_definitions is not None and name_ in additional_definitions:
        return additional_definitions[name_][0][index]
    else:
        return definitions[name_][0][index][0]

def get_index_name(name):
    name_, index = name[:-1].split("[", 1)
    try:
        return int(index), name_
    except ValueError:
        raise ClopenValueError(f"Cannnot use value: {index} as list index")

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


def get_value(value,definitions, additional_definitions=None, inputs=None):
    if inputs is not None and value in inputs:
        return inputs[value][0]
    elif value in definitions:
        return definitions[value][0]
    elif additional_definitions is not None and value in additional_definitions:
        return additional_definitions[value][0]

    if "." in value:
        return float(value)

    return int(value)

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

    
def get_var_from_definitions(name, definitions, additional_definitions=None, inputs=None):
    if inputs is not None and name in inputs:
        return inputs[name][0]

    elif additional_definitions is not None and name in additional_definitions:
        return additional_definitions[name][0]

    elif name in definitions:
        return definitions[name][0]

    else:
        raise ClopenNameError("Variable does not exist: " + name)

def get_target(name, definitions, additional_definitions=None, inputs=None):
    index = None

    if "[" in name and name.endswith("]"):
        name, index = name[:-1].split("[", 1)
        try:
            index = str(int(index))
        except ValueError:
            raise ClopenValueError(f"Cannot use value: {index} as list index")

    if inputs is not None and name in inputs:
        target = inputs
    elif additional_definitions is not None and name in additional_definitions:
        target = additional_definitions
    elif name in definitions:
        target = definitions
    else:
        raise ClopenNameError("Variable does not exist: " + name)

    return target, name, index

def get_value_type(container, name, index=None):
    if index is not None:
        return container[name][0][index][0], container[name][0][index][1]
    return container[name][0], container[name][1]


def set_value(container, name, value, _type, index=None):
    if index is not None:
        container[name][0][index][0] = value
        container[name][0][index][1] = _type
    else:
        container[name][0] = value
        container[name][1] = _type