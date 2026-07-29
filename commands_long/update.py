from errors import *
from helper_functions import *

def update(parts, definitions, additional_definitions=None, inputs=None):
    name = parts[1]
    if is_imported(name):
        raise ClopenReadonlyError("cannot modify imported value")
    operator = parts[2]
    value = parts[3]

    index = None

    if "[" in name and name.endswith("]"):
        name, index = name[:-1].split("[", 1)
        try:
            index = str(int(index))
        except ValueError:
            raise ClopenValueError(f"Cannot use value: {index} as list index")

    target, name, index = get_target(
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