from clo_loader import load_clo
from interpreter import run
from parser import parse
import sys

HELP = """\
Usage: clopen [-h | --help] [-v | --version]

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

conditionals
    if      executes code if connected condition is true "if "expr" {}"
    elif    executes code if connected condition is true and all previous conditions were false "elif "expr" {}"
    else    executes code if all previous conditions were false "else {}"

functions
    fn      creates a function "fn name "inputs" {}"

imports/modules
    with           imports file "with filename"
    from + with    imports selected module items "with x from filename"
    from + as      imports file using a selected name "with filename as nickname"
"""

if len(sys.argv) < 2:
    print("Usage: python main.py file.clo")
    exit()

if sys.argv[1] == "--version" or sys.argv[1] == "-v":
    print("Clopen 0.1.3 \npython interpreter 3.13.12\nstatus beta")
    exit()
    
elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
    print(HELP)
    exit()
filename = sys.argv[1]

if not filename.endswith(".clo"):
    print("Error: file must be .clo")
    exit()

definitions = {}

program = load_clo(filename)

instructions = parse(program)
#print(instructions)
run(instructions, definitions)