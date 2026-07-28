import shlex
from commands import read_block
import time

def parse(program):

    instructions = []

    i = 0

    while i < len(program):

        line = program[i].strip()

        if line.startswith("log "):
            parts = split_line(line)
        elif line.startswith("let "):
            parts = split_line(line)
        else:
            parts = tokenize(line)

        if parts[0] == "if":

            branches = []

            condition = get_condition(parts)

            block, i = read_block(program, i + 1)
                
            branches.append({
                "condition": condition,
                "block": parse(block)
            })

            else_block = None

            # check what comes after the }
            i += 1

            while i < len(program):

                next_line = program[i].strip()
                next_parts = tokenize(next_line)

                if next_parts[0] == "elif":

                    condition = get_condition(next_parts)

                    block, i = read_block(program, i + 1)

                    branches.append({
                        "condition": condition,
                        "block": parse(block)
                    })

                    i += 1

                elif next_parts[0] == "else":

                    block, i = read_block(program, i + 1)

                    else_block = parse(block)
                    i += 1
                    break

                else:
                    i -= 1
                    break


            instructions.append({
                "type": "if",
                "branches": branches,
                "else": else_block
            })
        elif parts[0] == "while":

            condition = get_condition(parts)

            block, i = read_block(program, i + 1)

            instructions.append({
                "type": "while",
                "condition": condition,
                "block": parse(block)
            })
        elif parts[0] == "for":

            data = get_condition(parts).split(";")

            init = shlex.split(data[0].strip())
            condition = data[1].strip()
            update = ["update"] + shlex.split(data[2].strip())

            block, i = read_block(program, i + 1)

            instructions.append({
                "type": "for",
                "init": init,
                "condition": condition,
                "update": update,
                "block": parse(block)
            })
        elif parts[0] == "fn":

            name = parts[1]

            inputs = get_condition(parts,2).split(",")

            block, i = read_block(program, i + 1)

            instructions.append({
                "type": "fn",
                "name": name,
                "inputs": [x.strip() for x in inputs if x.strip()],
                "block": parse(block)
            })
        else:
            instructions.append({
                "type": "command",
                "parts": parts
            })
        i += 1

    return instructions

def split_line(line):
    parts = []
    current = ""
    in_quotes = False
    encountered_escape = False

    for char in line:
        if char == '"':
            in_quotes = not in_quotes
            current += char
        elif char == " " and not in_quotes:
            if current:
                parts.append(current)
                current = ""
        elif char == "#" and not in_quotes:
            break
        elif char == "\\" and not in_quotes:
            if not encountered_escape:
                encountered_escape = True
            else:
                break
        else:
            encountered_escape = False
            current += char

    if current:
        parts.append(current)

    return parts

def get_condition(parts,index=1):
    if "(" in parts:
        start = parts.index("(")
        end = parts.index(")")
        return " ".join(parts[start + 1:end])
    else:
        return parts[index]

def tokenize(line):
    line = line.replace("(", " ( ")
    line = line.replace(")", " ) ")
    return shlex.split(line)