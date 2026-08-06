def replace_char(args, local_definitions):
    text = args[0]
    pos = int(args[1])
    char = args[2]

    result = text[:pos] + char + text[pos+1:]

    local_definitions["__return__"] = [str(result), "str"]


def length(args, local_definitions):
    result = len(args[0])

    local_definitions["__return__"] = [str(result), "int"]

def get_char(args, local_definitions):
    result = args[0][int(args[1])]

    local_definitions["__return__"] = [str(result), "str"]

definitions = {
    "replace_char": [
        {
            "type": "fn",
            "name": "replace_char",
            "inputs": ["text", "pos", "char"],
            "native": True,
            "function": replace_char
        },
        "fn"
    ],
    "length": [
        {
            "type": "fn",
            "name": "length",
            "inputs": ["text"],
            "native": True,
            "function": length
        },
        "fn"
    ],
    "get_char": [
        {
            "type": "fn",
            "name": "get_char",
            "inputs": ["text","pos"],
            "native": True,
            "function": get_char
        },
        "fn"
    ]
}