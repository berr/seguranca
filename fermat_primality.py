from __future__ import print_function
import random

def is_prime(number, iterations):
  calculated = 0
  while calculated < iterations:
    random_number =  random.randint(0, 2**32)        
    result = pow(random_number, number, number) # random_number^number mod number
    if result != (random_number % number):
      return False
    calculated += 1
  return 1.0/2**iterations

import sys


print('Felipe dos Santos Silveira - 09132014')
print('Usos:')
print('  Nao passe nenhum parametro para testar a primalidade de um numero aleatorio de 256 bits com 1000 iteracoes')
print('  Passe como parametro um numero para testar a primalidade dele com 1000 iteracoes')
print('  Passe como parametro um numero e o numero de iteracoes')
print('')
print('')


def possible_prime():
  number = random.randint(2, 2**254)
  plus_or_minus_one = 1 if random.randint(0,1) == 0 else -1 # every prime has the form 6k +- 1
  return number * 6 + plus_or_minus_one

if len(sys.argv) == 1:
  find_a_prime = True
  number = possible_prime()
  iterations = 1000
elif len(sys.argv) == 2:
  find_a_prime = False
  number = int(sys.argv[1])
  iterations = 1000
elif len(sys.argv )== 3:
  find_a_prime = False
  number = int(sys.argv[1])
  iterations = int(sys.argv[2])  
else:
  print('Numero de parametros errados')
  
  
print('Testando a primalidade de %d com %d iteracoes' % (number, iterations))

def is_a_prime_number(number, iterations):
  prime = is_prime(number, iterations)
  if not prime:
    print('O numero %d nao e primo' % number)
    return False
  else:
    print('O numero e %d primo com %g de probabilidade de erro' % (number,prime))
    return True

while True:
  _prime = is_a_prime_number(number, iterations)
  if _prime:
    sys.exit(0)
  else:
    if find_a_prime:
      number = possible_prime()
    else:
      sys.exit(0)

