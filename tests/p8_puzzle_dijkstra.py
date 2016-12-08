import random
import numpy as np
from alibi.structures import WeightedNodeGraph
from alibi.path_st import get_id, dijkstra

random.seed()

GAP = 0
PUZZLE_SIDE = 3

#numpy helpers
def where_gap(state):
  """
  returns "gap" position where is
  """
  res = np.where(state==0)
  return (res[0][0],res[1][0])

#State Codification

##Initial State (test state)
#IS = np.matrix('2,8,3;1,6,4;7,0,5')
IS = np.matrix('2,0,3;1,8,4;7,5,6')
##Goal State
GS = np.matrix('1,2,3;8,0,4;7,6,5')

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

def random_is():
  """
  randomize initial state
  """
  return  np.random.permutation(range(PUZZLE_SIDE**2)).reshape((PUZZLE_SIDE, PUZZLE_SIDE))

def shuffle(state,moves):
  """
  random shuffle of the puzzle
  """
  state_copy = state.copy()
  for n in range(moves):
    while True:
      op_id=random.randint(0,3)
      if check_cons(state_copy,op_id):
        ops[op_id](state_copy)
        break
  return state_copy  

##operation list
ops = [move_left,move_up,move_right,move_down]
##operation representation
arrows = ['<','^','>','v','=']

##Constraints
CS = [
  (1,0), #col is first
  (0,0), #row is first
  (1,PUZZLE_SIDE-1), #col is side
  (0,PUZZLE_SIDE-1), #row is side
]

def check_cons(state,op_id):
  """
  check constraints and returns if state is safe
  to apply the operation op_id
  """
  cs = CS[op_id]
  gap_xy = where_gap(state)
  return gap_xy[cs[0]] != cs[1]

##State production
def f_open_node(graph,current):
  """
  generates new states from current state
  and writes info about
  """
  def new_node(node,i,op):
    #apply op in state and generate new node
    new_state=op(np.copy(node['state']))
    return dict(id=get_id(),state=new_state,num_op=i,father_id=node['id'])
  open_nodes = []
  #branch all available states from current
  for i,op in enumerate(ops):
    if check_cons(current['state'],i):
      node = new_node(current,i,op)
      graph.connect(current,node)
      open_nodes.append(node)
  return open_nodes

def f_reached(node):
  """
  returns if node's state if the goal state
  """
  return goal_state_reached(node['state'])

def f_print_node(node):
  """
  print node's string representation
  """
  if node:
    print('{0}{1}{2}'.format(node['father_id'],arrows[node['num_op']],node['id']))
    print(node['state'])

def main():
  """
  example using the structures and solver
  """
  g = WeightedNodeGraph()
  print('Goal State:')
  print(GS)
  #state = random_is()
  node = dict(id=get_id())
  node['state'] = shuffle(GS,10)#IS#random_is()
  node['father_id'] = 0
  node['num_op'] = len(CS)
  print('Initial State:')
  print(node['state'])

  success,visited,id_goal = breadth(g,node,f_open_node,f_reached=f_reached,verbose=False,f_print=f_print_node)

  if success:
    print('success!')
  else:
    print('failure...')

  print('nodos visitados:')
  visited.qprint(f_print=f_print_node)

  print('solucion:')
  if id_goal:
    id_node = id_goal
    path = []
    next_node = g.get_node(id_node)
    while next_node:
      path.insert(0,next_node)
      next_node = g.get_node(next_node['father_id'])
    
    for node in path:
      f_print_node(node)

if __name__ == "__main__":
  main()