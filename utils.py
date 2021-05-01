from random import randrange
from sympy import isprime
from matplotlib import pyplot as plt

__all__ = ['inverse', 'is_prime', 'modular_sqrt']


# Расширенный алгоритм Евклида
def inverse(a, n):
    start_n = n
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n:
        q = a // n
        a, n = n, a % n
        x0, x1 = x1, x0 - x1*q
        y0, y1 = y1, y0 - y1*q
    return x0 % start_n


# Алгоритм Миллера-Рабина проверки числа на простоту
def is_prime(n, k=10):
	if n == 2:
		return True
	if not n & 1:
		return False

	def check(a, s, d, n):
		x = pow(a, d, n)
		if x == 1:
			return True
		for i in range(s - 1):
			if x == n - 1:
				return True
			x = pow(x, 2, n)
		return x == n - 1
	s = 0
	d = n - 1
	while d % 2 == 0:
		d >>= 1
		s += 1
	for i in range(k):
		a = randrange(2, n - 1)
		if not check(a, s, d, n):
			return False
	return True


# Найти корень по модулю
def modular_sqrt(a, p):

    def legendre_symbol(a, p):
        ls = pow(a, (p - 1) // 2, p)
        return -1 if ls == p - 1 else ls

    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m