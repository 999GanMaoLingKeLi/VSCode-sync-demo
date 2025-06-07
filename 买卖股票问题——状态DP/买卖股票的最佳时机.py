# prices=[7,1,5,3,6,4]
# n=len(prices)
# ans=0
# for i in range(n):
#     right=n-1
#     while i<right:
#         if prices[i]<=prices[right]:
#             ans=max(ans,prices[right]-prices[i])
#         else:
#             right-=1
# print(ans)
prices = [7, 1, 5, 3, 6, 4]
min_price=float('inf')
max_profit=0
for price in prices:
    if price < min_price:
        min_price = price
    else:
        max_profit = max(max_profit, price - min_price)