import math


def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append(int(bin(i)[2:]))
  return m

get_bin = lambda x, n: format(x, 'b').zfill(n)
# print('отправкка числа 300 (отсоси у водителя сельскохозяйственной техники)')
# print(get_bin(300,16), '- число')
# print(get_bin((32768>>8)&0b0000000011111111,8))
# print(get_bin((32768)&0b0000000011111111,8))
# print(get_bin((300>>8)&0b0000000011111111,8))
# print(get_bin(300&0b0000000011111111,8))
# print(get_bin((0b0111110000000000>>8)&0b0000000011111111,8))
# print(get_bin((0b0111110000000000)&0b0000000011111111,8))
print((31744>>8)&(0b0000000011111111))
# print(bytes(300&0b0000000011111111))
# print(0b101)