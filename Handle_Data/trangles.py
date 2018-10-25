
'''
Topic:杨辉三角
'''

def trangile1():
    a = [1]
    while True:
        yield a
        a = [sum(i) for i in zip([0] + a, a + [0])]

def trangile2():
    a = [1]
    while True:
        yield a
        a = [a[i] + a[i+1] for i in range(len(a)-1)]
        a = [1] + a
        a.append(1)


if __name__ == '__main__':
    for i in trangile2():
        print(i)
        if len(i) == 10:
            break


