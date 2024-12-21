# Cây đồ thị 1
tree_1 = {
    "a": ["b", "c"],
    "b": ["f", "d"],
    "c": ["e"],
    "e": ["g", "h"]
}

# Cây đồ thị 2
tree_2 = {
    "a": ["b", "c"],
    "b": ["f", "d"],
    "c": ["e"],
    "e": ["g", "h"]
}

# Cây đồ thị 3
tree_3 = {
    "a": ["b", "d"],
    "b": ["f"],
    "d": ["e", "g"],
    "e": ["h"]
}

# Cây đồ thị 4
tree_4 = {
    "a": ["b", "c", "d"],
    "b": ["e", "f"],
    "c": ["g"],
    "d": ["h"]
}

# Cây đồ thị 5
tree_5 = {
    "a": ["b"],
    "b": ["c"],
    "c": ["d"],
    "d": ["g"]
}


def dfs(tree, start, result):
    stack = []         
    visited = []       
    parent = {}        

    stack.append(start)  
    visited.append(start)
    parent[start] = None  

    while stack:
        current = stack.pop()  
        if current == result:  
            break
        for neighbor in tree.get(current, []): 
            if neighbor not in visited:
                visited.append(neighbor)
                stack.append(neighbor)
                parent[neighbor] = current 

    
    path = []
    current = result
    while current is not None:
        path.insert(0, current) 
        current = parent[current]
    print(f"Duyệt các đỉnh: {visited}")
    return path


path_1 = dfs(tree_1, "a", "g")
print(f"Đường đi từ a đến g của tree_1: {path_1}")
print()
path_2 = dfs(tree_2, "a", "h")
print(f"Đường đi từ a đến h của tree_2: {path_2}")
print()
path_3 = dfs(tree_3, "a", "e")
print(f"Đường đi từ a đến e của tree_3: {path_3}")
print()
path_4 = dfs(tree_4, "a", "f")
print(f"Đường đi từ a đến f của tree_4: {path_4}")
print()
path_5 = dfs(tree_5, "a", "g")
print(f"Đường đi từ a đến g của tree_5: {path_5}")

