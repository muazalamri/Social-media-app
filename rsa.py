import random
from sympy import isprime, mod_inverse

def generate_prime_candidate(length):
    p = random.getrandbits(length)
    while not isprime(p):
        p = random.getrandbits(length)
    return p

def generate_keypair(length):
    p = generate_prime_candidate(length)
    q = generate_prime_candidate(length)
    while q == p:
        q = generate_prime_candidate(length)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    
    d = mod_inverse(e, phi)
    
    return ((e, n), (d, n))

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def encrypt(public_key, plaintext):
    e, n = public_key
    cipher = [(ord(char) ** e) % n for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    d, n = private_key
    plain = [chr((char ** d) % n) for char in ciphertext]
    return ''.join(plain)

def save_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(' '.join(map(str, data)))

def load_from_file(filename):
    with open(filename, 'r') as file:
        data = file.read().split()
    return list(map(int, data))

def encrypt_file(text:str, output_filename:int, public_key=(10271, 14941)):
    encrypted_data = encrypt(public_key, text)
    save_to_file("posts/"+str(output_filename)+'.data', encrypted_data)

def decrypt_file(input_index:int, private_key=(14351, 14941)):
    encrypted_data = load_from_file("posts/"+str(input_index)+'.data')
    decrypted_data = decrypt(private_key, encrypted_data)
    return decrypted_data