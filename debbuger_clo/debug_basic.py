def run_debug_basic(run,program,definitions,return_error=False):
    for line in program:
        try:
            definitions = run([line],definitions)
        except Exception as e:
            if not return_error:
                instruction = "".join(part + " " for part in line["parts"]).strip()

                print(
                    f"[Line {line["line"]}] error at '{instruction}' ",
                    f"{type(e).__name__}: {e} "
                )
            else:
                instruction = "".join(part + " " for part in line["parts"]).strip()
                return f"[Line {line["line"]}] error at '{instruction}'" + f"{type(e).__name__}: {e} ", definitions

    return None, definitions