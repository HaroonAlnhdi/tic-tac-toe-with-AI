#Haroon Ali Mohammed 202008391

import math
from copy import deepcopy
import numpy as np

X = "X"
O = "O"
EMPTY = None

    #Returns starting state of the board.
def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

#function to get both diagonals of the board
def get_diagonal(board):
    return [[board[0][0], board[1][1], board[2][2]],
            [board[0][2], board[1][1], board[2][0]]]

#function to get all columns of the board.
def get_columns(board):
    columns = []

    for i in range(3):
        columns.append([row[i] for row in board])

    return columns

# function to check if all elements in a row are the same.
def three_in_a_row(row):
    return True if row.count(row[0]) == 3 else False

#returns the player whose turn it is to place on a board. 
def player(board):
    count_x=0
    count_o=0
    for i in board:
        for j in i:
            if(j=="X"):
                count_x=count_x+1
            if(j=="O"):
                count_o=count_o+1
     # Return O if X has more moves, else return X
    return O if count_x > count_o else X

#Returns set of all possible actions (i, j) available on the board.
def actions(board):
   
    action=set() # Initialize an empty set for actions.
    for i, row in enumerate(board):
        for j , vall in enumerate(row):
            if(vall==EMPTY):
                action.add((i,j))# Add the empty cell position as an action.
    return action




    #Returns the board that results from making move (i, j) on the board.
def result(board, action):
    
    
    
    i,j=action
    if(board[i][j]!=EMPTY):
        raise Exception("Invalid Move ")
    next_move=player(board)
    deep_board=deepcopy(board)
    deep_board[i][j]=next_move
    return deep_board

    #Returns the winner of the game, if there is one.
def winner(board):
   
    rows=board+get_diagonal(board) +get_columns(board)
    for row in rows:
        current_palyer=row[0]
        if current_palyer is not None and three_in_a_row(row):
            return current_palyer
    return None


    #Returns True if game is over, False otherwise.
def terminal(board):

    xx=winner(board)
    if(xx is  not None):
        return True # Return True if there is a winner.
    if(all(all(j!=EMPTY for j in i) for i in board)):
        return True # Return True if there are no empty cells.
    return False    # Return False if the game is not over.




        #Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
def utility(board):
  
    xx=winner(board) # Get the winner.
    if(xx==X):
        return 1  # Return 1 if X has won.
    elif(xx==O):
        return -1 # Return -1 if O has won
    else:
        return 0   # Return 0 if there is no winner.
    




#function for alpha-beta pruning maximizing step.
def MaxAlphaBeta(board ,alpha,beta):
    if(terminal(board)== True):
        return utility(board) , None
    vall=float("-inf") #Initialize value to negative infinity.
    best=None   # Initialize best_action to None.
    for action in actions(board):
        min_val=MinAlphaBeta(result(board ,action), alpha, beta)[0]
        if( min_val > vall):
            best=action     # Update best action.
            vall=min_val    # Update value.
        alpha=max(alpha,vall)  # Update alpha.
        if (beta <= alpha):
            break              # Beta cut-off
    return vall,best




    #function for alpha-beta pruning minimizing step.
def MinAlphaBeta(board ,alpha,beta):
    if(terminal(board)== True):
        return utility(board) , None   # Return utility and no action if terminal state
    vall=float("inf")   # Initialize value to positive infinity,
    best=None           ## Initialize best_action to None.
    for action in actions(board):
        max_val=MaxAlphaBeta(result(board ,action), alpha, beta)[0] # Get the maximum value
        if( max_val < vall):
            best=action # Update best action
            vall=max_val
        beta=min(beta,vall)
        if (beta <= alpha):
            break # Alpha cut-off
    return vall,best


    #Returns the optimal action for the current player on the board.
def minimax(board):

    if terminal(board):
        return None                 # Return None if the game is over
    if(player(board)==X):
        return MaxAlphaBeta(board ,float("-inf") ,float("inf"))[1]   # Maximize for X.
    elif(player(board) == O):
        return MinAlphaBeta(board , float("-inf"), float("inf"))[1]  # Minimize for O.
    else:
        raise Exception("Calculation of optimal move failed.")

