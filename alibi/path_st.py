from alibi.structures import Queue

_id_counter = 0

def get_id():
  global _id_counter
  _id_counter += 1
  return _id_counter

def breadth(graph, start, f_open_node, f_reached=None, verbose=False, f_print=None):
  # print out what we find
  open_nodes = Queue()
  closed = Queue()
  open_nodes.put(start)
  #closed.put(start)
  while not open_nodes.empty():
    current = open_nodes.get()
    if verbose:
      if callable(f_print):
        f_print(current)
      else:
        print(current)
    closed.put(current)
    #verify goal reached
    if callable(f_reached):
      if f_reached(current):
        return (True,closed,current['id'])
    new_nodes = f_open_node(graph,current)
    for node in new_nodes:
      if closed.has(node) < 0:
        open_nodes.put(node)
  #if open_nodes is empty return failure
  return (not open_nodes.empty(),closed,[])