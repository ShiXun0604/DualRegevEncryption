# External
from __future__ import annotations
import random

# Internal
from DualRegev.Config import *



__all__ = ['IntMatrix']


class IntMatrix():
    """
    此為實做整數矩陣的class，資料結構用慢速python內建雙層list，搭配multiprocessing讓執行快一些@@
    """
    def __init__(self, data: list[list[int]] = []) -> None:
        self.IntMatrix = data
        #self.rows = len(data)
        #self.cols = len(data[0]) if self.rows > 0 else 0
        #self.maxlen = maxlen if maxlen else self.__find_max_len()

    @property
    def rows(self) -> int:
        return len(self.IntMatrix)
    
    @property
    def cols(self) -> int:
        return len(self.IntMatrix[0]) if self.rows > 0 else 0
    
    @property
    def maxlen(self) -> int:
        return self.__find_max_len()


    def __find_max_len(self) -> int:
        max_length = 0
        for row in self.IntMatrix:
            for element in row:
                max_length = max(max_length, len(str(element)))
        return int(max_length)
    

    # 定義加法運算
    def __add__(self, other: IntMatrix) -> IntMatrix:
        if not isinstance(other, IntMatrix):
            error_message = 'Invalid type input.'
            raise TypeError(error_message)
        
        if self.rows != other.rows or self.cols != other.cols:
            error_message = 'The dimensions of the two matrices are different and cannot be added.'
            raise ValueError(error_message)
        
        result = [[self.IntMatrix[j][i] + other.IntMatrix[j][i] for i in range(self.cols)] for j in range(self.rows)]
        return IntMatrix(result)


    # 定義乘法運算
    def __rmul__(self, other: int) -> IntMatrix:
        return self.__mul__(other)
    

    def __mul__(self, other: IntMatrix | int) -> IntMatrix:
        # 偵錯
        if not isinstance(other, IntMatrix) and not isinstance(other, int):
            error_message = "unsupported operand type(s) for *: '{}' and 'IntMatrix'.".format(str(type(other)).split("'")[1])
            raise TypeError(error_message)
        elif isinstance(other, IntMatrix) and self.cols != other.rows:
            error_message = "IntMatrix A row len not equal to IntMatrix B column len."
            raise ValueError(error_message)
        
        # init result
        result = []
        
        # 乘法運算
        if isinstance(other, IntMatrix):  # 矩陣*矩陣
            result = [[0 for _ in range(other.cols)] for __ in range(self.rows)]
            for i in range(self.rows):
                for j in range(other.cols):
                    for k in range(self.cols):
                        result[i][j] += self.IntMatrix[i][k] * other.IntMatrix[k][j]  # 需要進行multiprocessing
        else:  # 整數*矩陣 or 矩陣*整數
            result = [[0 for _ in range(self.cols)] for __ in range(self.rows)]
            for i in range(self.rows):
                for j in range(self.cols):
                    result[i][j] = self.IntMatrix[i][j] * other  # 需要進行multiprocessing

        # 回傳結果
        return IntMatrix(result)
    
    
    # 定義模除運算
    def __mod__(self, other: int) -> IntMatrix:
        # 偵錯
        if not isinstance(other, int):
            error_message = "unsupported operand type(s) for %: '{}' and 'IntMatrix'.".format(str(type(other)).split("'")[1])
            raise TypeError(error_message)

        # 模除運算
        result = [[0 for _ in range(self.cols)] for __ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                result[i][j] = self.IntMatrix[i][j] % other  # 需要進行multiprocessing

        # 回傳結果
        return IntMatrix(result)
    

    # 定義 ==
    def __eq__(self,  other: object) -> bool:
        return self.IntMatrix == other.IntMatrix


    # 定義轉為文字相關
    def __str__(self) -> str:
        return '\n'.join(' '.join(str(element) for element in row) for row in self.IntMatrix)
    

    # 定義轉置矩陣
    @property
    def trans(self) -> IntMatrix:
        result = [[self.IntMatrix[i][j] for i in range(self.rows)] for j in range(self.cols)]
        return IntMatrix(result)
    

    # 回傳維度大小
    def dsize(self) -> str:
        return '{}x{}'.format(self.rows, self.cols)
    

    @staticmethod
    def str_to_matrix(str_data) -> IntMatrix:
        """
        回傳
        """
        data = str_data.split('\n')
        
        for i in range(len(data)):
            data[i] = data[i].split(' ') 
            for j in range(len(data[i])):
               data[i][j] = int(data[i][j])
        
        return IntMatrix(data)

    # 工整的印出當前的儲存的結果
    def print_str(self) -> None:
        s = '\n'.join('  '.join(f'{element:{self.maxlen}}' for element in row) for row in self.IntMatrix)
        print(s)
        """
        s = ''
        for row in self.IntMatrix:
            for element in row:
                s += '{:{width}}  '.format(element, width=self.maxlen)
            s += '\n'
        print(s.strip('\n'))
        """
    

    # 回傳隨機分布矩陣
    @staticmethod
    def rand_normal_distribute_matrix(size: tuple[int, int], rng: tuple[int, int]) -> IntMatrix:
        result = [[random.randint(*rng) for _ in range(size[1])] for __ in range(size[0])]
        return IntMatrix(result)


    # 回傳高斯分布矩陣
    @staticmethod
    def gauss_distribute_matrix(size: tuple[int, int], mu: int = 0, sigma: float | int = 10) -> IntMatrix:
        result = [[round(random.gauss(mu, sigma)) for _ in range(size[1])] for __ in range(size[0])]
        return IntMatrix(result)