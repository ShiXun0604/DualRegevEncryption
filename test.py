from DualRegev.Math.Matrix import IntMatrix
from time import time
from DualRegev.Config import config
import multiprocessing



def func_timer(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        exec_time = time() - start_time

        print('執行時間：{:.4f}秒'.format(exec_time))

        return result
    return wrapper


M1 = IntMatrix.rand_normal_distribute_matrix((2, 3), (1, 9))
M2 = IntMatrix.rand_normal_distribute_matrix((3, 2), (1, 9))


@func_timer
def main():
    M3 = M1 * M2
    print(M3.dsize())



if __name__ == '__main__':
    main()