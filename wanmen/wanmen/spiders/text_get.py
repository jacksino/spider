def find_text(b):
    if b:
        a=[]
        for i in range(len(b)):
            a.append(b[i].get("text",None))
        return a
    else:
        return None

def find_teacher(b):
    if b:
        a=[]
        a.append(b[0].get("author",None))
        a.append(b[0].get("description",None))
        return a
    else:
        return None
