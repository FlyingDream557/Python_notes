import pickle


data1 = {'a': [1, 2.0, 3, 4+6j],
         'b': ('string', u'Unicode string'),
         'c': None}

print(type(data1))
f = open('s.pickle', 'wb')
pickle.dump(data1, f)
f.close()

print('----------------------------')

f1 = open('s.pickle', 'rb')
s1 = pickle.load(f1)
print(s1)
