import numpy as np
from alibi.structures import Graph
from alibi.path_st import get_id, breadth

GAP = 0
PUZZLE_SIDE = 3

#numpy helpers
def where_gap(state):
  res = np.where(state==0)
  return (res[0][0],res[1][0])

#State Codification
def random_is():
  """
  randomize initial state
  """
  return  np.random.permutation(range(PUZZLE_SIDE**2)).reshape((PUZZLE_SIDE, PUZZLE_SIDE))

##Initial State (test state)
#IS = np.matrix('2,8,3;1,6,4;7,0,5')
IS = np.matrix('0,2,3;1,8,4;7,5,6')
##Goal State
GS = np.matrix('1,2,3;8,0,4;7,5,6')

#Production Rules
def move_up(state):
  """
  move 0 up: move gap up (it is equivalent to move an eight puzzle piece down)
  """
  gap_xy = where_gap(state)
  if gap_xy[0] == 0:
    raise Exception('You can\'t do that!')
  num = state[gap_xy[0]-1,gap_xy[1]]
  state[gap_xy[0]-1,gap_xy[1]] = GAP
  state[gap_xy[0],gap_xy[1]] = num
  return state

def move_down(state):
  """
  move 0 down: move gap down (it is equivalent to move an eight puzzle piece up)
  """
  gap_xy = where_gap(state)
  if gap_xy[0] == PUZZLE_SIDE-1:
    raise Exception('You can\'t do that!')
  num = state[gap_xy[0]+1,gap_xy[1]]
  state[gap_xy[0]+1,gap_xy[1]] = GAP
  state[gap_xy[0],gap_xy[1]] = num
  return state

def move_right(state):
  """
  move 0 right: move gap right (it is equivalent to move an eight puzzle piece left)
  """
  gap_xy = where_gap(state)
  if gap_xy[1] == PUZZLE_SIDE-1:
    raise Exception('You can\'t do that!')
  num = state[gap_xy[0],gap_xy[1]+1]
  state[gap_xy[0],gap_xy[1]+1] = GAP
  state[gap_xy[0],gap_xy[1]] = num
  return state

def move_left(state):
  """
  move 0 left: move gap left (it is equivalent to move an eight puzzle piece right)
  """
  gap_xy = where_gap(state)
  if gap_xy[1] == 0:
    raise Exception('You can\'t do that!')
  num = state[gap_xy[0],gap_xy[1]-1]
  state[gap_xy[0],gap_xy[1]-1] = GAP
  state[gap_xy[0],gap_xy[1]] = num
  return state

#Utilities
def goal_state_reached(state):
  return (state == GS).all()

##ops list
ops = [
  move_left,
  move_up,
  move_right,
  move_down
]
##Constraints
CS = [
  (1,0), #col is first
  (0,0), #row is first
  (1,PUZZLE_SIDE-1), #col is side
  (0,PUZZLE_SIDE-1), #row is side
]

def check_cons(state,op_id):
  cs = CS[op_id]
  gap_xy = where_gap(state)
  return gap_xy[cs[0]] != cs[1]

##State production
def f_open_node(graph,current):
  def new_node(state,op):
    #apply op in state and generate new node
    new_state=op(np.copy(state))
    return dict(id=get_id(),state=new_state)
  open_nodes = []
  #branch all available states from current
  for i,op in enumerate(ops):
    if check_cons(current['state'],i):
      node = new_node(current['state'],op)
      graph.connect(current['id'],node['id'])
      open_nodes.append(node)
  return open_nodes

def f_reached(node):
  return goal_state_reached(node['state'])

def main():
  g = Graph()
  print('Goal State:')
  print(GS)
  #state = random_is()
  nodo = dict(id=get_id())
  nodo['state'] = IS#random_is()
  print('Initial State:')
  print(nodo['state'])

  success,visited,id_goal = breadth(g,nodo,f_open_node,f_reached=f_reached,verbose=True)

  g.gv_graph('8-puzzle example')

  if success:
    print('success!')
  else:
    print('failure...')

  print(visited)

if __name__ == "__main__":
  main()