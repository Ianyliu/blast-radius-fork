from pyvis.network import Network
import networkx as nx
from data import *

g = Network(height=800, width=800)

g.add_nodes([1,2,3], value=[10, 100, 400],
                         title=['n1', 'n2', 'n3'],
                         x=[21.4, 54.2, 11.2],
                         y=[100.2, 23.54, 32.1],
                         shape=['box', 'box', 'box'],
                         label=['aws_acm_certificate.internal_https\naws_acm_certificate', 'aws_acm_certificate_validation.internal_validate\naws_acm_certificate_validation', 'aws_ecs_service.neo4j\naws_ecs_service'],
                         color=['#fff', '#fff', '#fff'])
g.add_edge(1,2)
g.add_edge(2,3)

g.set_options("""
const options = {
  "nodes": {
    "font": {
      "face": "monaco"
    }
  },
  "interaction": {
    "zoomSpeed": 0.4
  }
}
""")

g.show('nx.html')