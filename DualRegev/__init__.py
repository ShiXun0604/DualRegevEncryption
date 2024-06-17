from .Performance import MultiprocEnvSetting
from .CryptParameter import CryptParameter



__all__ = [
    "Performance", 
    "CryptParameter",
    "Cipher",
    "Math",
]

version_info = (1, 0, '0')

__version__ = ".".join([str(x) for x in version_info])


# 定義全域使用的參數
# (感覺是個爛方法,不知道有沒有更好的方法,知識不足QAQ)
PROC_SETTING = MultiprocEnvSetting()
SECURTY_PARA = CryptParameter(20, 30, 240)