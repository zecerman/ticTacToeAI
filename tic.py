from random import randint

'''
this is an UNBEATABLE AI for tic tac toe which plays against the player in the terminal.
said AI uses the minimax algorithm to choose its next move
the player is always 'O' and the AI is always 'X', 
the starting player is chosen randomly. (meaning O can go first, I know, I'm sorry for my sacrilege).
'''

def main():
    #init board
    board = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(0)
        board.append(row)
    
    #init vars
    turnsym = ['illegal index', 'X', 'O']#exists solely for printing purposes
    turn = 1
    pturnis = turn + randint(0, 1) #randomly decide who goes first

#game loop
    while True:
#update vars and declare turn is available
        pturnis = 1 if pturnis % 2 == 1 else 2
        print('turn {}, your move {}'.format(turn, turnsym[pturnis])) 
        drawBoard(board)
#logic for who moves
        if pturnis == 1: #must be AIs turn
            aiMove(board)
        else: #must be players turn
            playerMove(board)
#check if game is over
        if checkGameover(board) == abs(10):
            print('game over, {} wins'.format(turnsym[pturnis]))
            drawBoard(board)
            break
        if checkGameover(board) == 1:
            print('cats game, you tied')
            drawBoard(board)
            break
#else: loop     
        turn += 1
        pturnis += 1
        
def aiMove(board):
    #behave randomly on an empty board, for the sake of variety
    checklist = []
    for i in range(3):
        for j in range(3):
            checklist.append(board[i][j])
    if 1 not in checklist and 2 not in checklist:
        row = randint(0, 2)
        col = randint(0, 2)
        board[row][col] = 1
        return 1
    #else: minimax(initial call)*
    best_score = -999 #-inf
    best_move = [-1, -1] #invalid index
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0: #for each empty position on the board, spawn a parent node of minimax()
                board[i][j] = 1
                score = minimax(board, 0, False) #consider all possible consequences of the game, given X has just moved to location i, j (next turn is O, so minimax is False)
                if score > best_score: #if the score we got back is the highest one so far... 
                    best_move = (i, j) #remember that X moving to the location i, j yields best current results
                    best_score = score
                #restore the board to how it was before we considered the game loop given X made a move of i, j so we can check a different move i, j
                board[i][j] = 0 
                
    #commit bestMove to board, haven checked all possible permutations of the game, and return to main()
    board[best_move[0]][best_move[1]] = 1
    return 1
        
def minimax(board, depth, isMaximizing): #NOTE: depth is not used, see NOTE below in function
    
    #we are going to check if the game is over, if this is so, then we have reached the terminal node and want to return the score
    score = checkGameover(board)
    if score == 10:  # AI has won
        return score
    if score == -10:  # Human has won
        return score
    if score == 1:  # There are no more moves and the game is a draw
        return score 
    #reaching here means that we are not yet in the terminal node, so continue with minimax 
    
    '''
    NOTE: traditionally, minimax algs consider depth to limit how much computation they require, but tictactoe is a simple enough game that ALL possible boardstates can be easily computed, 
    thereforen depth is not considered in this implimentation as it would limiting the algorithms scope on the grounds of depth harms accuracy unnecessarily
    (and neither is alpha-beta pruning)
    ((I USED to consider depth and later removed it for the above reason, and I didn't want to change the function definition. Opting instead to spend five times
    longer than it wouldve taken to revise the code, justifying my "laziness" in this note. Hysterical.))
    '''
    
    #we want to check if we are maximizing or minimizing, and then we want to return the best score for that player
    if isMaximizing:  # Maximizing player, AI's move
        best = -999  # -Infinity
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    # Make a move and call minimax again, 1 is always the AI's move, best for the AI is the highest return number
                    board[i][j] = 1
                    best = max(best, minimax(board, depth+1, False))
                    # Undo the move for backtracking!!
                    board[i][j] = 0
        return best

    else:  # Minimizing player, human's move
        best = 999  # Infinity
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    # Make a move and call minimax again, 2 is always the human's move, 'best' for the human is the lowest return number
                    board[i][j] = 2
                    best = min(best, minimax(board, depth+1, True))
                    # Undo the move for backtracking
                    board[i][j] = 0
        return best

def checkGameover(board):
    #this function checks if the game has reached a terminal state, returning 0 if the game is still ongoing
    checklist = []
    #checking rows
    for i in range(3):
        checklist = []
        for j in range(3):
            checklist.append(board[i][j])
        if checklist[0] == checklist[1] == checklist[2] and checklist[0] != 0:
            if checklist[0] == 1:
                return 10
            else:
                return -10
    #checking cols
    for i in range(3):
        checklist = []
        for j in range(3):
            checklist.append(board[j][i])
        if checklist[0] == checklist[1] == checklist[2] and checklist[0] != 0:
            if checklist[0] == 1:
                return 10
            else:
                return -10
    #checking diags
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        if board[1][1] == 1:
            return 10
        else:
            return -10
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
        if board[1][1] == 1:
            return 10
        else:
            return -10
    #checking for tie
    checklist = []
    for i in range(3):
        for j in range(3):
            checklist.append(board[i][j])
    if 0 not in checklist:
        return 1
    #getting here means that no one has won yet
    return 0

def playerMove(board):
    #this function takes player inputs indexed at 1 and converts them into a move on the board if the inputted move is possible
    while True:
        row = input('choose a row 1-3 ')
        col = input('choose a column 1-3 ')
        try:
            #are ints?
            row = int(row) - 1
            col = int(col) - 1
            #are in range of board index && are not already taken locations?
            if board[row][col] != 0:
                print('location on board already taken')
            else:
                #then commit move to board and break loop
                board[row][col] = 2
                break
        #if any of the above checks fail, we try the while loop again with new inputs
        except (ValueError, IndexError, TypeError):  
            print('invalid entry')
    #go back home to main()
    return 1

def drawBoard(board):
    #draw board
    chars= ['#', 'X', 'O']
    for i in range(3):
        for j in range(3):
            print(charForIJinboardis := chars[board[i][j]], end = ' ')
        print() #'\n'
    #go back home to main()
    return 1
      
      
main()