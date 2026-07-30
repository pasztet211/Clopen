from clo_loader import load_clo
from interpreter import run
from parser import parse
import sys
from info import HELP_DETAILS
import difflib
from errors import ClopenFileError
import debbuger_clo

VERSION = "0.1.7"
PYTHON_VERSION = "3.14.2"
STATUS = "beta"

commands = [
    "let",
    "get",
    "log",
    "del",
    "update",
    "set",
    "halt",
    "shalt",
    "return",
    "if",
    "elif",
    "else",
    "fn",
    "with"
]

def suggest_command(name):
    matches = difflib.get_close_matches(
        name,
        commands,
        n=3,
        cutoff=0.5
    )

    if matches:
        print(f"Unknown command: {name}")
        print("Did you mean:")
        for match in matches:
            print(f"    {match}")
    else:
        print(f"Unknown command: {name}")

HELP = """\
Usage: clopen [filename.clo] [-h <command> | --help <command>] [-v <command> | --version <command>] or \nclopen [-d | --debug] [mode (check 'clopen --help --debug')] [filename.clo]

common commands
    let     create a variable "let var val type"
    log     print a value to terminal "log value"
    del     delete a variable "del var"
    get     get value for var from user "get var "optional message""
    halt    stop the program "halt"
    shalt   stop current loop "shalt"
    return  returns variable or expression result from function "return var"
    update  updates the value of a variable "update var "expression""
    set     sets the value and type of an existing variable "set var val type"

list commands
    add.to  adds value to end of start of or an index of a list "add 0 int to start-of list"

conditionals
    if      executes code if connected condition is true "if (expr) {}"
    elif    executes code if connected condition is true and all previous conditions were false "elif (expr) {}"
    else    executes code if all previous conditions were false "else {}"

functions
    fn      creates a function "fn name (input1,input2) {}"

imports/modules
    with           imports file "with filename"
    from + with    imports selected module items "with x from filename"
    from + as      imports file using a selected name "with filename as nickname"
"""

if len(sys.argv) < 2:
    print("Usage: clopen [filename.clo] [-h <command> | --help <command>] [-v <command> | --version <command>] or \nclopen [-d | --debug] [mode (check 'clopen --help --debug')] [filename.clo]")
    exit()

if sys.argv[1] == "--version" or sys.argv[1] == "-v":
    if len(sys.argv) < 3:
        print(f"Clopen {VERSION} \npython interpreter {PYTHON_VERSION}\nstatus {STATUS}")
    else:
        if sys.argv[2] == "clopen":
            print(f"Clopen {VERSION}")
        elif sys.argv[2] == "interpreter":
            print(f"python interpreter {PYTHON_VERSION}")
        elif sys.argv[2] == "status":
            print(f"status {STATUS}")
        else:
            raise Exception("Invalid version parameter")
    exit()
    
elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
    if len(sys.argv) < 3:
        print(HELP)
    else:
        try:
            print(HELP_DETAILS[sys.argv[2]])
        except KeyError:
            suggest_command(sys.argv[2])
    exit()

if sys.argv[1] == "--debug" or sys.argv[1] == "-d":
    if len(sys.argv) > 2 and sys.argv[2] == "--basic":
        if len(sys.argv) < 4:
            raise ClopenFileError("Must have file parameter")
        filename = sys.argv[3]

        if not filename.endswith(".clo"):
            raise ClopenFileError("File must have .clo extension")

        definitions = {}
    
        program = load_clo(filename)
        
        instructions = parse(program)
        #print(instructions)
        debbuger_clo.run_debug_basic(run, instructions, definitions, False)
        exit()
    elif len(sys.argv) > 2 and sys.argv[2] == "--vars":
        if len(sys.argv) < 4:
            raise ClopenFileError("Must have file parameter")
        filename = sys.argv[3]
        
        if not filename.endswith(".clo"):
            raise ClopenFileError("File must have .clo extension")
        
        definitions = {}
            
        program = load_clo(filename)
                
        instructions = parse(program)
        #print(instructions)
        debbuger_clo.run_debug_vars(run, instructions, definitions)
        exit()
    else:
        if len(sys.argv) < 3:
            raise ClopenFileError("Must have file parameter")
        filename = sys.argv[2]

        if not filename.endswith(".clo"):
            raise ClopenFileError("File must have .clo extension")

        definitions = {}
        
        program = load_clo(filename)
        
        instructions = parse(program)
        #print(instructions)
        debbuger_clo.debug(run, instructions)
        exit()
else:
    filename = sys.argv[1]
 
    if not filename.endswith(".clo"):
        raise ClopenFileError("File must have .clo extension")

    definitions = {}

    program = load_clo(filename)

    instructions = parse(program)
    #print(instructions)
    run(instructions, definitions)