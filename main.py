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

def read_txt(file:str):
    flavors = []
    links = []
    with open (file,encoding='utf-8') as f:
        file = f.readlines()
        for l in file:
            l = l.rstrip('\n')
            l = l.split(' -> ')
            links.append(l)
            if l[0] not in flavors:
                flavors.append(l[0])
            if l[1] not in flavors:
                flavors.append(l[1])
    return flavors,links

def graph(flavors:list,links:list):
    def fill_links(links):
        for l in links:
            col = l[0]
            row = l[1]
            df_flavors.loc[row][col] = 1
    
    df_flavors = pd.DataFrame(index=flavors,columns=flavors).fillna(0)
    fill_links(links)

    graph = {}
    for flavor in df_flavors.columns:
        graph[flavor] = df_flavors.loc[df_flavors[flavor]==1,[flavor]].index.to_list()
    
    return graph

def cups(flavors:list,graph:dict):
    count2 = 0
    count3 = 0
    cup2 = []
    cup3 = []
    for flavor in flavors:
        if len(graph[flavor]) > 0:
            itr = set(flavors) - set({flavor})
            for i in itr:
                path = find(graph,flavor,i)
                if len(path)>0:
                    cup2.append((flavor,i))
                    count2 += 1
                for s in path:
                    if len(s)==3:
                        if s not in cup3:
                            cup3.append(s)
                            count3 += 1
                    if len(s) > 3:
                        aux = list(set(s) - set({flavor}))
                        for elm in aux:
                            if elm != s[-1]:
                                if [flavor,elm,s[-1]] not in cup3:
                                    cup3.append([flavor,elm,s[-1]])
                                    count3 += 1
    return cup2, count2, cup3, count3
    
def main():
    for root,_,files in os.walk('t2_casostestes_iniciais'):
        for file in files:
            path = f'{root}\\{file}'
            flavors,links = read_txt(path)
            g = graph(flavors,links)
            cup2, count2, cup3, count3 = cups(flavors,g)
            print(f'-> {file} <-')
            print(f'Cups with two flavors: {count2}')
            print(f'Cups with three flavors: {count3}')
            print()
main()