from __future__ import annotations
from DualRegev.Math.Matrix import IntMatrix



class SecurityPattern():
    def __init__(self, n: int, m: int , q: int, rng: tuple=None) -> None:
        self.name = 'Pattern {}-{}-{}'.format(n, m, q)
        self.__n = n
        self.__m = m
        self.__q = q
        self.__range = rng
        
    
    def ext_size(self) -> tuple[int, int]:
        return (self.__n, self.__m)

    
    def ext_module(self) -> int:
        return self.__q
    

    def ext_range(self) -> tuple:
        return self.__range


SECURTY_PTRN = SecurityPattern(10, 10, 37, (0, 100))

class LBDRKey():
    def __init__(self, ptrn: SecurityPattern = SECURTY_PTRN) -> None:
        self.public_key = (None, None)
        self.__private_key = None
        self.scurty_ptrn = ptrn
    

    def generate_key(self) -> LBDRKey:
        size = self.scurty_ptrn.ext_size()
        rng = self.scurty_ptrn.ext_range()
        A = IntMatrix.rand_normal_distribute_matrix(size, rng)
        print(A)


class LBDRCrypt():
    def __init__(self, ptrn: SecurityPattern = SECURTY_PTRN) -> None:
        pass
        
        
    





    