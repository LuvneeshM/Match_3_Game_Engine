
# coding: utf-8

# In[1]:


import pyximport; pyximport.install()
from cythoned import *


# In[2]:


def func():
    random.seed(73)

    mcts_ai = MCTSAgent(None)
    board = Board(7,7)
    board.init()
    start_time = time.time()
    for i in range(20):
        print("Move "  + str(i))
        results_list = []
        start_time = time.time()
        mct_move = mcts_ai.find_next_move(board)
        print(time.time()-start_time)

        matchMade(board, mct_move)


# In[3]:


func()

