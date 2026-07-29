def run_debug_vars(run, program, definitions):
    defined = definitions.copy()
    for line in program:
        parts = line["parts"]
        if parts[0] == "let":
            print(
                f"created {parts[1]} "
                f"with value '{parts[2]} {parts[3]}'"
            )

        if parts[0] == "update":
            name = parts[1]
            old = defined.get(name, [None])[0]

            defined = run([line], defined)

            new = defined.get(name, [None])[0]
            print(f"{name}: {old} -> {new}")

        else:
            defined = run([line], defined)

    return defined