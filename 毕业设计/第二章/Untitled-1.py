# def largest_rectangle_area(heights):
#     """
#     单调栈方法，O(n) 计算直方图最大矩形面积
#     """
#     stack = []
#     max_area = 0
#     # 在末尾添加一个高度0便于统一处理
#     extended = heights + [0]
#     for i, h in enumerate(extended):
#         # 当当前高度小于栈顶高度时，计算以栈顶为高的最大矩形
#         while stack and extended[stack[-1]] > h:
#             height = extended[stack.pop()]
#             left = stack[-1] + 1 if stack else 0
#             # 宽度为当前下标i减去弹出后栈顶的下标 - 1
#             width = i - left
#             max_area = max(max_area, height * width)
#         stack.append(i)
#     return max_area

# def max_rectangle_after_one_swap(heights):
#     """
#     允许交换一次任意两个柱子的高度，然后求最大矩形面积。
#     演示用的 O(n^2) 解法，对大规模输入不适用。
#     """
#     n = len(heights)
#     # 原始最大面积
#     best = largest_rectangle_area(heights)

#     # 尝试交换任意两根柱子的高度
#     for i in range(n):
#         for j in range(i+1, n):
#             # 交换
#             heights[i], heights[j] = heights[j], heights[i]
#             # 计算新的面积
#             area = largest_rectangle_area(heights)
#             if area > best:
#                 best = area
#             # 交换回去
#             heights[i], heights[j] = heights[j], heights[i]
#     return best

# if __name__ == "__main__":
#     # 读入 n
#     n = 6
#     # 读入 heights
#     heights = [3, 1, 6, 5, 2, 3]
#     # 计算并输出结果
def max_rectangle_after_swap(heights):
    n = len(heights)
    # Compute nearest smaller to left and right
    stack = []  # stores indices
    left = [-1] * n
    right = [n] * n
    for i in range(n):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    stack.clear()
    for i in range(n-1, -1, -1):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)
    # Find baseline max rectangle
    max_area = 0
    best_i = -1
    for i in range(n):
        area = heights[i] * (right[i] - left[i] - 1)
        if area > max_area:
            max_area = area
            best_i = i
    # Region boundaries
    L = left[best_i] + 1
    R = right[best_i] - 1
    # Find two smallest heights in region
    h1 = heights[best_i]
    # Initialize second smallest
    h2 = float('inf')
    for i in range(L, R+1):
        h = heights[i]
        if i == best_i:
            continue
        if h < h2:
            h2 = h
    # If region has only one bar, cannot improve height
    if h2 == float('inf'):
        h2 = 0
    # Find max height outside region
    H_out = 0
    for i in range(0, L):
        if heights[i] > H_out:
            H_out = heights[i]
    for i in range(R+1, n):
        if heights[i] > H_out:
            H_out = heights[i]
    # Compute improved area
    improved_area = 0
    if H_out > h1:
        new_min = min(h2, H_out)
        improved_area = new_min * (R - L + 1)
    return max(max_area, improved_area)

if __name__ == '__main__':
    import sys
    hs = [3,1,6,5,2,3]
    print(max_rectangle_after_swap(hs))
