import re
import json
import pandas as pd

def plan():
  data = None
  with open("plan.json", "r") as f:
    data = json.load(f)

  HEXCODES = ["#007bff","#6610f2","#6f42c1","#e83e8c","#dc3545","#fd7e14","#ffc107","#28a745","#20c997","#17a2b8","#fff","#6c757d","#343a40","#007bff","#6c757d","#28a745","#17a2b8","#ffc107","#dc3545","#f8f9fa","#343a40"]

  resources = pd.json_normalize(data["values"]["root_module"]["resources"])
  colors = pd.DataFrame(zip(resources["type"].unique(), HEXCODES), columns=["type", "colour"])
  nodes = resources.merge(colors, how='left', on="type")
  d = []
  for _, row in resources[["address", "depends_on"]].iterrows():
    targets = row["depends_on"]
    if type(targets) == list :
      for target in targets:
        d.append([row["address"], target])

  edges = pd.DataFrame(d, columns=["source", "target"])
  return edges, nodes

if __name__=="__main__":
  print(plan())