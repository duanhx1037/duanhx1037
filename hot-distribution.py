import gzip
import json

datapath = "C:\\Users\\duanhx\\Desktop\\Rec+Sys论文\\数据集\\Amazon\\reviews_Baby.json.gz"


def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield json.loads(l)


# 统计每个商品出现的次数，以字典形式返回
def getOccurrenceForeachItem():
    occur = {}
    cnt = 0
    for review in parse(datapath):
        if review['asin'] in occur.keys():
            occur[review['asin']] += 1
        else:
            occur[review['asin']] = 1
        cnt += 1
    return occur, cnt


occur, length = getOccurrenceForeachItem()
print("所有产品出现次数统计:", length)
print(len(occur))

# 按出现次数从高到低排序
occur_orderd = sorted(occur.items(), key=lambda x: x[1], reverse=True)
occur = {}
for t in occur_orderd:
    occur[t[0]] = t[1]


# 指定出现的频率的阈值来确定热度产品
def getHotItem1(hotrate, occur, length):
    hotitem = {}
    for k, v in occur.items():
        if v / length > hotrate:
            hotitem[k] = v
    return hotitem


# 指定热度产品所占百分比来确定热度产品
def getHotItem2(rate, occur):
    cnt = 0
    hotitem = {}
    for k, v in occur.items():
        if cnt / length < rate:
            hotitem[k] = v
            cnt += 1
        else:
            break
    return hotitem

# 出现次数最多的%5为热度产品
hotItem = getHotItem2(0.05, occur)
print("hot item（共", len(hotItem), "个）：")
# print(hotItem)

hotitem_sum_occur = 0
for hotitemid, hottimes in hotItem.items():
    hotitem_sum_occur += hottimes
print("hot item出现的次数占总访问次数的", hotitem_sum_occur / length)

import matplotlib.pyplot as plt
import pylab as mpl

# plt显示中文设置
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

gap = 1000
plots = {}
cnt = 0
sum = 0
for tp in list(enumerate(occur.values())):
    if cnt < gap:
        sum += tp[1]
        cnt += 1
    else:
        plots[tp[0]] = sum
        sum = 0
        cnt = 0

print(plots)

x = [i for i in plots.keys()]
y = [i for i in plots.values()]

plt.plot(x, y, label="occurrence")
plt.title(u"Baby类产品热度统计")
plt.legend()
plt.show()
