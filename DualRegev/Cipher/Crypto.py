# Extrnl
from __future__ import annotations
import base64, hashlib, multiprocessing
# Intrnl_Lvl
from DualRegev.Config import *
# Intrnl_Lv2
from DualRegev.Math.Matrix import IntMatrix
from DualRegev.IO import Converter, String
from DualRegev.IO.Error import *



__all__ = ['LBDRKey', 'LBDRCrypt']

"""
金鑰格式:
    1. 公鑰格式為 pk = (A, u, para)
    2. 私鑰格式為 sk = (A, u, para, x)
    3. 矩陣使用空格隔開、\n換行
    4. 各資料之間使用'$'隔開

加密訊息格式:
    1. 加密訊息資料結構為 list[tuple(IntMatrix, int), ...]
    2. 矩陣使用空格隔開、\n換行
    3. tuple資料間使用'#'隔開
    4. list資料間使用'$'隔開
"""



# for multiprocessing
def encrypt_task(task_bin_data: list[str], A: IntMatrix, u: IntMatrix, q: int, range: tuple, MU: int, sigma: int) -> str:
    task_enc_data = ''
    for bit in task_bin_data:
        # 生成s、x
        s_size = (u.rows, 1)
        x_size = (A.cols, 1)
        s = IntMatrix.rand_normal_distribute_matrix(size=s_size, rng=range)
        x = IntMatrix.gauss_distribute_matrix(size=x_size, mu=MU, sigma=sigma)
        
        # 計算密文
        c_0 = (A.trans*s + x) % q
        c_1 = ( ((u.trans*s).IntMatrix)[0][0] + (int(q/2) * int(bit)) ) % q
        
        task_enc_data += str(c_0) + '#' + str(c_1) + '$'
    return task_enc_data



class LBDRKey():
    """
    測試測試
    """
    def __init__(self, para: CryptParameter = config.cryptParameter) -> None:
        self.public_key = (None, None)
        self.__private_key = None
    
    @property
    def para(self) -> CryptParameter:
        return config.cryptParameter
    
    
    # 回傳私鑰
    def get_private_key(self) -> IntMatrix:
        return self.__private_key
    
    # 生成公、私鑰對
    @staticmethod
    def generate_key() -> LBDRKey:
        key_obj = LBDRKey()

        size = key_obj.para.ext_size()
        rng = key_obj.para.ext_range()
        q = key_obj.para.ext_module()

        A = IntMatrix.rand_normal_distribute_matrix(size, rng)
        x = IntMatrix.rand_normal_distribute_matrix(size=(size[1], 1), rng=(0,1))
        u = (A * x) % q

        key_obj.public_key = (A, u)
        key_obj.__private_key = x
        
        return key_obj
    
    
    # 回傳pem格式的公鑰
    def extract_key(self) -> bytes:
        # 除錯
        if self.public_key == (None, None):
            error_message = 'No public key import/generate in class.'
            raise KeyExtractionError(error_message)
        
        A = self.public_key[0]
        u = self.public_key[1]
        para = self.para

        ext_A = str(A).replace('\n', '\\')
        ext_u = str(u).replace('\n', '\\')
        ext_para = str(para)
        
        ext_data = (ext_A + '$' + ext_u + '$' + ext_para).encode()
        ext_data = base64.b64encode(ext_data)
        ext_data = self.__insert_line_breaks(ext_data)
        
        ext_str = b'-----BEGIN DUAL REGEV PUBLIC KEY-----' + b'\n'
        ext_str += ext_data + b'\n-----END DUAL REGEV PUBLIC KEY-----'
        
        return ext_str


    # 回傳pem格式的私鑰
    def extract_private_key(self) -> bytes:
        # 除錯
        if self.public_key == (None, None):
            error_message = 'No private key import/generate in class.'
            raise KeyExtractionError(error_message)
        
        A = self.public_key[0]
        u = self.public_key[1]
        x = self.__private_key
        para = self.para

        ext_A = str(A).replace('\n', '\\')
        ext_u = str(u).replace('\n', '\\')
        ext_x = str(x).replace(' ', '').replace('\n', '')
        ext_para = str(para)

        ext_data = (ext_A + '$' + ext_u + '$' + ext_para + '$' + ext_x).encode()
        ext_data = base64.b64encode(ext_data)
        ext_data = self.__insert_line_breaks(ext_data)

        ext_str = b'-----BEGIN DUAL REGEV PRIVATE KEY-----\n'
        ext_str += ext_data + b'\n-----END DUAL REGEV PRIVATE KEY-----'

        return ext_str


    # 載入金鑰
    @error_catcher(KeyImportError, 'Error occure while import key.')
    def import_key(self, data: bytes) -> None:
        base64_data_list = data.decode().split('\n')

        # 取出中間字段，去掉---BEGIN---和---END---
        ext_data = ''
        for i in range(1, len(base64_data_list)-1):
            ext_data += base64_data_list[i]
        ext_data = base64.b64decode(ext_data.encode()).decode()
        
        # 分析、拆分中間字段
        data_list = ext_data.split('$')
        str_A = data_list[0].replace('\\', '\n')
        str_u = data_list[1].replace('\\', '\n')
        str_para = data_list[2]

        # 公鑰
        A = IntMatrix().str_to_matrix(str_A)
        u = IntMatrix().str_to_matrix(str_u)
        self.public_key = (A, u)

        # 參數
        n, m, q, rng_1, rng_2 = str_para.split(' ')
        config.set_parameter(int(n), int(m), int(q), (int(rng_1), int(rng_2)))
        
        # 私鑰
        if len(data_list) == 4:
            str_x = data_list[3]
            x = IntMatrix([[int(i)] for i in str_x])
            self.__private_key = x
    

    def __insert_line_breaks(self, s):
        WIDTH = 64
        return b'\n'.join([s[i:i+WIDTH] for i in range(0, len(s), WIDTH)])



