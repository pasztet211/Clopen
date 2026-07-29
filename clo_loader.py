def load_clo(filename):

    code = []

    with open(filename, 'r') as program:
        i = 0
        for line in program:
            i += 1
            line = line.strip()
            if line.startswith("#") or line.startswith("//"):
                continue
            if not line:
                continue

            code.append(line + " " + str(i))
    
    return code