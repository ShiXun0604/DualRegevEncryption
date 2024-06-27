import multiprocessing



__all__ = ['MultiprocEnv', 'CryptParameter', 'config']



class MultiprocEnv():
    def __init__(self) -> None:
        self.is_multiproc = False
        self.ENV_CPU_COUNT = multiprocessing.cpu_count()
        self.__used_cpu_count = 2


    def get_used_cpu(self) -> int:
        return self.__used_cpu_count
    

    def set_used_cpu(self, num: int) -> None:
        self.__used_cpu_count = num



class CryptParameter():
    def __init__(self, n: int, m: int , q: int, rng: tuple=None) -> None:
        self.name = 'Pattern {}-{}-{}'.format(n, m, q)
        self.__n = int(n)
        self.__m = int(m)
        self.__q = int(q)
        self.__rng = rng if rng else (1, q)
    
    
    def ext_size(self) -> tuple[int, int]:
        return (self.__n, self.__m)

    
    def ext_module(self) -> int:
        return self.__q
    

    def ext_range(self) -> tuple:
        return self.__rng
    

    def __str__(self) -> str:
        data = [self.__n, self.__m, self.__q, self.__rng[0], self.__rng[1]]
        return ' '.join(str(i) for i in data)



# 設定的class物件
class config:
    multiprocEnv = MultiprocEnv()
    cryptParameter = None

    def set_parameter(n: int, m: int , q: int, rng: tuple=None) -> None:
        config.cryptParameter = CryptParameter(n, m, q, rng)



# default
config.set_parameter(n=256, m=512, q=16349)