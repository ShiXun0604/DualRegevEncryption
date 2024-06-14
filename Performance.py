import multiprocessing



class MultiprocEnvSetting:
    def __init__(self) -> None:
        self.__is_multiprocessing = False
        self.proc_mode = 'qter_1' if self.__is_multiprocessing else None
        self.ENV_CPU_COUNT = multiprocessing.cpu_count()


    def set_is_multiprocessing(self, config: bool) -> None:
        # 偵錯
        if isinstance(config, bool):
            error_message = "unsupported type(s) for '{}'.".format(str(type(config)).split("'")[1])
            raise TypeError(error_message)
        



# for test
if __name__ == '__main__':
    print(MultiprocEnvSetting().ENV_CPU_COUNT)
