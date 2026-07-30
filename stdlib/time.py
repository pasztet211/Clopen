import time

_start = time.perf_counter_ns()

def get_time(args, local_variables):
    if args[0] == "microseconds":
        ms = (time.perf_counter_ns() - _start) // 1_000
    elif args[0] == "seconds":
        ms = (time.perf_counter_ns() - _start) // 1_000_000_000
    elif args[0] == "nanoseconds":
        ms = (time.perf_counter_ns() - _start)
    else:
        ms = (time.perf_counter_ns() - _start) // 1_000_000
    local_variables["__return__"] = [str(ms), "int"]

def sleep(args, local_variables):
    time.sleep(int(args[0]) / 1000)


definitions = {
    "time": [
        {
            "type": "fn",
            "name": "time",
            "inputs": ["type"],
            "native": True,
            "function": get_time
        },
        "fn"
    ],
    "sleep": [
        {
            "type": "fn",
            "name": "sleep",
            "inputs": ["miliseconds"],
            "native": True,
            "function": sleep
        },
        "fn"
    ]
}