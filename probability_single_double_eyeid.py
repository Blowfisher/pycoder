import itertools
parents_gene =['F','f','F','f']
A = 0
B = 0
count = 0

for ret in itertools.combinations(parents_gene,2):
    if 'F' in ret:
        B += 1
    else:
        A += 1
    count += 1
    prob_A = round(A/count,2)
    prob_B = round(B/count,2)

print(prob_A,prob_B)
#此处有bug 会排列自身