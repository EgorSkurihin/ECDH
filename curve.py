from utils import *
import random
from sympy import isprime

class EllCurve:
    def __init__(self, a, b, p):
        if not isprime(p):
            raise ValueError(f"Module {p} is not prime number")
        self.a = a
        self.b = b
        self.module = p
        self.null_point = (None, None)


    def is_null(self, p):
        return p == self.null_point


    def is_opposite(self, p1, p2):
        return p1[0] == p2[0] and p1[1] == -p2[1] % self.module

    
    def is_point_on_curve(self, p):
        x, y = p
        if self.is_null(p):
            return True
        left = y ** 2
        rigth = x ** 3 + x*self.a + self.b
        return rigth % self.module == left % self.module


    def add(self, p1, p2):
        if not self.is_point_on_curve(p1):
            raise ValueError("Point p1 is not on curve")
        if not self.is_point_on_curve(p2):
            raise ValueError("Point p2 is not on curve")

        if self.is_null(p1):
            return p2
        if self.is_null(p2):
            return p1
        if self.is_opposite(p1, p2):
            return self.null_point

        x1, y1 = p1
        x2, y2 = p2

        l = 0
        if x1 != x2:
            l = (y2 - y1) * inverse(x2 - x1, self.module)
        else:
            l = (3 * x1 ** 2 + self.a) * inverse(2 * y1, self.module)

        x = (l * l - x1 - x2) % self.module
        y = (l * (x1 - x) - y1) % self.module
        return (x, y)


    def double(self, p):
        return self.add(p, p)


    def multiply(self, n, p):
        if self.is_null(p) or n == 0:
            return self.null_point

        res = self.null_point
        while n:
            if n & 1:
                res = self.add(res, p)
            p = self.double(p)
            n >>= 1
        return res
    

    def find_rand_point(self):
        while True:
            x = random.randint(0, self.module)
            right = (x ** 3 + self.a * x + self.b) % self.module
            y = modular_sqrt(right, self.module)
            point = (x, y)
            if self.is_point_on_curve(point):
                return point


if __name__ == "__main__":
    c = EllCurve(-1, 1, 751)
    print(f"Curve parameters: a=-1, b=1, p=751;\n")
    p1 = (0, 1)
    print(f"Point1: {p1}")
    p2 = c.find_rand_point()
    print(f"Random point of curve (Point2) = {p2}")
    print(f"Point1 + Point2 = {p1} + {p2} = {c.add(p1,p2)}")
    print(f"10 * {p1} = {c.multiply(10, p1)}")

