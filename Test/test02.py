# # print(bin(10))
# # print(chr(97))
# # print(ord("q"))
# # print(oct(10))
# # print(hex(10))
#
# """
#     字符串的相关函数
# """
# a = "I love you"
# # 1.查找
# print(a.find("o"))
#
# # print(a.index("r"))
#
# # 2.计数
# print(a.count("o", 0, 3))
#
# # 3.替换
# print(a.replace('o', '4', 1))
#
# # 4.分割
# b = "fwf\t\ngsegewregre   s"
# print(b.split(' '))
#
# # 5. 大写
# print(a.capitalize())
# print(a.title())
#
#
# c = "fsjgklsA"
# print(c.isalpha())
#
# d = "32f"
# print(d.isdigit())
# print(d.isalnum())

# 复习
s = "I love you"
# print(s.replace("4"))
# print(s[::-1])
a = list(s)
print(''.join(a))
print(type(a))
s.isalnum()