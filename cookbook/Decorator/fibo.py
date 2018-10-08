import functools
from clockdeco2 import clock


@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)


# 使用缓存实现，速度更快
@functools.lru_cache()
@clock
def fibonacci1(n):
    if n < 2:
        return n
    return fibonacci1(n-2) + fibonacci1(n-1)
    
if __name__=='__main__':
    # print(fibonacci(6))
    print(fibonacci1(30))
