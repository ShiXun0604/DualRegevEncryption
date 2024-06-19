def AES_key_gen():
    import random

    data = ''.join(str(random.randint(0, 1)) for _ in range(128))
    return hex(int(data, 2))



def key_generation_demo():
    from DualRegev.Cipher import Crypto
    from DualRegev.Config import config

    # 設定安全參數
    config.set_parameter(n=90, m=100, q=241)

    # 生成公鑰、私鑰
    key_obj = Crypto.LBDRKey().generate_key()
    private_key = key_obj.extract_private_key()
    public_key = key_obj.extract_key()

    # 將公鑰、私鑰寫入檔案
    with open('sk.pem', 'wb') as f:
        f.write(private_key)
    with open('pk.pem', 'wb') as f:
        f.write(public_key)



def encryption_demo():
    from DualRegev.Cipher import Crypto
    from DualRegev.IO import Converter

    # 創建加密工具物件
    crypto_obj = Crypto.LBDRCrypt()

    # 載入公鑰
    with open('pk.pem', 'rb') as f:
        pk = f.read()
    crypto_obj.import_key(pk)

    # 加密訊息
    data = '0x7c091f4c34ef21bac81f4d406f4e9cd1'
    byte_data = Converter.hex_to_bytes(data)

    enc_data = crypto_obj.encrypt(byte_data)

    # 紀錄加密訊息
    with open('cipher_text.bin', 'wb') as f:
        f.write(enc_data)



def decryption_demo():
    from DualRegev.Cipher import Crypto
    from DualRegev.IO import Converter

    # 創建加密工具物件
    crypto_obj = Crypto.LBDRCrypt()

    # 載入私鑰
    with open('sk.pem', 'rb') as f:
        sk = f.read()
    crypto_obj.import_key(sk)

    # 讀取加密訊息
    with open('cipher_text.bin', 'rb') as f:
        enc_data = f.read()
    
    # 解密訊息
    byte_data = crypto_obj.decrypt(enc_data)
    data = Converter.bytes_to_hex(byte_data)

    print(data)



# data = AES_key_gen()