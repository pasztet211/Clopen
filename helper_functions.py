from errors import *

def get_index_value(name, definitions, additional_definitions=None, inputs=None):
    name_, index = name[:-1].split("[", 1)

    if inputs is not None and name_ in inputs:
        target = inputs

    elif additional_definitions is not None and name_ in additional_definitions:
        target = additional_definitions

    elif name_ in definitions:
        target = definitions

    else:
        raise ClopenNameError(f"[Line {Error_line}] Variable does not exist: " + name_)

    index = str(int(index))

    return target[name_][0][index][0]

def get_index_val_typ(name, definitions, additional_definitions=None, inputs=None):
    name_, index = name[:-1].split("[", 1)

    if inputs is not None and name_ in inputs:
        target = inputs

    elif additional_definitions is not None and name_ in additional_definitions:
        target = additional_definitions

    elif name_ in definitions:
        target = definitions

    else:
        raise ClopenNameError(f"[Line {Error_line}] Variable does not exist: " + name_)

    index = str(int(index))

    return target[name_][0][index][0], target[name_][0][index][1]


def get_index_name(name):
    name_, index = name[:-1].split("[", 1)
    try:
        return int(index), name_
    except ValueError:
        raise ClopenValueError(f"[Line {Error_line}] Cannnot use value: {index} as list index")

def read_block(program, i, line):

    block = []
    depth = 1

    program_no_line = [
        " ".join(line.split()[:-1])
        for line in program
    ]

    while i < len(program_no_line):

        line = program_no_line[i].strip()

        if "{" in line:
            depth += 1

        if line == "}":
            depth -= 1

            if depth == 0:
                return block, i

        block.append(program[i])
        i += 1

    raise ClopenSyntaxError(f"[Line {line}] Statement missing closing brace")

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

    if "[" in expression and expression.endswith("]"):
        expression = get_index_value(
            expression,
            definitions,
            additional_definitions,
            inputs
        )

        return expression

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

    raise ClopenSyntaxError(f"[Line {Error_line}] Invalid bool expression: " + expression)


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

def get_val_typ(value,definitions, additional_definitions=None, inputs=None):
    if inputs is not None and value in inputs:
        return inputs[value][0] ,inputs[value][1]
    elif value in definitions:
        return definitions[value][0], definitions[value][1]
    elif additional_definitions is not None and value in additional_definitions:
        return additional_definitions[value][0], additional_definitions[value][1]

    if "." in value:
        return float(value), "float"

    return int(value), "int"

def eval_expr(expression, definitions, additional_definitions=None, inputs=None):

    variables = {}
    expression = handle_lists(
        expression,
        definitions,
        additional_definitions,
        inputs
    )
    if len(expression) == 1:
        return get_value(expression, definitions, additional_definitions, inputs)

    # globals
    for name, data in definitions.items():
        if data[1] != "list":
            variables[name] = data[0]

    if additional_definitions is not None:
        for name, data in additional_definitions.items():
            if data[1] != "list":
                variables[name] = data[0]

    if inputs is not None:
        for name, data in inputs.items():
            if data[1] != "list":
                variables[name] = data[0]

    try:
        return eval(expression, {"__builtins__": {}}, variables)

    except Exception:
        raise ClopenSyntaxError(f"[Line {Error_line}] Invalid expression: " + expression)

    
def get_var_from_definitions(name, definitions, additional_definitions=None, inputs=None):
    if inputs is not None and name in inputs:
        return inputs[name][0]

    elif additional_definitions is not None and name in additional_definitions:
        return additional_definitions[name][0]

    elif name in definitions:
        return definitions[name][0]

    else:
        raise ClopenNameError(f"[Line {Error_line}] Variable does not exist: " + name)

def get_target(name, definitions, additional_definitions=None, inputs=None):
    index = None

    if "[" in name and name.endswith("]"):
        name, index = name[:-1].split("[", 1)
        try:
            index = str(int(index))
        except ValueError:
            raise ClopenValueError(f"[Line {Error_line}] Cannot use value: {index} as list index")

    if inputs is not None and name in inputs:
        target = inputs
    elif additional_definitions is not None and name in additional_definitions:
        target = additional_definitions
    elif name in definitions:
        target = definitions
    else:
        raise ClopenNameError(f"[Line {Error_line}] Variable does not exist: " + name)

    return target, name, index

def get_target_nl(name, definitions, additional_definitions=None, inputs=None):
    if inputs is not None and name in inputs:
        target = inputs
    elif additional_definitions is not None and name in additional_definitions:
        target = additional_definitions
    elif name in definitions:
        target = definitions
    else:
        raise ClopenNameError(f"[Line {Error_line}] Variable does not exist: " + name)

    return target
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

def handle_lists(expression, definitions, additional_definitions=None, inputs=None):
    containers = [definitions, additional_definitions, inputs]

    while True:
        replaced = False

        for container in containers:
            if container is None:
                continue

            for name, data in container.items():
                if data[1] == "list":
                    if f"{name}[" in expression:
                        start = expression.find(name + "[")
                        end = expression.find("]", start)

                        if start != -1 and end != -1:
                            list_index = expression[start:end + 1]

                            value = get_index_value(
                                list_index,
                                definitions,
                                additional_definitions,
                                inputs
                            )

                            expression = expression.replace(
                                list_index,
                                str(value),
                                1
                            )

                            replaced = True
                            break

                    elif name in expression:
                        raise ClopenTypeError(
                            f"[Line {Error_line}] Cannot use list without an index: " + name
                        )

            if replaced:
                break

        if not replaced:
            break

    return expression

def is_imported(name):
    return "." in name