def run_debug_vars(run, program, definitions):
    defined = definitions.copy()
    for line in program:
        parts = line["parts"]
        if parts[0] == "let":
            print(
                f"created {parts[1]} "
                f"with value '{parts[2]} {parts[3]}'"
            )
            defined = run([line], defined)

        if parts[0] == "update":
            name = parts[1]
            old = defined.get(name, [None])[0]

            defined = run([line], defined)

            new = defined.get(name, [None])[0]
            print(f"{name}: {old} -> {new}")

        else:
            try:
                defined = run([line], defined)
            except Exception as e:
                instruction = "".join(part + " " for part in line["parts"]).strip()
                
                print(
                    f"[Line {line["line"]}] error at '{instruction}' "
                    f"{type(e).__name__}: {e} "
                )

    return defined