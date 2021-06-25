import gzip
import json
metadata_path = "C:\\Users\\duanhx\\Desktop\\Rec+Sys论文\\数据集\\Amazon\\meta_Office_Products.json.gz"
data_list = []

def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield json.dumps(eval(l))

f = open("meta_Office.strict", 'w')
for l in parse(metadata_path):
  f.write(l + '\n')