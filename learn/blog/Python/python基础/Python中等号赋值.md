### python中等号赋值

python中等号赋值是指向，

data=[['wwww',22,1],['hhht',11,777]]

data_temp = data

则改变data中的值，data_temp也会变，只有在import copy，使用copy.deepcopy拷贝的才是真正独立的

即data_temp = copy.deepcopy(data)