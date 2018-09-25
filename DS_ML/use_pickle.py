import pickle


data1 = {'a': [1, 2.0, 3, 4+6j],
         'b': ('string', u'Unicode string'),
         'c': None}

print(type(data1))

# 注意要以 ‘wb’ 的方式打开文件
with open('s.pickle', 'wb') as f:
    pickle.dump(data1, f)

print('----------------------------')

# 注意要以 ‘rb’ 的方式打开文件
with open('s.pickle', 'rb') as f1:
    pickle.load(f1)
    print(s1)
