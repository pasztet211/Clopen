HELP_DETAILS = {
    "let": """\
let - creates a variable

Syntax:
    let name value type

Example:
    let age 10 int
""",

    "log": """\
log - prints a value to the terminal

Syntax:
    log value

Example:
    log "Hello"
    log $variable
""",

    "del": """\
del - deletes a variable

Syntax:
    del name

Example:
    del age
""",

    "get": """\
get - gets a value from the user and stores it in a variable

Syntax:
    get name "optional message"

Example:
    get age "Enter age: "
""",

    "update": """\
update - updates the value of a variable

Syntax:
    update name operator value

Example:
    update age += 1
""",

    "set": """\
set - changes the value and type of an existing variable

Syntax:
    set name value type

Example:
    set age 20 int
""",

    "halt": """\
halt - stops program execution

Syntax:
    halt
""",

    "shalt": """\
shalt - stops the current loop

Syntax:
    shalt
""",

    "return": """\
return - returns a value from a function

Syntax:
    return value

Example:
    return result
""",

    "if": """\
if - executes code when a condition is true

Syntax:
    if (expression) {}

Example:
    if (x > 5) {}
""",

    "elif": """\
elif - executes code when previous conditions failed
and this condition is true

Syntax:
    elif (expression) {}
""",

    "else": """\
else - executes code when all previous conditions failed

Syntax:
    else {}
""",

    "fn": """\
fn - creates a function

Syntax:
    fn name (inputs) {}

Example:
    fn add (a,b) {}
""",

    "with": """\
with - imports another Clopen file

Syntax:
    with filename
    with item from filename
    with filename as nickname

Examples:
    with math
    with pi from math
    with math as m
""",

    "add.to": """\
add.to - adds value to a list

Syntax
    add x type to start-of list
    add x type to end-of list
    add x type to index-[index] list

Examples
    add 20 int to end-of nums
    add "he" str to start-of pronouns
""",

    "--debug": """\
clopen --debug | -d <filename>   opens debugger in selected mode for selected file

Modes
    --basic
        Runs the basic debugger.
        Shows errors and continues execution after failures.

Examples
    clopen --debug --basic test.clo
""",

    "-d": """\
clopen --debug | -d <filename>   opens debugger in selected mode for selected file

Modes
    --basic
        Runs the basic debugger.
        Shows errors and continues execution after failures.

Examples
    clopen --debug --basic test.clo
"""
}