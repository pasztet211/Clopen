from errors import *
from helper_functions import *


def get_target(name, definitions, additional_definitions=None, inputs=None):
    if inputs is not None and name in inputs:
        return inputs
    elif additional_definitions is not None and name in additional_definitions:
        return additional_definitions
    elif name in definitions:
        return definitions
    else:
        raise ClopenNameError("Variable does not exist: " + name)


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


def update(parts, definitions, additional_definitions=None, inputs=None):
    name = parts[1]
    operator = parts[2]
    value = parts[3]

    index = None

    if "[" in name and name.endswith("]"):
        name, index = name[:-1].split("[", 1)
        try:
            index = str(int(index))
        except ValueError:
            raise ClopenValueError(f"Cannot use value: {index} as list index")

    target = get_target(
        name,
        definitions,
        additional_definitions,
        inputs
    )

    if inputs is not None and value in inputs:
        value = inputs[value][0]
    elif additional_definitions is not None and value in additional_definitions:
        value = additional_definitions[value][0]
    elif value in definitions:
        value = definitions[value][0]

    old_value, old_type = get_value_type(target, name, index)

    if operator == "+=":
        if old_type == "int":
            if "." in str(value):
                set_value(
                    target,
                    name,
                    float(old_value) + float(value),
                    "float",
                    index
                )
            else:
                set_value(
                    target,
                    name,
                    old_value + int(value),
                    "int",
                    index
                )

        elif old_type == "float":
            set_value(
                target,
                name,
                old_value + float(value),
                "float",
                index
            )

    elif operator == "-=":
        if old_type == "int":
            if "." in str(value):
                set_value(
                    target,
                    name,
                    float(old_value) - float(value),
                    "float",
                    index
                )
            else:
                set_value(
                    target,
                    name,
                    old_value - int(value),
                    "int",
                    index
                )

        elif old_type == "float":
            set_value(
                target,
                name,
                old_value - float(value),
                "float",
                index
            )

    elif operator == "*=":
        if old_type == "int":
            if "." in str(value):
                set_value(
                    target,
                    name,
                    float(old_value) * float(value),
                    "float",
                    index
                )
            else:
                set_value(
                    target,
                    name,
                    old_value * int(value),
                    "int",
                    index
                )

        elif old_type == "float":
            set_value(
                target,
                name,
                old_value * float(value),
                "float",
                index
            )

    elif operator == "/=":
        set_value(
            target,
            name,
            float(old_value) / float(value),
            "float",
            index
        )