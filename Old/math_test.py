import math
from pprint import pprint

number_list = list(range(1,550))

# int_1 = len(number_list)/100
#
# print(int_1)
# int_2 = math.ceil(int_1)
#
# for x in range(1,int_2):
#     offset = int(x*100)
#     offset_front = number_list[:offset] #gets first 100 characters
#     offset_back = offset_front[-100:] #gets last 100?
#     print("this is loop "+str(x)+" out of "+str(int_2))
#     print(offset_back)
#     print()

[number_list[i:i+100] for i in range(0, len(number_list), 100)]
