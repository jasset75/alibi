import collections
import heapq
from graphviz import Digraph

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

  def __str__(self):
    return str(self.edges)

  def gprint(self):
    print(self.edges)

  def gv_graph(self,title):
    dot = Digraph(comment=title)
    for e in self.edges:
      str_e = str(e)
      dot.node(str_e,str_e)
      dot.edges(filter(lambda x: '{0}{1}'.format(str_e,x),self.edges[e]))
    print(dot.source)

class Queue:
  def __init__(self):
    self.elements = collections.deque()

  def qprint(self,f_print=None):
    nq = self.elements.copy()
    for n in nq:
      if callable(f_print):
        f_print(n)
      else:
        print(n)
    """
    l = self.elements.list()
    print(l)
    """
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

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]