class LBDRCrypt(LBDRKey):
    def __init__(self, para: CryptParameter = config.cryptParameter) -> None:
        super().__init__(para)
        self.__MU = 0
        self.sigma = 20
    

    def encrypt(self, data: bytes) -> bytes:
        if isinstance(data, bytes):
            bin_data = Converter.bytes_to_binary(data)[2:]  # 去掉0x
            #print(len(bin_data))  # 檢查加密資料bit數
        else:
            error_message = 'Invalid data input.'
            raise ValueError(error_message)
        
        # 載入參數
        A = self.public_key[0]
        u = self.public_key[1]
        q = self.para.ext_module()

        if not A or not u or not q:
            error_message = 'Encryption requires public key. No public key imported.'
            raise NoPublicKeyError(error_message)

        # 加密開始
        task_data_list = String.split_string(bin_data, 3)
        tasks = []
        for ele in task_data_list:
            tasks.append((ele, A, u, q, self.para.ext_range(), self.__MU, self.sigma))

        # multiprocessing
        PROC_CNT = config.multiprocEnv.used_cpu_count
        with multiprocessing.Pool(PROC_CNT) as pool:
            return_data = pool.starmap(encrypt_task, tasks)

            pool.close()
            pool.join()

        # 合併結果
        enc_data = ''
        for ele in return_data:
            enc_data += ele
        enc_data = enc_data.strip('$').encode()

        # 將明文的長度以及hash值寫入最前面
        hash_value = '0x' + hashlib.sha256(data).hexdigest()
        hash_value = Converter.hex_to_bytes(hash_value)
        enc_data = hash_value + enc_data

        # base64編碼
        enc_data = base64.b64encode(enc_data)

        return enc_data

    
    def decrypt(self, enc_data: bytes) -> bytes:
        # 載入私鑰、參數
        sk = self.get_private_key()
        q = self.para.ext_module()
        half_q = int(q/2)
        qutr_q = int(q/4)

        # 若沒有私鑰,則不能解密
        if not sk:
            error_message = 'Decryption requires private key. No private key imported.'
            raise NoPrivateKeyError(error_message)
        # 若資料結構錯誤,則不能解密
        if not isinstance(enc_data, bytes):
            error_message = ''
            raise TypeError(error_message)

        # base64解碼
        enc_data = base64.b64decode(enc_data)

        # 分割hash value
        hash_value = enc_data[:32]
        cipher_text = enc_data[32:]

        # 密文前處理
        cipher_text = cipher_text.decode()
        enc_data_list = cipher_text.split('$')

        # 解密區塊
        try:
            data = '0b'
            for ele in enc_data_list:
                c_0, c_1 = ele.split('#')

                c_0 = IntMatrix.str_to_matrix(c_0)
                c_1 = int(c_1)
                
                u_prime = (c_1 - ((sk.trans * c_0).IntMatrix)[0][0]) % q
                #print(u_prime, sep=' ')  # 檢查sigma是否太大

                if abs(u_prime - half_q) < qutr_q:
                    data += '1'
                else:
                    data += '0'
            data = Converter.binary_to_bytes(data)
        except:
            error_message = 'Decryption failed.'
            raise DecryptionError(error_message)

        # 資料檢查
        hash_value = Converter.bytes_to_hex(hash_value)[2:]
        if hash_value != hashlib.sha256(data).hexdigest():
            error_message = 'Decryption failed. Not using the correct private key.'
            raise DecryptionError(error_message)
        
        return data


            
        

