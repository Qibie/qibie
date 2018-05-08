def floatrange(start,stop,steps):
    return [start+float(i)*(stop-start)/(float(steps)-1) for i in range(steps)]


for i in floatrange(25.2,75.72,20):
    print(i)