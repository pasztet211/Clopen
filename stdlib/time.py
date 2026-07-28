import time

_start = time.perf_counter_ns()

def get_time(args, local_variables):
    ms = (time.perf_counter_ns() - _start) // 1_000_000
    local_variables["__return__"] = [str(ms), "int"]


def hello(args, local_variables):
    local_variables["__return__"] = ["Hello from Python", "str"]

def sleep(args, local_variables):
    time.sleep(int(args[0]) / 1000)


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
    ],

    "time": [
        {
            "type": "fn",
            "name": "time",
            "inputs": [],
            "native": True,
            "function": get_time
        },
        "fn"
    ],
    "sleep": [
        {
            "type": "fn",
            "name": "sleep",
            "inputs": [],
            "native": True,
            "function": sleep
        },
        "fn"
    ]
}