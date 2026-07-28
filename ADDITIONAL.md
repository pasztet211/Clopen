# Guide to making a .py extension for Clopen

## 1. Create file

- Your file should have a name reflecting what the extension does, eg. `time.py`.
- The filename cannot contain `.` characters.

## 2. Write file

- The file must contain a `definitions` dictionary.

### Functions

- Each function must have only `args` and `local_variables` parameters.

- `args` contains the arguments passed from Clopen.
- `local_variables` is used to return values to Clopen.

To return a value from a function, set `__return__`:

```py
local_definitions["__return__"] = [
    returned_value,
    type(returned_value).__name__
]
```

- For each function you want to make available, add an entry to `definitions` and make the function:

```py
def function_object(args,local_variables):
    pass

"used_name": [
    {
        "type": "fn",
        "name": "used_name",
        "inputs": [],
        "native": True,
        "function": function_object
    },
    "fn"
]
```

#### Function Example:

```py
def hello(args, local_variables):
    local_variables["__return__"] = [
        "Hello from Python!",
        "str"
    ]

definitions = {
    "hello": [
        {
            "type": "fn",
            "name": "hello",
            "inputs": [],
            "native": True,
            "function": hello
        },
        "fn"
    ]
}
```

### Constants

- to add a constant you only need to add an entry to `definitions`:

```py
definitions = {
    "CONSTANT_NAME": [str(value), type(value).__name__]
}
```
