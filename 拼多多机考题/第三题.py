def solve():
    import sys
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    T = int(next(it))
    out = []
    for _ in range(T):
        n = int(next(it)); m = int(next(it))
        # 读矩阵
        a = [list(map(int, (next(it) for _ in range(m)))) for __ in range(n)]
        ans = 0
        # 从高位到低位尝试
        for b in range(30, -1, -1):
            cand = ans | (1 << b)
            # dp 只保留前一行
            prev = [False] * m
            for i in range(n):
                cur = [False] * m
                for j in range(m):
                    if (a[i][j] & cand) != cand:
                        continue
                    if i == 0 and j == 0:
                        cur[j] = True
                    else:
                        if i > 0 and prev[j]:
                            cur[j] = True
                        elif j > 0 and cur[j-1]:
                            cur[j] = True
                prev = cur
                # 提前剪枝
                # 如果到最后一行都不可能，则无需再往下测试
                if i == n-1 and not prev[m-1]:
                    break
            else:
                # 如果循环未 break，且终点可达
                if prev[m-1]:
                    ans = cand
        out.append(str(ans))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()