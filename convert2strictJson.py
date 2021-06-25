import gzip
import json
metadata_path = "C:\\Users\\duanhx\\Desktop\\Rec+Sys论文\\数据集\\Amazon\\meta_Office_Products.json.gz"

# 原json.gz文件解压后得到的json文件均为单引号，无法读取
# 通过下列代码生成的.strict文件，修改后缀为.json后得到符合标准的.json文件

def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield json.dumps(eval(l))

f = open("meta_Office.strict", 'w')
for l in parse(metadata_path):
  f.write(l + '\n')