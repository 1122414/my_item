import copy
data = [['wwww',22,31,3],['ggg',7,8,9]]
index = data.index(['ggg',7,8,9])
data[data.index(['ggg',7,8,9])][1]=1
print(index)
print(type(data[0]))

# 注意这里的坑 列表是可变对象。当你使用等号将一个列表赋值给另一个变量时，实际上是将两个变量指向了同一个列表对象。因此，对其中一个变量的修改会影响到另一个变量。
data_te = data
data_te[0][1] = 55
print(data)

data_temp = copy.deepcopy(data)
data_temp[0][1] = 100
print(data)