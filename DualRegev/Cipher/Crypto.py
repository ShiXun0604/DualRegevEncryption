# Extrnl
from __future__ import annotations
import base64
# Intrnl_Lvl-1
from DualRegev.__init__ import SECURTY_PARA
from DualRegev.CryptParameter import CryptParameter
# Intrnl_Lvl-2
from DualRegev.Math.Matrix import IntMatrix



__all__ = ['LBDRKey', 'LBDRCrypt']


class LBDRKey():
    """
    測試測試
    """
    def __init__(self, para: CryptParameter = SECURTY_PARA) -> None:
        self.para = para
        self.public_key = (None, None)
        self.__private_key = None
    
    
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
    
    
    # 輸出公鑰
    def extract_key(self) -> bytes:
        A = self.public_key[0]
        u = self.public_key[1]
        para = self.para

        ext_A = str(A).replace(' ', ',').replace('\n', '\\')
        ext_u = str(u).replace(' ', ',').replace('\n', '\\')
        ext_para = str(para).replace(' ', ',')
        
        ext_data = (ext_A + '$' + ext_u + '$' + ext_para).encode()
        ext_data = base64.b64encode(ext_data)
        ext_data = self.__insert_line_breaks(ext_data)
        
        ext_str = b'-----BEGIN DUAL REGEV PUBLIC KEY-----' + b'\n'
        ext_str += ext_data + b'\n-----END DUAL REGEV PUBLIC KEY-----'
        
        return ext_str


    # 輸出私鑰
    def extract_private_key(self) -> bytes:
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

        return ext_str.encode()
    

    # 載入金鑰
    def import_key(self, data) -> None:
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
        self.para = CryptParameter(n, m, q, (rng_1, rng_2))
        
        # 私鑰
        if len(data_list) == 4:
            str_x = data_list[3]
            x = IntMatrix([[i] for i in str_x])
            self.__private_key = x
    

    def __insert_line_breaks(self, s):
        WIDTH = 64
        return b'\n'.join([s[i:i+WIDTH] for i in range(0, len(s), WIDTH)])



class LBDRCrypt(LBDRKey):
    def __init__(self, para) -> None:
        super().__init__(para)
        self.__mu = 0
        self.sigma = 10
    

    def encrypt(self, data) -> bytes:
        pass





    