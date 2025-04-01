import copy

user = {
  'gather':1111,
  'gather111':1111
}

temp = copy.deepcopy(user)

temp['gather'] = 1

print(user)
print(temp)