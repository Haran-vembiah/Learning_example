def sam_gen():
    for x in range(3):
        yield x

g= sam_gen()
print(next(g))
print(next(g))
print(next(g))
