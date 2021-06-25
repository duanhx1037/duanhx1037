import gzip
import json
import numpy as np
import pandas as pd

rootpath = "C:\\Users\\duanhx\\Desktop\\Rec+Sys论文\\数据集\\Amazon\\"

datapath = rootpath + "reviews_Office_Products.json.gz"


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


# length为评论条数，即商品总出现次数
occur, length = getOccurrenceForeachItem()
print("所有产品出现次数统计：\n")
print(length)

# 按照出现次数从高到低排序
occur_orderd = sorted(occur.items(), key=lambda x: x[1], reverse=True)
occur = {}
for t in occur_orderd:
    occur[t[0]] = t[1]


# 选择最热的n个数据作为hot item
def getHotItem2():
    cnt = 0
    hotitem = {}
    for k, v in occur.items():
        if cnt < 800:
            hotitem[k] = v
            cnt += 1
        else:
            break
    return hotitem


hotItem = getHotItem2()
hotitem_len = len(hotItem)

# 用于在id和idx之间转化的两个字典
hotid2idx = {}
idx2hotid = {}
for tp in list(enumerate(hotItem.keys())):
    hotid2idx[tp[1]] = tp[0]
    idx2hotid[tp[0]] = tp[1]

metadata_path = rootpath + "meta_Office_Products.json"
data_list = []

with open(metadata_path, 'r', encoding="utf-8") as f:
    for jsonstr in f.readlines():
        # 将josn字符串转化为dict字典
        ameta = json.loads(jsonstr)
        # 只挑出hot的项目
        if ameta["asin"] not in hotItem.keys():
            continue
        arow = [0 for index in range(hotitem_len)]
        curr_id = ameta["asin"]
        arow[hotid2idx[curr_id]] = 1
        # 有可能没有related
        if "related" not in ameta.keys():
            print("无related")
            continue
        related = ameta["related"]  # dict type
        ratio = occur[curr_id] / length
        if "also_buy" in related.keys():
            alsobuy = related["also_buy"]
            for id in alsobuy:
                # 只挑hot的项目
                if id in hotItem.keys():
                    arow[hotid2idx[id]] = 1
        if "also_viewed" in related.keys():
            alsoviewed = related["also_viewed"]
            for id in alsoviewed:
                if id in hotItem.keys():
                    arow[hotid2idx[id]] = 1
        data_list.append(arow)


# print(data_list)
data_np_mat = np.matrix(data_list)

# print(data_np_mat)
data_df = {}
for i in range(hotitem_len):
    # pandas DataFrame的格式，原矩阵中某列对应商品id为key，该列数据作为value
    data_df[idx2hotid[i]] = [it[0] for it in data_np_mat[:, i].tolist()]


df = pd.DataFrame(data_df)

corrdf = df.corr(method='pearson')
print(corrdf.head(10))

import seaborn as sns
import matplotlib.pyplot as plt
import pylab as mpl

# plt显示中文设置
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

plt.figure(figsize=(11, 9), dpi=50)
plt.title("Office Products类商品correlation heatmap")
sns.heatmap(data=corrdf, cmap="OrRd")
plt.show()
