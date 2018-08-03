class fibIterator:
    def __init__(self, n):
        self.a = 0
        self.b = 1
        self.i = 0
        self.n = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.n:
            self.a, self.b = self.b, self.a + self.b
            self.i += 1
            return self.a
        else:
            raise StopIteration


iterator = fibIterator(10)
for x in iterator:
    print(x)
