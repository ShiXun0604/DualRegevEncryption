import multiprocessing


MODE_LIST = {
    'qter_0' : 0,
    'qter_1' : 0.25,
    'qter_2' : 0.5,
    'qter_3' : 0.75,
    'qter_4' : 1.0,
}


class MultiprocEnvSetting:
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