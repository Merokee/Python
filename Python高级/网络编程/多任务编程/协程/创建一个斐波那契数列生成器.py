def fibGenerator(n):
    a = 0
    b = 1
    i = 0
    while i < n:
        yield a
        a, b = b, a + b
        i += 1
    else:
        raise StopIteration


generator = fibGenerator(10)
for x in generator:
    print(x)
    
