class CryptParameter():
    def __init__(self, n: int, m: int , q: int, rng: tuple=None) -> None:
        self.name = 'Pattern {}-{}-{}'.format(n, m, q)
        self.__n = n
        self.__m = m
        self.__q = q
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