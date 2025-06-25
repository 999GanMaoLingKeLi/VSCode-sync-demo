import sys
input_data = sys.stdin.read().strip().split()
T = int(input_data[0])  # 测试组数
# idx = 1
# for _ in range(T):
#     # 读取 Alice 的 26 张牌
#     alice_cards = list(map(int, input_data[idx:idx+26]))
#     idx += 26
#     # 读取 Bob 的 26 张牌
#     bob_cards = list(map(int, input_data[idx:idx+26]))
#     idx += 26    
print(input_data)