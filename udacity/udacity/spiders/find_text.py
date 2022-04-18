def find_teachers(a):
    b=[]
    if a:
        for i in range(len(a)):
            b.append(a[i].get("name",None))
        return b
    else:
        return None
def find_lessons(a):
    b = []
    if a:
        for i in range(len(a)):
            b.append(a[i].get("title", None))
            point = a[i].get("points",None)
            for j in range(len(point)):
                b.append(point[j])
        return b
    else:
        return None


