class Matrix:
    def __init__(self, data:list[list[int]]=[]) -> None:
        self.matrix = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0
    
    # 定義乘法運算
    def __mul__(self, other):
        if self.cols != other.rows:
            raise ValueError("矩陣 A 的列數必須等於矩陣 B 的行數")
        
        result = [[0 for _ in range(other.cols)] for _ in range(self.rows)]
        
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result[i][j] += self.matrix[i][k] * other.matrix[k][j]
        
        return Matrix(result)
    
    # for印出當前的儲存的結果
    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])
    

m1 = Matrix([[1,1], [1,1]])
m2 = Matrix([[3,1], [2,5]])
print(m1*m2)