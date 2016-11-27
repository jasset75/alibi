import collections

class Graph:
  def __init__(self):
    self.edges = {}

  def neighbors(self, id):
    return self.edges[id]

  def _fst_edge(self,node_id):
    node = self.edges.get(node_id,None)
    if not node:
      self.edges[node_id] = []

  def connect(self,id_1,id_2,bi=False):
    self._fst_edge(id_1)
    self.edges[id_1].append(id_2)
    if bi:
      self._fst_edge(id_2)
      self.edges[id_2].append(id_1)


class Queue:
  def __init__(self):
    self.elements = collections.deque()

  def qprint(self):
    """
    nq = self.elements.copy()
    for n in nq:
      print(n)
    """
    l = self.elements.list()
    print(l)

  def __iter__(self):
    while not self.empty():
      yield self.get()
  
  def empty(self):
    return len(self.elements) == 0
  
  def put(self, x):
    self.elements.append(x)
  
  def get(self):
    return self.elements.popleft()

  def has(self, x):
    try:
      return self.elements.index(x)
    except ValueError:
      return -1