queue = []       
visited = []      
path = []          
tree_1 = {
    "a": ["b", "c"],
    "b": ["f", "d"],
    "c": ["e"],
    "e": ["g", "h"]
}

tree_2 = {
    "a": ["b", "c"],
    "b": ["f", "d"],
    "c": ["e"],
    "e": ["g", "h"]
}

tree_3 = {
    "a": ["b", "d"],
    "b": ["f"],
    "d": ["e", "g"],
    "e": ["h"]
}

tree_4 = {
    "a": ["b", "c", "d"],
    "b": ["e", "f"],
    "c": ["g"],
    "d": ["h"]
}

tree_5 = {
    "a": ["b"],
    "b": ["c"],
    "c": ["d"],
    "d": ["g"]
}


def bfs(tree, start, result):
    queue = []        
    visited = []        
    parent = {}         

    queue.append(start)  
    visited.append(start)
    parent[start] = None  

    while queue:
        current = queue.pop(0)  
        if current == result:   
            break
        for neighbor in tree.get(current, []): 
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)
                parent[neighbor] = current  

    
    path = []
    current = result
    while current is not None:
        path.insert(0, current)  
        current = parent[current]
    print(f"Duyệt các đỉnh: {visited}")
    return path  


path_1 = bfs(tree_1, "a", "g")
print(f"Đường đi từ a đến g cua tree_1: {path_1}")
print()
path_2 = bfs(tree_2, "a", "h")
print(f"Đường đi từ a đến h cua tree_2: {path_2}")
print()
path_3 = bfs(tree_3, "a", "e")
print(f"Đường đi từ a đến e cua tree_3: {path_3}")
print()
path_4 = bfs(tree_4, "a", "f")
print(f"Đường đi từ a đến f cua tree_4: {path_4}")
print()
path_5 = bfs(tree_5, "a", "g")
print(f"Đường đi từ a đến g cua tree_5: {path_5}")




