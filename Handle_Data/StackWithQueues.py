'''
    使用队列来实现栈
'''


class StackWithQueues:
    def __init__(self):
        self.q1 = []
        self.q2 = []

    def push(self, val):
        # 都为空则往队列1 push数据,以后选择不为空的进行push数据
        if len(self.q1) == 0 and len(self.q2) == 0:  # 2个都为空
            self.q1.append(val)
        elif len(self.q1) == 0 and len(self.q2) > 0:
            self.q2.append(val)
        elif len(self.q2) == 0 and len(self.q1) > 0:
            self.q1.append(val)
        else:
            assert(1 == 0)

    def pop(self):
        # 将不为空的队列数据挨个push到空队列，
        # 直到剩下一个元素为止，打印这个元素并删除
        if len(self.q1) > 0 and len(self.q2) == 0:
            while len(self.q1) > 1:
                self.q2.append(self.q1.pop(0))
            return self.q1.pop(0)
        elif len(self.q2) > 0 and len(self.q1) == 0:
            while len(self.q2) > 1:
                self.q1.append(self.q2.pop(0))
            return self.q2.pop(0)
        else:
            assert(1 == 0)

    def __repr__(self):
        # 输出信息
        if self.q1:
            return self.q1.__str__()
        else:
            return self.q2.__str__()
            

if __name__ == '__main__':
    s = StackWithQueues()
    s.push(1)
    s.push(2)
    s.push(3)
    print(s.pop())
    s.push(4)
    print(s)
    print(s.pop())
    print(s.pop())
    print(s.pop())            




