def test():
    from DualRegev.Cipher import Crypto



    key_obj = Crypto.LBDRKey().generate_key()
    print(key_obj.extract_key())



test()

