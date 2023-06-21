# 1. 增
a = ["faf"]
a.append("ff")
a.insert(0, "235")
a.extend([1, 2])
print(a)

# 2. 删
# del a[0]
# print(a)
# a.remove("ff")

# 3. 改
# a[0] = "fesg"
# print(a)

# 4. 查
"i" in a

# a1 = [1,2,3,4]
# b1 = [6,7,8]
# a1.extend(b1)
# for i in a1:
#     print(i)

s = "I love you"
a = list(s)
a.insert(a.index('l'), "really ")
print(''.join(a))
print(a)
a.clear()
print(a)
a = {}
a.setdefault("aa", 33)
a.setdefault("aa", 43)

# 字典
d = {1: 2, 2: 3, 3: 4, 5:1}
print(sorted(d.items(), key=lambda x:x[1]))
d.update({5:6, 7:1})
print(d)