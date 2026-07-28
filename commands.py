from commands_long.let import let
from errors import *
from commands_long.update import update
from helper_functions import *

def cmd_let(parts,definitions,additional_definitions=None,inputs=None):
    let(parts, definitions, additional_definitions, inputs)

def cmd_update(parts,definitions,additional_definitions=None,inputs=None):
    update(parts,definitions,additional_definitions,inputs)

def cmd_log(parts,definitions,additional_definitions=None,inputs=None):
    name = parts[1]
    if inputs is not None and name in inputs:
        _type = inputs[name][1]
        value = inputs[name][0]
    elif additional_definitions is not None and name in additional_definitions:
        _type = additional_definitions[name][1]
        value = additional_definitions[name][0]
    else:
        _type = definitions[name][1]
        value = definitions[name][0]
    
    if "[" in name and name.endswith("]"):
        print(get_index_value(name,definitions,additional_definitions,inputs))
    else:
        if name.startswith("\"") and name.endswith("\""):
            if not name[1:-1] == '\\n':
                print(name[1:-1])
            else:
                print()
            return
        
        elif name.startswith("$"):
            print(get_var_from_definitions(name[1:], definitions, additional_definitions, inputs))
            return
        elif _type == "list":
            output = []

            for index in sorted(value.keys(), key=int):
                item, item_type = value[index]

                if item_type == "bool":
                    output.append("true" if item else "false")
                else:
                    output.append(str(item))

            print("[" + ",".join(output) + "]")
        else:
            if inputs is not None and name in inputs:
                print(inputs[name][0])

            elif additional_definitions is not None and name in additional_definitions:
                print(additional_definitions[name][0])

            elif name in definitions:
                print(definitions[name][0])
            
            else:
                if name == '\\n':
                    print()
                    return
                print(name)

def cmd_set(parts, definitions, additional_definitions=None, inputs=None):
    name = parts[1]
    expression = parts[2]
    _type = parts[3]
    index = None

    if "[" in name and name.endswith("]"):
        index, name = get_index_name(name)

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

    if index is not None:
        target[name][0][str(index)][0] = value
        target[name][0][str(index)][1] = _type
    else:
        target[name][0] = value
        target[name][1] = _type

def cmd_get(parts,definitions,additional_definitions=None,inputs=None):

    name = parts[1]
    message = None
    if len(parts) == 3:
        message = parts[2]

    index = None
    target,name,index = get_target(name,definitions,additional_definitions,inputs)
        
    if name not in target and target is not None:
        raise ClopenNameError("Variable does not exist: " + name)

    if message != None:
        value = input(message)
    else:
        value = input("> ")

    if index is None and target is not None:
        _type = target[name][1]
    elif target is not None:
        _type = target[name][0][index][1]

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
        
    if index is None and target is not None:
        target[name][0] = value
    elif target is not None:
        target[name][0][index][0] = value

def cmd_return(parts, definitions, additional_definitions=None, inputs=None):
    value = parts[1]

    try:
        value = eval_expr(
            value,
            definitions,
            additional_definitions,
            inputs
        )
        _type = type(value).__name__
    except Exception: 
        if "[" in value and value.endswith("]"): #type: ignore
            value,_type = get_index_val_typ(
                value,
                definitions,
                additional_definitions,
                inputs
            )
        else:
            value,_type = get_val_typ(
                value,
                definitions,
                additional_definitions,
                inputs
            )

    if additional_definitions is not None:
        additional_definitions["__return__"] = value,_type

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