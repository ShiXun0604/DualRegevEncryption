import multiprocessing



__all__ = ['multiprocEnv', 'cryptParameter', 'MultiprocEnv', 'CryptParameter']

MODE_LIST = {
    'qter_0' : 0,
    'qter_1' : 0.25,
    'qter_2' : 0.5,
    'qter_3' : 0.75,
    'qter_4' : 1.0,
}



class MultiprocEnv():
    def __init__(self) -> None:
        self.__proc_mode = 'qter_0'
        self.ENV_CPU_COUNT = multiprocessing.cpu_count()
        self.__used_cpu_count = 1

        self.change_used_cpu_mode(self.__proc_mode)


    def change_used_cpu_mode(self, mode: str) -> None:
        # 偵錯
        if mode not in MODE_LIST.keys():
            keys =  ' '.join(MODE_LIST.keys())
            error_message = 'Invalid mode type (expect {})'.format(keys)
            raise ValueError(error_message)
        
        # 進行設定
        n = int(self.ENV_CPU_COUNT * MODE_LIST[mode])  # 無條件捨去
        self.__used_cpu_count = n if n != 0 else 1
        self.__proc_mode = mode
    
    
    def extract_used_cpu_count(self) -> int:
        return self.__used_cpu_count



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


# 設定檔的class物件
multiprocEnv = MultiprocEnv()
cryptParameter = CryptParameter(20, 30, 241)