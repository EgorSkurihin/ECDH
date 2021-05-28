from curve import EllCurve
from random import randrange


class ECDH:

    def __init__(self):
        self.__module = int("0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F", 16)
        a = int("0000000000000000000000000000000000000000000000000000000000000000", 16)
        b = int("0000000000000000000000000000000000000000000000000000000000000007", 16)
        xG = int("0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798", 16)
        yG = int("0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8", 16)

        self.__curve = EllCurve(a, b, self.__module)
        self.__PUBLIC_POINT = (xG, yG)


    def gen_public_key(self):
        #A = kA * Pub_point
        #B = kB * Pub_point
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
        shared_key = self.__curve.multiply(self.__secret_num, partners_public_key)
        return shared_key
        

    

if __name__ == '__main__':
    
    A_ECDH = ECDH()
    B_ECDH = ECDH()
    A_pub_key = A_ECDH.gen_public_key()
    B_pub_key = B_ECDH.gen_public_key()
    print(f"Alice pub key: {A_pub_key}")
    print(f"Bob pub key: {B_pub_key}")
    shared_key1 = A_ECDH.gen_shared_key(B_pub_key)
    shared_key2 = B_ECDH.gen_shared_key(A_pub_key)
    print(f"\nAlice shared key: {shared_key1}")
    print(f"Bob shared key: {shared_key2}")


