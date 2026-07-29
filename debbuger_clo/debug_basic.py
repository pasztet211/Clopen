def run_debug_basic(run,program,definitions):
    for line in program:
        try:
            definitions = run([line],definitions)
        except Exception as e:
            instruction = "".join(part + " " for part in line["parts"]).strip()

            print(
                f"[Line {line["line"]}] error at '{instruction}' "
                f"{type(e).__name__}: {e} "
            )