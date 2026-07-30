import random

def randint(args, local_definitions):
    random_num = random.randint(int(args[0]),int(args[1]))
    local_definitions["__return__"] = [str(random_num),type(random_num).__name__]

def choice(args, local_definitions):
    random_num = random.choice(args[0])
    local_definitions["__return__"] = [str(random_num),type(random_num).__name__]
    


definitions = {
    "randint": [
        {
            "type": "fn",
            "name": "randint",
            "inputs": ["a", "b"],
            "native": True,
            "function": randint
        },
        "fn"
    ],
    "choice": [
            {
                "type": "fn",
                "name": "choice",
                "inputs": ["seq"],
                "native": True,
                "function": choice
            },
            "fn"
        ]
}