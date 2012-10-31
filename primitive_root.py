# Felipe dos Santos Silveira - 09132014
# Trabalho Individual 2. Seguranca em Computacao. 2012-2


import math  


def factor(n):
    factors = set()

    for i in range(2, math.ceil(math.sqrt(n)) + 1):
        added = False
        while (n % i) == 0:
            n = int(n / i)
            added = True
        if added:
            factors.add(i)

    if n > 1:
        factors.add(n)

    return factors


def primitive_roots(n):
    phi_n = n - 1
    factors = factor(phi_n)

    primitive_roots = []

    for m in range(1, n):
        for p in factors:
            r = pow(m, int(phi_n / p), n)
            if r == 1:
                break
        else:
            primitive_roots.append(m)

    return primitive_roots

import sys


if len(sys.argv) != 2:
    print ('Passe como argumento o numero primo n')
    sys.exit(1)

try:
    n = int(sys.argv[1])
except:
    print ('Tipo do argumento invalido. Passe um numero inteiro primo')
    sys.exit(1)

roots = primitive_roots(n)

if roots:
    print ('A raizes primitivas sao:', ','.join((str(x) for x in roots)))
else:
    print ('Nao existe raiz primitiva')
