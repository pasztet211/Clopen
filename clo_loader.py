def load_clo(filename):

    code = []

    with open(filename, 'r') as program:
        for line in program:
            line = line.strip()
            if line.startswith("#") or line.startswith("//"):
                continue
            if not line:
                continue

            code.append(line)
    
    return code