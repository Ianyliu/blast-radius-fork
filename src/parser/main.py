from pyvis.network import Network
import networkx as nx
from data import *
import pydot
from networkx.drawing.nx_pydot import graphviz_layout


def add_nodes(graph):
  for _, node in nodes.iterrows():
    label = "%s\n%s" % (node['type'], node['address'])
    graph.add_node(node['id'], value=10,
                  level=node['level'],
                  title="%s" % node['id'], # change to 'name'
                  shape='box',
                  label="%s" % node['id'],
                  color=node['colour'])
def add_edges(graph):
  for _, edge in edges.iterrows():
    graph.add_edge(int(edge['source']), int(edge['target']))
  g.show_buttons(filter_='layout')

# g.set_options("""
# const options = {
#   "nodes": {
#     "font": {
#       "face": "monaco"
#     }
#   },
#   "interaction": {
#     "zoomSpeed": 0.4
#   }
# }
# """)

nodes, edges = plan()
g = Network(height=800, width=800, directed=True, layout=True)
prep = nx.DiGraph()
add_nodes(prep)
add_edges(prep)

d = []
for node in prep.nodes:
  print(nx.ancestors(prep, node), nx.descendants(prep, node))
  if nx.ancestors(prep, node) == set():
    d.append([node, 0])
  elif nx.descendants(prep, node) == set():
    d.append([node, 10])
  else: 
    d.append([node, len(list(nx.bfs_layers(prep, node)))])
tmp = pd.DataFrame(d, columns=["id", "level"])
print(tmp)
nodes['level'] = tmp['level']
G = nx.DiGraph()
add_nodes(G)
add_edges(G)

g.from_nx(G)
g.show('nx.html')