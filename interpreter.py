from commands import *
from commands_long.with_ import cmd_with

in_loop = False
shalted = False

def run(program,definitions,additional_definitions=None,inputs=None):
    global in_loop, shalted

    for instruction in program:
        if ("__return__" in additional_definitions if additional_definitions is not None else False):
            return
        if "__HALTED__" in definitions:
            return
        if shalted and in_loop:
            return

        if instruction["type"] == "command":

            parts = instruction["parts"]

            command = parts[0]
            if additional_definitions is not None:

                if (command in additional_definitions and additional_definitions[command][1] == "fn"):
                    output = None

                    if len(parts) > 2:
                        output = parts[1]
                        args = parts[2:]
                    else:
                        args = parts[1:]

                    result = call_function(command, args, additional_definitions, inputs)
                    
                    if output and result is not None:
                        if output in additional_definitions:
                            additional_definitions[output] = [
                                result,
                                type(result).__name__
                            ]
                        else:
                            definitions[output] = [
                                result,
                                type(result).__name__
                            ]

                    continue
            else:
                if (command in definitions and definitions[command][1] == "fn"): #type: ignore

                    output = None

                    if len(parts) > 2:
                        output = parts[1]
                        args = parts[2:]
                    else:
                        args = parts[1:]

                    result = call_function(command, args, definitions)

                    if output and result is not None:
                        definitions[output] = [
                            result,
                            type(result).__name__
                        ]

                    continue

            if command == "let":
                cmd_let(parts,definitions,additional_definitions,inputs)

            elif command == "update":
                cmd_update(parts,definitions,additional_definitions,inputs)

            elif command == "log":
                cmd_log(parts,definitions,additional_definitions,inputs)

            elif command == "set":
                cmd_set(parts,definitions,additional_definitions,inputs)

            elif command == "get":
                cmd_get(parts,definitions,additional_definitions,inputs)
            
            elif command == "return":
                cmd_return(parts, definitions, additional_definitions, inputs)

            elif command == "del":
                cmd_del(parts, definitions, additional_definitions, inputs)
            
            elif command == "halt":
                definitions["__HALTED__"] = "stapped"
            
            elif command == "shalt":
                if cmd_shalt(in_loop):
                    shalted = True
                    return
            elif command == "with":
                cmd_with(parts, definitions, run, additional_definitions)


        elif instruction["type"] == "if":
            executed = False

            for branch in instruction["branches"]:
                result = eval_bool(
                    branch["condition"],
                    definitions,
                    additional_definitions,
                    inputs
                )

                if result:
                    run(
                        branch["block"],
                        definitions,
                        additional_definitions,
                        inputs
                    )
                    executed = True
                    break

            if not executed and instruction["else"] is not None:
                run(
                    instruction["else"],
                    definitions,
                    additional_definitions,
                    inputs
                )

        elif instruction["type"] == "while":

            while eval_bool(
                instruction["condition"],
                definitions,
                additional_definitions,
                inputs
            ):
                in_loop = True
                run(
                    instruction["block"],
                    definitions,
                    additional_definitions,
                    inputs
                )
                in_loop = False
                if shalted:
                    shalted = False
                    break


        elif instruction["type"] == "for":

            # initialization
            cmd_let(
                instruction["init"],
                definitions,
                additional_definitions,
                inputs
            )

            while eval_bool(
                instruction["condition"],
                definitions,
                additional_definitions,
                inputs
            ):
                in_loop = True
                run(
                    instruction["block"],
                    definitions,
                    additional_definitions,
                    inputs
                )

                cmd_update(
                    instruction["update"],
                    definitions,
                    additional_definitions,
                    inputs
                )
                in_loop = False
                if shalted:
                    shalted = False
                    break

        elif instruction["type"] == "fn":

            definitions[instruction["name"]] = [
                {
                    "inputs": instruction["inputs"],
                    "block": instruction["block"]
                },
                "fn"
            ]

    return definitions

def call_function(name, args, definitions, output=None):

    function = definitions[name][0]

    local_definitions = {} #definitions.copy()
    inputs = {}

    for input_name, value in zip(function["inputs"], args):
        if value in definitions:
            value = definitions[value][0]
        else:
            value = parse_literal(value)

        inputs[input_name] = [
            value,
            type(value).__name__
        ]

    if inputs != {}:
        run(function["block"], definitions, local_definitions, inputs)
    else:
        run(function["block"], definitions, local_definitions)
    if "__return__" in local_definitions:
        return local_definitions["__return__"]

    return None