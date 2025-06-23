def solve():
    import sys
    data = sys.stdin.read().split()
    it = iter(data)
    T = int(next(it))
    out = []

    for _ in range(T):
        n = int(next(it)); m = int(next(it))
        seg_zeros = []
        seg_ones = []
        # 读取 m 段区间与二进制序列
        for _ in range(m):
            a = int(next(it)) - 1
            b = int(next(it)) - 1
            length = b - a + 1
            zeros = []
            ones = []
            for offset in range(length):
                if next(it) == '0':
                    zeros.append(a + offset)
                else:
                    ones.append(a + offset)
            seg_zeros.append(zeros)
            seg_ones.append(ones)

        # diff[i] 表示第 i 个关卡当前“等级差分值”
        diff = [0] * n

        # 最多做 n 次迭代松弛
        for _ in range(n):
            changed = False
            for k in range(m):
                # 找到该区间中所有 zeros 的最大 diff
                maxz = 0
                for j in seg_zeros[k]:
                    dj = diff[j]
                    if dj > maxz:
                        maxz = dj
                # ones 中每个位置至少要大于 maxz
                target = maxz + 1
                for i in seg_ones[k]:
                    if diff[i] < target:
                        diff[i] = target
                        changed = True
            if not changed:
                break

        # 关卡等级从 0 开始编号，答案是最大编号 + 1
        out.append(str(max(diff) + 1))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()