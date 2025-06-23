def solve():
    import sys
    from collections import deque
    
    input_data = sys.stdin.read().strip().split()
    n = int(input_data[0])
    idx = 1
    
    # 建立邻接表，使用列表存储
    adjacency = [[] for _ in range(n+1)]
    
    # 读入 n-1 条道路，构建树
    for _ in range(n-1):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        idx += 2
        adjacency[x].append(y)
        adjacency[y].append(x)
    
    # 读入新建道路 (a, b)
    a = int(input_data[idx])
    b = int(input_data[idx+1])
    # 将此边加入图中
    adjacency[a].append(b)
    adjacency[b].append(a)
    
    # BFS 计算每个城市到首都 1 的最短距离
    dist = [-1] * (n+1)
    dist[1] = 0
    
    queue = deque([1])
    while queue:
        front = queue.popleft()
        for nxt in adjacency[front]:
            if dist[nxt] == -1:  # 未访问过
                dist[nxt] = dist[front] + 1
                queue.append(nxt)
    
    # 输出结果：从 1..n 依次输出其到首都的最短距离
    for city in range(1, n+1):
        print(dist[city])

if __name__ == "__main__":
    solve()