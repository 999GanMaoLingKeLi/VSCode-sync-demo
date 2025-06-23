def solve():
    import sys
    input_data = sys.stdin.read().strip().split()
    T = int(input_data[0])  # 测试组数
    idx = 1
    
    for _ in range(T):
        # 读取 Alice 的 26 张牌
        alice_cards = list(map(int, input_data[idx:idx+26]))
        idx += 26
        # 读取 Bob 的 26 张牌
        bob_cards = list(map(int, input_data[idx:idx+26]))
        idx += 26
        
        # 分别记录 Alice 和 Bob 到手的牌数
        alice_score = 0
        bob_score = 0
        
        # 将要依次打出的牌按照顺序存放在 table 中
        table = []
        
        # 分别用下标追踪 Alice 和 Bob 已经打到哪张牌
        a_ptr = 0
        b_ptr = 0
        
        # 共 52 次出牌操作，Alice 先出 (i 为偶数时是 Alice 出牌)
        for i in range(52):
            if i % 2 == 0:  # Alice 出牌
                cur_card = alice_cards[a_ptr]
                a_ptr += 1
                current_player = "Alice"
            else:           # Bob 出牌
                cur_card = bob_cards[b_ptr]
                b_ptr += 1
                current_player = "Bob"
            
            # 将当前牌放到台面上
            table.append(cur_card)
            
            # 检查是否与之前的牌有相同点数（找最近出现的相同点数）
            # 如果有，收走中间所有牌
            target = cur_card
            j = len(table) - 2  # 从倒数第二个开始往前找
            found_pos = -1
            while j >= 0:
                if table[j] == target:
                    found_pos = j
                    break
                j -= 1
            
            # 如果找到相同点数，则收走 [found_pos, 末尾] 区间的牌
            if found_pos != -1:
                captured_count = len(table) - found_pos
                # 根据是哪位玩家进行累加
                if current_player == "Alice":
                    alice_score += captured_count
                else:
                    bob_score += captured_count
                # 从台面移除这些牌
                table = table[:found_pos]
        
        # 所有人都出完牌后，比较得分
        if alice_score > bob_score:
            print("Alice")
        elif alice_score < bob_score:
            print("Bob")
        else:
            print("Draw")



solve()