from alibi.structures import Queue

_id_counter = 0

def get_id():
  global _id_counter
  _id_counter += 1
  return _id_counter

def breadth(graph, start, f_open_node, verbose=True):
  # print out what we find
  open_nodes = Queue()
  visited = Queue()
  open_nodes.put(start)
  #visited.put(start)
  while not open_nodes.empty():
    current = open_nodes.get()
    visited.put(current)
    if verbose:
      print('Visiting ',current['id'])
    new_nodes = f_open_node(graph,current)

    for node in new_nodes:
      if visited.has(node) < 0:
        open_nodes.put(node)
  return visited