def run_debug_vars(run, program, definitions):
    defined = definitions.copy()

    for line in program:
        before = {k: v.copy() if isinstance(v, list) else v
                  for k, v in defined.items()}

        try:
            defined = run([line], defined)
        except Exception as e:
            instruction = " ".join(line["parts"])
            print(
                f"[Line {line['line']}] error at '{instruction}' "
                f"{type(e).__name__}: {e}"
            )
            continue

        # New variables
        for name in defined:
            if defined[name][1] == "fn":
                continue
            if name not in before:
                print(f"+ {name}: {defined[name][0]} ({defined[name][1]})")

        # Modified variables
        for name in before:
            if name in defined and before[name] != defined[name]:
                print(f"~ {name}: {before[name][0]} -> {defined[name][0]}")

        # Deleted variables
        for name in before:
            if name not in defined:
                print(f"- {name}")

    return defined