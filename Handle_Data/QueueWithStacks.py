'''
    怎么用栈来实现队列
'''

class QueueWithStacks:
    def __init__(self):
        self.s1 = []
        self.s2 = []

    # push直接让节点进入栈1
    def push(self, val):
        self.s1.append(val)

    def pop(self):
        if len(self.s2) <= 0:
            while len(self.s1) > 0:  # 将s1中的元素依次Push到s2中
                t = self.s1.pop()
                self.s2.append(t)

        # 此时需要保证S2中一定有元素，否则逻辑上队列是没有元素输出的
        assert(len(self.s2) > 0)  
        return self.s2.pop()

    # 显示当前封装队列的两个栈的当前信息
    def __repr__(self):
        print('s1:', self.s1)
        print('s2:', self.s2)
        return "QueueWithStacks('%r')" % self.s2 


if __name__ == '__main__':
    q = QueueWithStacks()
    q.push('a')
    q.push('b')
    q.push('c')
    print(q.pop())
    q.push('d')
    print(q)
    print(q.pop())
    print(q.pop())
    print(q.pop())
    print(q)
    # print(q.pop())








