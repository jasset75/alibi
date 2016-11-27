from alibi.structures import Graph
from alibi.path_st import get_id, breadth


def f_open_node(graph,current):
  counter = get_id()
  def new_node(n_id):
    fake = {'id': n_id, 'Estado': 'fake_{}'.format(n_id)}
    return fake
  if counter < 25:
    node = new_node(counter)
    graph.connect(current['id'],node['id'])
    if counter < 21 and counter > 15:
      node2 = new_node(get_id()*100)
      graph.connect(current['id'],node2['id'])
      return [node,node2]
    #return the new nodes generated
    return [node]
  else:
    return []

g = Graph()
start_id = get_id()
print('start id',start_id)
start = {'id': start_id, 'Estado': 'uno' }
visited = breadth(g,start,f_open_node,verbose=False)

visited.qprint()