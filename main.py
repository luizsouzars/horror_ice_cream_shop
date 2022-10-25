import pandas as pd
import os

def cls():
    os.system('cls')

def find(graph, start, end, path =[]):
  path = path + [start]
  if start == end:
    return [path]
  paths = []
  for node in graph[start]:
    if node not in path:
      newpaths = find(graph, node, end, path)
    for newpath in newpaths:
      paths.append(newpath)
  return paths

cls()

flavors = []
links = []

# with open ('t2_casostestes_iniciais\casoleonardo10.txt',encoding='utf-8') as f:
with open ('teste_1.txt',encoding='utf-8') as f:
    file = f.readlines()
    for l in file:
        l = l.rstrip('\n')
        l = l.split(' -> ')
        links.append(l)
        if l[0] not in flavors:
            flavors.append(l[0])
        if l[1] not in flavors:
            flavors.append(l[1])

df_flavors = pd.DataFrame(index=flavors,columns=flavors).fillna(0)

for l in links:
    col = l[0]
    row = l[1]
    df_flavors.loc[row][col] = 1

graph = {}
for flavor in df_flavors.columns:
    graph[flavor] = df_flavors.loc[df_flavors[flavor]==1,[flavor]].index.to_list()

print(find(graph,'chocolate_branco','maca_verde'))