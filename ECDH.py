from curve import EllCurve
from utils import is_prime
from random import randrange


class ECDH:
    PUBLIC_POINT = (None, None)


    def __init__(self, a, b, module):
        self.__module = module
        self.__curve = EllCurve(a, b, module)
        # Public point should be the same, so I use first point of EllCurve
        self.__PUBLIC_POINT = self.__curve.find_minimal_point()
        self.__secret_num = None
        self.__shared_key = (None, None)


    def gen_public_key(self, secret_num=None):
        #A = kA * Pub_point
        #B = kB * Pub_point  
        if not secret_num:
            secret_num = randrange(1, self.__module)
        self.__secret_num = secret_num
        self.__public_key = self.__curve.multiply(self.__secret_num, self.__PUBLIC_POINT)
        return self.__public_key


    def gen_shared_key(self, partners_public_key):
        # shared_key = k2*A = k2*B
        # k2*A = kA*kB*Pub_point 
        # k1*B = KA*kB*Pub_point 
        if not self.__curve.is_point_on_curve(partners_public_key):
            raise ValueError(f"Partners point {partners_public_key} is not on curve")
        self.__shared_key = self.__curve.multiply(self.__secret_num, partners_public_key)
        return self.__shared_key

    

if __name__ == '__main__':
    # Curve parameters
    module = 115792089210356248762697446949407573530086143415290314195533631308867097853951
    a = 115792089210356248762697446949407573530086143415290314195533631308867097853948
    b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
    
    A_ECDH = ECDH(a, b, module)
    B_ECDH = ECDH(a, b, module)

    A_pub_key = A_ECDH.gen_public_key(secret_num=1234)
    B_pub_key = B_ECDH.gen_public_key()

    shared_key1 = A_ECDH.gen_shared_key(B_pub_key)
    shared_key2 = B_ECDH.gen_shared_key(A_pub_key)

    print(shared_key1)
    print(shared_key2)