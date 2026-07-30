from . import debug_basic, debug_vars

def debug(run,program):
    definitions = {}
    index = 0
    debug_vars.run_debug_vars(run,[program[index]],definitions,False)
    error, definitions = debug_basic.run_debug_basic(run,[program[index]],definitions,return_error=True) #type: ignore
    while True:
        op = input("n - next line\n> ")
        if op == "n":
            index += 1
        debug_vars.run_debug_vars(run,[program[index]],definitions,False)
        error, definitions = debug_basic.run_debug_basic(run,[program[index]],definitions,return_error=True) #type: ignore
        if error is not None:
            print(error)
            