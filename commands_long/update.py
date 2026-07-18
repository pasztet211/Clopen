from errors import *

def update(parts,definitions,additional_definitions=None,inputs=None):
    name = parts[1]
    operator = parts[2]
    value = parts[3]

    if inputs is not None and name in inputs:
        # it's a function parameter
        pass

    elif additional_definitions is not None and name in additional_definitions:
        # it's a local variable
        pass

    elif name in definitions:
        # it's a global variable
        pass

    else:
        raise ClopenNameError("Variable does not exist: " + name)
    
    if inputs is not None and value in inputs:
        value = inputs[value][0]

    elif additional_definitions is not None and value in additional_definitions:
        value = additional_definitions[value][0]

    elif value in definitions:
        value = definitions[value][0]

    if operator == "+=":
        if additional_definitions is not None: 
            if inputs is not None and name in inputs:
                old_value, old_type = inputs[name]
            elif name in additional_definitions:
                old_value, old_type = additional_definitions[name]
            elif name in definitions:
                old_value, old_type = definitions[name]
        else:
            old_value, old_type = definitions[name]

        if old_type == "int":
            if additional_definitions is not None:
                if inputs is not None and name in inputs:
                    if "." in str(value):
                        inputs[name][0] = float(old_value) + float(value)
                        inputs[name][1] = "float"
                    else:
                        inputs[name][0] += int(value)
                elif name in additional_definitions:
                    if "." in str(value):
                        additional_definitions[name][0] = float(old_value) + float(value)
                        additional_definitions[name][1] = "float"
                    else:
                        additional_definitions[name][0] += int(value)
                else:
                    if "." in str(value):
                        definitions[name][0] = float(old_value) + float(value)
                        definitions[name][1] = "float"
                    else:
                        definitions[name][0] += int(value)
            else:
                if "." in str(value):
                    definitions[name][0] = float(old_value) + float(value)
                    definitions[name][1] = "float"
                else:
                    definitions[name][0] += int(value)

        elif old_type == "float":
            if additional_definitions is not None:
                if inputs is not None and name in inputs:
                    inputs[name][0] += float(value)
                else:
                    additional_definitions[name][0] += float(value)
            else:
                definitions[name][0] += float(value)
    if operator == "-=":
        if inputs is not None and name in inputs:
            old_value, old_type = inputs[name]

        elif additional_definitions is not None and name in additional_definitions:
            old_value, old_type = additional_definitions[name]

        elif name in definitions:
            old_value, old_type = definitions[name]

        else:
            raise ClopenNameError("Variable does not exist: " + name)
        
        if old_type == "int":
            if additional_definitions is not None:
                if inputs is not None and name in inputs:
                    if "." in str(value):
                        inputs[name][0] = float(old_value) - float(value)
                        inputs[name][1] = "float"
                    else:
                        inputs[name][0] -= int(value)

                elif name in additional_definitions:
                    if "." in str(value):
                        additional_definitions[name][0] = float(old_value) - float(value)
                        additional_definitions[name][1] = "float"
                    else:
                        additional_definitions[name][0] -= int(value)

                else:
                    if "." in str(value):
                        definitions[name][0] = float(old_value) - float(value)
                        definitions[name][1] = "float"
                    else:
                        definitions[name][0] -= int(value)

            else:
                if "." in str(value):
                    definitions[name][0] = float(old_value) - float(value)
                    definitions[name][1] = "float"
                else:
                    definitions[name][0] -= int(value)

        elif old_type == "float":
            if additional_definitions is not None:
                if inputs is not None and name in inputs:
                    inputs[name][0] -= float(value)
                elif name in additional_definitions:
                    additional_definitions[name][0] -= float(value)
                else:
                    definitions[name][0] -= float(value)

            else:
                definitions[name][0] -= float(value)
    if operator == "*=":
        if inputs is not None and name in inputs:
            old_value, old_type = inputs[name]
        elif additional_definitions is not None and name in additional_definitions:
            old_value, old_type = additional_definitions[name]
        elif name in definitions:
            old_value, old_type = definitions[name]
        else:
            raise ClopenNameError("Variable does not exist: " + name)

        if old_type == "int":
            if "." in str(value):
                if inputs is not None and name in inputs:
                    inputs[name][0] = float(old_value) * float(value)
                    inputs[name][1] = "float"
                elif additional_definitions is not None and name in additional_definitions:
                    additional_definitions[name][0] = float(old_value) * float(value)
                    additional_definitions[name][1] = "float"
                else:
                    definitions[name][0] = float(old_value) * float(value)
                    definitions[name][1] = "float"
            else:
                if inputs is not None and name in inputs:
                    inputs[name][0] *= int(value)
                elif additional_definitions is not None and name in additional_definitions:
                    additional_definitions[name][0] *= int(value)
                else:
                    definitions[name][0] *= int(value)

        elif old_type == "float":
            if inputs is not None and name in inputs:
                inputs[name][0] *= float(value)
            elif additional_definitions is not None and name in additional_definitions:
                additional_definitions[name][0] *= float(value)
            else:
                definitions[name][0] *= float(value)
    if operator == "/=":
        if inputs is not None and name in inputs:
            old_value, old_type = inputs[name]
        elif additional_definitions is not None and name in additional_definitions:
            old_value, old_type = additional_definitions[name]
        elif name in definitions:
            old_value, old_type = definitions[name]
        else:
            raise ClopenNameError("Variable does not exist: " + name)

        if old_type == "int":
            if inputs is not None and name in inputs:
                inputs[name][0] = float(old_value) / float(value)
                inputs[name][1] = "float"
            elif additional_definitions is not None and name in additional_definitions:
                additional_definitions[name][0] = float(old_value) / float(value)
                additional_definitions[name][1] = "float"
            else:
                definitions[name][0] = float(old_value) / float(value)
                definitions[name][1] = "float"

        elif old_type == "float":
            if inputs is not None and name in inputs:
                inputs[name][0] /= float(value)
            elif additional_definitions is not None and name in additional_definitions:
                additional_definitions[name][0] /= float(value)
            else:
                definitions[name][0] /= float(value)
