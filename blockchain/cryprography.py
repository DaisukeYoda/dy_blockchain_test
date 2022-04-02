import math
import binascii

def lcm(p,q):
    return (p * q) // math.gcd(p, q)


class RSA(object):

    @staticmethod
    def generate_keys(p,q):
        N = p * q
        L = lcm(p - 1, q - 1)

        for i in range(2, L):
            if math.gcd(i, L) == 1: 
                E = i
                break

        for i in range(2, L):
            if (E * i) % L == 1: 
                D = i
                break

        return (E, N), (D, N)

    @staticmethod
    def encrypt(text, public_key):
        E, N = public_key
        plain_integers = [ord(char) for char in text]
        encrypted_int = [pow(i, E, N) for i in plain_integers]
        #encrypted_text = ''.join(chr(i) for i in encrypted_integers)

        return encrypted_int

    @staticmethod
    def decrypt(encrypted_int, private_key):
        D, N = private_key
        #encrypted_integers = [ord(char) for char in encrypted_text]
        decrypted_intergers = [pow(i, D, N) for i in encrypted_int]
        decrypted_text = ''.join(chr(i) for i in decrypted_intergers)

        return decrypted_text


if __name__ == '__main__':
    public_key,private_key = RSA.generate_keys(101,73)

    plain_text = 'Hello World'
    ord_text = list(map(ord,plain_text))
    print(ord_text)

    encrypted_ = RSA.encrypt(plain_text,public_key)

    print(encrypted_)

    decrypted_ = RSA.decrypt(encrypted_,private_key)

    print(decrypted_)


