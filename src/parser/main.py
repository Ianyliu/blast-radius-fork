from pyvis.network import Network
import networkx as nx
import re
import json
import pandas as pd
#g = Network(height=800, width=800)
data = None
with open("plan.json", "r") as f:
  data = json.load(f)

resources = pd.json_normalize(data["values"]["root_module"]["resources"])
#print(resources[["address", "depends_on"]])
d = []
for _, row in resources[["address", "depends_on"]].iterrows():
  targets = row["depends_on"]
  if type(targets) == list :
    for target in targets:
      d.append([row["address"], target])

edges = pd.DataFrame(d, columns=["source", "target"])

print(edges)
"""
data = re.sub(r"\\\"", "", data)
g.use_DOT = True
data = " ".join(data.splitlines())
data = data.replace('"', '\\"')
g.dot_lang = data

g.show("index.html")
"""