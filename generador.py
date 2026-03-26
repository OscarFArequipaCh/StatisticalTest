# datos Unix
# a = 1103515245
# c = 12345
# m = 2**32
# x0 = 111 
class LCG:
    def __init__(self, x0, a, c, m):
        self.x0 = x0
        self.x_n = x0
        self.a = a
        self.c = c
        self.m = m

    def nextint(self):
        self.x_n = (self.a * self.x_n + self.c) % self.m
        return self.x_n

    def next(self):
        return self.nextint() / self.m

    def generar_numeros(self, n):
        return [self.next() for _ in range(n)]