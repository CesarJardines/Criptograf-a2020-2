import sys
import math
import sympy # Tal vez se tenga que descargar: pip install sympy
from random import randint

def inv_mod(a, b):
    '''
    Inverso modular: inverso, aux, gcd
    '''
    if b == 0:
        return 1, 0, a
    q, r = divmod(a, b)
    x, y, g = inv_mod(b, r)
    return y, x - q * y, g



def suma_eliptica(p, q, a, b, m):
    '''
    Suma de la curva módulo m
    '''
    if p[2] == 0:
        return q # Verificamos los puntos, para regresar uno u otro.
    if q[2] == 0:
        return p
    if p[0] == q[0]:
        if (p[1] + q[1]) % m == 0:
            return 0, 1, 0
        num = (3 * p[0] * p[0] + a) % m
        denom = (2 * p[1]) % m
    else:
        num = (q[1] - p[1]) % m
        denom = (q[0] - p[0]) % m
    inv, _, g = inv_mod(denom, m)
    if g > 1: # No hay inverso
        return 0, 0, denom
    z = (num * inv * num * inv - p[0] - q[0]) % m
    return z, (num * inv * (p[0] - z) - p[1]) % m, 1

def mult_eliptica(k, p, a, b, m):
    '''
    Multiplicación de la curva, módulo m
    '''
    r = (0, 1, 0)
    while k > 0:
        if p[2] > 1:
            return p
        if k % 2 == 1:
            r = suma_eliptica(p, r, a, b, m)
        k = k // 2
        p = suma_eliptica(p, p, a, b, m)
    return r

def lenstra(n):
    '''
    Lenstra
    '''
    g = n
    while g == n:
        q = randint(0, n - 1), randint(0, n - 1), 1
        a = randint(0, n - 1)
        b = (q[1] * q[1] - q[0] * q[0] * q[0] - a * q[0]) % n
        g = math.gcd(4 * a * a * a + 27 * b * b, n)
    if g > 1:
        return (g, n//g) # factores
    for p in list(sympy.primerange(0,n)):
        pp = p
        while pp < n:
            q = mult_eliptica(p, q, a, b, n)
            if q[2] > 1:
                g = math.gcd(q[2], n)
                return (g, n//g) # factores
            pp = p * pp
    return None

print(lenstra(int(sys.argv[1])))

