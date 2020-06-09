import collections
import matplotlib.pyplot as plt
a = "thank for my like to and the  to for my like would and for"
a_str = a.split(' ')
n = collections.Counter(a_str)

print(n.values())

s = zip(n.values(),n.keys())
print(type(s))
for i in sorted(s,reverse = True):
    print(i)