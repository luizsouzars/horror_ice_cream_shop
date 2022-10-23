import pandas as pd

flavors = []
links = []

with open ('teste_1.txt') as f:
    file = f.readlines()
    for l in file:
        l = l.rstrip('\n')
        l = l.split(' - ')
        links.append(l)
        if l[0] not in flavors:
            flavors.append(l[0])
        if l[1] not in flavors:
            flavors.append(l[1])

df = pd.DataFrame(index=flavors,columns=flavors).fillna(0)

for l in links:
    col = l[0]
    row = l[1]
    df.loc[col][row] = 1
    df.loc[row][col] = 1

print(df)