from socket import *
import sys
import getpass


def main():
    # 从命令行输入Ip 和 端口号，用于多种测试
    if len(sys.argv) < 3:
        print("argv is error!")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    s = socket()
    s.connect((HOST, PORT))

    # 循环请求
    while True:
        print('''
            ========Welcome=========
            --1:注册  2:登录  3.退出
            ========================
            ''')
        try:
            cmd = int(input("输入选项>>"))
        except Exception:
            print('命令错误')
            continue
        if cmd not in [1, 2, 3]:
            print("请输入正确选项！")
            # 不清理缓存，连续输入可能会出现错误
            sys.stdin.flush()  # 清除标准输入的缓存
            continue
        elif cmd == 1:
            # 通过返回值结果来处理不同情况
            if do_register(s) == 0:
                print("注册成功")
            else:
                print("注册失败")
        elif cmd == 2:
            name = do_login(s)
            # 成功了则返回值不等于1
            if name != 1:
                print("登录成功")
                login(s, name)
            # 失败的话，返回1
            else:
                print("登录失败")
        elif cmd == 3:
            # 退出前，告知服务器
            s.send(b'E')
            sys.exit('欢迎使用')


def do_register(s):
    while True:
        name = input('User name:')
        passwd = getpass.getpass()
        passwd1 = getpass.getpass('Confirm passwd:')
        if (' ' in name) or (' ' in passwd):
            print('名字或密码不允许有空格')
            continue
        if passwd != passwd1:
            print("密码不一致")
            continue
        # 拼接字符串
        # msg = 'R ' + name + ' ' + passwd
        msg = 'R {} {}'.format(name, passwd)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            return 0
        elif data == 'EXISTS':
            print('用户名已存在')
            return 1
        else:
            return 1


def do_login(s):
    name = input("请输入用户名:")
    passwd = getpass.getpass('密码:')
    msg = 'L {} {}'.format(name, passwd)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        return name
    else:
        print('用户名或密码错误')
        return 1


def login(s, name):
    while True:
        print('''
            ===========查询界面===========
            --1.查词   2.历史记录  3.退出　--
            =============================
            ''')
        try:
            cmd = int(input("输入选项>>"))
        except Exception:
            print('命令错误')
            continue
        if cmd not in [1, 2, 3]:
            print("请输入正确选项！")
            # 不清理缓存，连续输入可能会出现错误
            sys.stdin.flush()  # 清除标准输入的缓存
            continue
        elif cmd == 1:
            do_query(s, name)
        elif cmd == 2:
            do_history(s, name)
        elif cmd == 3:
            return  # 退出，则直接返回到一级界面


def do_query(s, name):
    while True:
        try:
            word = input('单词(输入##退出):')
        except Exception:
            continue
        if word == '##':
            break
        msg = 'Q {} {}'.format(name, word)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            data = s.recv(2048).decode()
            print(data)
        else:
            print("没有找到该单词")


def do_history(s, name):
    msg = 'H {}'.format(name)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            # 发送'##',表示发送完了
            if data == '##':
                break
            print(data)
    else:
        print("没有历史记录")


if __name__ == "__main__":
    main()
