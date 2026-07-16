from clo_loader import load_clo
from interpreter import run
from parser import parse
import sys
from interpreter import run

if len(sys.argv) < 2:
    print("Usage: python main.py file.clo")
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