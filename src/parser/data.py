import re
import json
import pandas as pd

def find(haystack, needle):
  hit = haystack[haystack['address']==needle]['id'].astype(int).ravel()
  assert len(hit) == 1
  return hit[0]

def plan():
  data = None
  with open("plan.json", "r") as f:
    data = json.load(f)

  HEXCODES = ["#007bff","#f3ff8c","#b996f9","#e83e8c","#dc3545","#fd7e14","#ffc107","#28a745","#20c997","#17a2b8","#fff","#b1c3d2","#007bff","#28a745","#17a2b8","#ffc107","#dc3545","#f8f9fa","#f43a40"]

  raw = pd.json_normalize(data["values"]["root_module"]["resources"])
  raw['address'] = raw['address'].replace(r'\[\".*\"\]', '', regex=True)
  colors = pd.DataFrame(zip(raw["type"].unique(), HEXCODES), columns=["type", "colour"])

  nodes = raw.merge(colors, how='left', on="type")
  nodes['id'] = nodes.index +1
  nodes['level'] = 0

  d = []
  for _, row in raw[["address", "depends_on"]].iterrows():
    targets = row["depends_on"]
    if type(targets) == list :
      source_id = find(nodes, row["address"])
      for target in targets:
        target_id = find(nodes, target)
        d.append([source_id, target_id])
  edges = pd.DataFrame(d, columns=["source", "target"])
  return nodes, edges


def dfs_levels(edges):
  levels = []
  for _,  node in nodes.iterrows():
    print(node['id'], 1 if type(node['depends_on']) == list else 0)


if __name__=="__main__":
  nodes, edges = plan()
  dfs_levels(edges)