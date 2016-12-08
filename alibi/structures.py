import collections
import heapq
from graphviz import Digraph

def _def_get_node_id(node):
  return node['id']
def _def_get_father_id(node):
  return node['father']
def _def_node_dot_label(node):
  return 'lab_'+str(_def_get_node_id(node))

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

  def gv_graph(self,title,fmt='svg',file=None, view=True, f_node_dot_label=_def_node_dot_label):
    dot = Digraph(comment=title)
    dot.engine = 'circo'
    dot.attr('node', shape='record')
    for node in self.nodes:
      label=f_node_dot_label(self.nodes[node])
      dot.node(str(node),label)
      #for each node e connect with each child 
      list(map(lambda nn,sn=str(node): dot.edge(sn,str(nn),''),self.edges.get(node,[])))
    if file:
      dot.format = fmt
      dot.render(file,view=view)
    return dot.source

  def gv_path(self,node_id, f_get_node_id=_def_get_node_id, f_get_father_id=_def_get_father_id,title='path to node',fmt='svg',file=None, view=True, f_node_dot_label=_def_node_dot_label):
    dot = Digraph(comment=title)
    dot.attr('node', shape='record')
    next_node = self.get_node(node_id)
    while next_node:
      child_id = f_get_node_id(next_node)
      label=f_node_dot_label(next_node)
      dot.node(str(child_id),label)
      father_id = f_get_father_id(next_node)
      next_node = self.get_node(father_id)
      if next_node:
        dot.edge(str(father_id),str(child_id),'')   
    if file:
      dot.format = fmt
      dot.render(file,view=view)
    return dot.source

class NodeGraph(Graph):

  def _fst_add_node(self,node,f_get_node_id=_def_get_node_id):
    node_id = f_get_node_id(node)
    exist_node = self.nodes.get(node_id,None)
    if not exist_node:
      self.nodes[node_id] = node

  def __init__(self):
    super(self.__class__,self).__init__()
    self.nodes = {}

  def connect(self,node_1,node_2,f_get_node_id=_def_get_node_id,bi=False):
    id_1 = f_get_node_id(node_1)
    id_2 = f_get_node_id(node_2)
    self._fst_add_node(node_1)
    self._fst_add_node(node_2)
    super(self.__class__,self).connect(id_1,id_2)

  def gprint(self,f_print_node=None):
    super(self.__class__,self).gprint()
    #print(self.nodes)
    if callable(f_print_node):
      for node_id in self.nodes:
        f_print_node(self.nodes[node_id])

  def get_node(self,node_id):
    return self.nodes.get(node_id,None)

class WeightedNodeGraph(NodeGraph):

  def __init__(self):
    super(self.__class__,self).__init__()
    self.weights = {}
  
  def connect(self,node_1,node_2,f_weight,f_get_node_id=_def_get_node_id,bi=False):
    super(self.__class__,self).connect(node_1,node_2,f_get_node_id=f_get_node_id,bi=bi)
    if calable(f_weight):
      id_1 = f_get_node_id(node_1)
      id_2 = f_get_node_id(node_2)
      w_1 = f_weight(node_1,node_2)
      if not self.weights.get('id_1',None):
        self.weights['id_1'] = {}
      self.weights['id_1']['id_2'] = w_1
      if bi:
        if not self.weights.get('id_2',None):
          self.weights['id_2'] = {}
        w_2 = f_weight(node_2,node_1)
        self.weights['id_2']['id_1'] = w_2

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
  
  def put(self, x, priority=0):
    heapq.heappush(self.elements, (priority, x))
  
  def get(self):
    return heapq.heappop(self.elements)[1]