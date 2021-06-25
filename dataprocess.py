import gzip
import json

datapath = "C:\\Users\\duanhx\\Desktop\\Rec+Sys论文\\数据集\\Amazon\\reviews_Baby.json.gz"


def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield json.loads(l)

length = 0

# 统计每个商品出现的次数，以字典形式返回
def getOccurrenceForeachItem():
    occur={}
    cnt = 0
    for review in parse(datapath):
        if review['asin'] in occur.keys():
            occur[review['asin']] += 1
        else: occur[review['asin']] = 1
        cnt += 1
    return occur, cnt

occur, length = getOccurrenceForeachItem()
print("所有产品出现次数统计：\n")
print(length)

occur_orderd = sorted(occur.items(), key=lambda x:x[1], reverse=True)
occur = {}
for t in occur_orderd:
    occur[t[0]] = t[1]

# 按照出现频率的阈值得到热度产品
def getHotItem1(hotrate, occur, length):
    hotitem = {}
    for k, v in occur.items():
        if v / length > hotrate:
            hotitem[k] = v
    return hotitem

# 按照百分比选择最热的数据作为hot item
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

hotItem = getHotItem2(0.05, occur)
print("hot item（共", len(hotItem), "个）：")
# print(hotItem)

hotitem_sum_occur = 0
for hotitemid, hottimes in hotItem.items():
    hotitem_sum_occur += hottimes
print("hot item出现的次数占总访问次数的", hotitem_sum_occur / length)
# example:
# hot item（共 45773 个）：
# hot item出现的次数占总访问次数的 0.9796241394904779

metadata_path = "C:\\Users\\duanhx\\Desktop\\Rec+Sys论文\\数据集\\Amazon\\meta_Ba.json"
sum = 0
hot_dict={}
with open(metadata_path, 'r', encoding="utf-8") as f:
    for jsonstr in f.readlines():
        ameta = json.loads(jsonstr) # 将josn字符串转化为dict字典
        if ameta["asin"] not in hotItem.keys():
            continue
        sum+=1
        # print("编号为", ameta["asin"], "的hot item:", end="")
        if "related" not in ameta.keys():
            print("无related")
            continue
        related = ameta["related"]  # dict type
        if "bought_together" in related.keys():
            # print("有", len(related["bought_together"]), "个一起购买的产品 ", end="")
            cnt = 0
            for item in related["bought_together"]:
                if item in hotItem.keys():
                    cnt += 1
            # print("其中", cnt, "个为hot item，", len(related["bought_together"]) - cnt, "个为非hot item")
            hot_dict[ameta["asin"]] = cnt * 1.0 / len(related["bought_together"])
        else:
            print("没有一起购买的产品")

# hot数据的打包数据是否更多的也是hot?
print(hot_dict)
value_sum = 0.0
for value in hot_dict.values():
    value_sum += value
print(value_sum / len(hot_dict))

