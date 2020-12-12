def objMerger(obj_f1, obj_f2):
    obj1 = open(obj_f1, "r+")
    obj2 = open(obj_f2, "r+")

    v_1 = []
    vn_1 = []
    vt_1 = []
    f_1 = []
    tex_1 = []

    v_2 = []
    vn_2 = []
    vt_2 = []
    f_2 = []
    tex_2 = []

    for line in obj1:
        if line.contains("v "):
            v_1.append(line)
        elif line.contains("vn "):
            vn_1.append(line)
        elif line.contains("vt "):
            vt_1.append(line)
        elif line.contains("f "):
            f_1.append(line)
        elif line.contains(".mtl"):
            tex_1.append(line)
    
    for line in obj2:
        if line.contains("v "):
            v_2.append(line)
        elif line.contains("vn "):
            vn_2.append(line)
        elif line.contains("vt "):
            vt_2.append(line)
        elif line.contains("f "):
            f_2.append(line)
        elif line.contains(".mtl"):
            tex_2.append(line)