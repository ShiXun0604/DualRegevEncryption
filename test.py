
from DualRegev.Cipher import Crypto
from DualRegev.IO import Converter
from DualRegev import Config
from DualRegev.Math.Matrix import IntMatrix
import random



def AES_key_gen():
    data = ''.join(str(random.randint(0, 1)) for _ in range(128))
    return hex(int(data, 2))


def key_gen():
    key_obj = Crypto.LBDRKey().generate_key()
    sk = key_obj.extract_private_key()
    pk = key_obj.extract_key()

    with open('sk.pem', 'wb') as f:
        f.write(sk)

    with open('pk.pem', 'wb') as f:
        f.write(pk)


def matrix_test():
    m1 = IntMatrix().rand_normal_distribute_matrix((2,3), (1,100))
    m2 = IntMatrix().rand_normal_distribute_matrix((2,3), (1,100))
    m1.print_str()
    m2.print_str()
    print(m1+m2)


def test():
    data = "0b11001011"
    data = Converter.binary_to_bytes(data)
    print(data)

    with open('sk.pem', 'rb') as f:
        sk = f.read()
    with open('pk.pem', 'rb') as f:
        pk = f.read()

    cipher = Crypto.LBDRCrypt()
    cipher.import_key(sk)
    enc_data = cipher.encrypt(data)
    dec_data = cipher.decrypt(enc_data)
    print(dec_data)
    

def test2():
    data = "0b11001101"
    a = data.encode()
    print(a)


test()