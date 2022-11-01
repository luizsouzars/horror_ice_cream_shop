import pandas as pd
import os

def cls():
    '''Clear terminal'''
    os.system('cls')

def find(graph:dict, start:str, end:str, path =[]) -> list:
    '''Find a path between two flavors, if exists
        inputs:
            graph: dict graph
            start: init flavor
            end: target flavor
            path: recursive argument to save a partial path between two flavors
        output:
            list with one or more paths between two flavors
    '''
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

def read_txt(file:str) -> list:
    '''Read a file with a graph connections
        input:
            file: str with name and path of the file
        output:
            flavors: list with all flavors presents in file
            links: list with connections between a flavor and other flavor
        '''
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
    '''Cretate a graph
        input:
            flavors: list with all flavors presents in file
            links: list with connections between a flavor and other flavor
        output:
            graph: dict with flavors adjacency list
    '''
    def _fill_links(links):
        '''Fill flavors dataframe with 1 where exists link between de flavor in column and row flavor
            inputs:
                links: list with connections between a flavor and other flavor
        '''
        for l in links:
            col = l[0]
            row = l[1]
            df_flavors.loc[row][col] = 1
    
    df_flavors = pd.DataFrame(index=flavors,columns=flavors).fillna(0)
    _fill_links(links)

    graph = {}
    for flavor in df_flavors.columns:
        graph[flavor] = df_flavors.loc[df_flavors[flavor]==1,[flavor]].index.to_list()
    return graph

def cups(flavors:list,graph:dict):
    '''Count how many possibilities of cups with 2 or 3 flavors are possible.
        inputs:
            flavors: list with all flavors presents in file
            graph: dict with flavors adjacency list
        outputs:
            cup2: List with all possible 2 flavors combinations 
            count2: integer of len(cup2)
            cup3: list with all posible 3 flavors combinations
            count3: integer of len(cup3)

    '''
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