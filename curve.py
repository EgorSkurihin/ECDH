from utils import *
import random

class EllCurve:
    def __init__(self, a, b, p):
        if not is_prime(p):
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
        left = pow(y, 2) % self.module
        right = (pow(x, 3)+ x*self.a + self.b) % self.module
        return right == left


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
    

    def find_minimal_point(self):
        x = 0
        while True:
            right = (x ** 3 + self.a * x + self.b) % self.module
            y = modular_sqrt(right, self.module)
            point = (x, y)
            if self.is_point_on_curve(point):
                return point
            x+=1


if __name__ == "__main__":
    module = 115792089210356248762697446949407573530086143415290314195533631308867097853951
    a = 115792089210356248762697446949407573530086143415290314195533631308867097853948
    b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
    c = EllCurve(a, b, module)
    point = c.find_rand_point()
    print(point)
    print(c.is_point_on_curve(point))