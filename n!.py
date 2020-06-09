
string = str()
def factor(n,s=string):
    if n <= 1:
        s += '1'
        print(s)
        return 1
    else :
        s += '{0}*'.format(n)
        return n*factor(n-1,s)

a = factor(5)
print(a,string)