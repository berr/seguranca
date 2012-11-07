from __future__ import print_function
import random
import math
import socket
import multiprocessing

# Felipe dos Santos Silveira - 09132014


################################################################################
##                     Helper funtions to diffie hellman                      ##
################################################################################

PRIME_FIND_MAX_ITERATIONS = 1000

def get_prime(n_bits):
    while True:
        iterations = 0
        possible_prime = random.randint(2, 2**n_bits)
        while iterations < PRIME_FIND_MAX_ITERATIONS:            
            random_number =  random.randint(0, 2**31)        
            result = pow(random_number, possible_prime, possible_prime) # random_number^number mod number
            if result != (random_number % possible_prime):
                break
            iterations += 1
        else:
            return possible_prime




def factors(number):
    first_primes = [2,3]

    yield 1

    for prime in first_primes:
        prime_is_factor = False
        while number % prime == 0:
            prime_is_factor = True
            number = number / prime
        if prime_is_factor:
            yield prime

    for i in xrange(6, int(math.sqrt(number)) + 1, 6):
        first = i - 1
        first_is_prime = False 
        while number % (i - 1) == 0:
            first_is_prime = True
            number = number / first
        if first_is_prime:
            yield first

        second_is_prime = False
        second = i + 1
        while number % (i + 1) == 0:
            second_is_prime = True
            number = number / second
        if second_is_prime:
            yield second


    if number != 1:
        yield number



def is_primitive_root(a, n, prime_factors=None):
    phi_n = n - 1 # because n is prime

    if prime_factors is None:
        prime_factors = list(factors(phi_n))
    for p in prime_factors:
        r = pow(a, int(phi_n / p), n)
        if r == 1:
            return False
    else:
        return True

    


def get_primitive_root(n):
    phi_n = n - 1 # because n is prime

    prime_factors = list(factors(phi_n))[1:]
    
    possible_primitive_root = random.randint(1,n-1)
    while not is_primitive_root(possible_primitive_root, n, prime_factors):
        possible_primitive_root = random.randint(1,n-1)

    return possible_primitive_root
            

################################################################################
##                              Server and client                             ##
################################################################################


def build_int_str(number):
    number_str = str(number)
    return '0' * (64 - len(number_str)) + number_str
    

    
def server(host, port):
    # Setting up the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER_HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    try:
        # Generate prime and calculate primitive_root
        prime = get_prime(48)
        primitive_root = get_primitive_root(prime)

        conn.sendall(build_int_str(prime))
        conn.sendall(build_int_str(primitive_root))
        
        # Generate my secret number
        secret = random.randint(1, 2**31)

        my_half_session = pow(primitive_root, secret, prime)
        conn.sendall(build_int_str(my_half_session))

        their_half_session = conn.recv(64)
        their_half_session = int(their_half_session)
        print('Metade de sessao do cliente:', their_half_session)

        full_session = pow(their_half_session, secret, prime)
        print('== Chave de sessao do servidor:', full_session)
        
    finally:
        conn.close()
        s.close()


def client(host, port):
    #Setting up the client
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((CLIENT_HOST,PORT))

    try:
        prime = s.recv(64)
        prime = int(prime)
        print('Primo usado:', prime)

        primitive_root = s.recv(64)
        primitive_root = int(primitive_root)
        print('Raiz primitiva usada:', primitive_root)

        their_half_session = s.recv(64)
        their_half_session = int(their_half_session)
        print('Metade de sessao do servidor:', their_half_session)

        # Generate my secret number
        secret = random.randint(1, 2**31)

        my_half_session = pow(primitive_root, secret, prime)
        s.sendall(build_int_str(my_half_session))

        full_session = pow(their_half_session, secret, prime)
        print('== Chave de sessao do cliente:', full_session)        

    finally:
        s.close()



SERVER_HOST = ''
CLIENT_HOST = '127.0.0.1'
PORT = 3317
    


server_process = multiprocessing.Process(
    target=server, 
    name='diffie-hellman-server', 
    args=(SERVER_HOST, PORT),
)
client_process = multiprocessing.Process(
    target=client, 
    name='diffie-hellman-client',
    args=(CLIENT_HOST, PORT),
)

print('Iniciando servidor')    
server_process.start()
print('Iniciando cliente')
client_process.start()

server_process.join()
client_process.join()



