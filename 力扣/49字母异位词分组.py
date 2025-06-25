###哈希表的key值必须是可哈希的，因为哈希表需要对key调用—hash——（）函数计算出一个整数
#而list是可变的，可以随时进行增删操作，修改后的哈希值就会变，哈希表就找不到原来的槽位
#哈希表就会混乱，因为python设计上禁止使用list作为key

#    groups = defaultdict(list)这是在干什么
# 创造一个默认字典，它的默认值类型是一个list，当你访问一个不存在的键时，defaultdict()
#会自动创建一个空列表【】，并且返回，这样的好处是不需要判断或初始化某一个key是否存在
#排序
mp=collections.defaultdict(list)
for st in strs:
    key="".join(sorted(st))
    mp[key].append(st)
return list(mp.values())
#计数
mp=collections.defaultdict(list)
for st in strs:
    counts=[0]*26
    for ch in st:
        counts[ord[ch]-ord['a']]+=1
    mp[tuple(counts)].append(st)
return list(mp.values())
