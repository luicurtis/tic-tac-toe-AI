# a3.py
''' 
    A computer AI program to play tic tac toe against.
    On the computer's turn it will make a list of all legal moves and for each of the moves 
    it does random playouts (simulates playing the game until it is over)
    Out of all the legal moves, the move with the least number of losses is chosen
'''
import random
from datetime import datetime

def printBoard(board):
    ''' Print the game board. Input board is a list '''
    i = 0
    while i < 9:
        print("        ", board[i], "|", board[i+1], "|", board[i+2])
        if i < 6:
            print("        ---+---+---")
        i += 3
    print()
    return None

def firstMove():
    ''' Determine who goes first '''
    turn = random.choice([0, 1])
    if (turn):
        print("    The player will go first. \n     The player will use X and the computer will use O\n")
        return 'player'
    else:
        print("    The computer will go first. \n    The computer will use X and the player will use O\n")
        return 'computer'

def checkWin(board, symbol):
    ''' Check if the current board is a win for the current turn
    
        Returns true if it is a winning board, else false'''
    i = 0
    # horizontal lines
    while i < 9:
        if (board[i] == symbol and board[i+1] == symbol and board[i+2] == symbol):
            return True
        i += 3
    
    # vertical lines
    i = 0
    while i < 3:
        if (board[i] == symbol and board[i+3] == symbol and board[i+6] == symbol):
            return True
        i += 1
    
    # diagonal lines
    if ((board[0] == symbol and board[4] == symbol and board[8] == symbol) or \
         board[2] == symbol and board[4] == symbol and board[6] == symbol):
         return True

    return False

def checkDraw(board):
    ''' Check if the board is a draw (fill up) and there are no more moves to be played

        Return True if in a draw position, else false '''
    if checkWin(board, 'X') or checkWin(board, 'O'):
        return False

    for i in range(len(board)):
        # find empty positions
        if board[i] == ' ':
            return False

    return True

def playerMove(board, symbol):
    ''' Allow the player to enter their move '''
    legalMoves = []
    tempBoard = [' '] * 9

    for i in range(len(board)):
        # find empty positions and create a temp board to print to user
        if board[i] == ' ':
            legalMoves.append(str(i+1))
            tempBoard[i] = str(i+1)
        else:
            tempBoard[i] = board[i]
    legalMoves.sort()

    move = ''
    while move not in legalMoves:
        print("    The player's symbols are", symbol)
        print("    The following are your possible legal moves:", str(legalMoves)[1:-1], "\n")
        printBoard(tempBoard)
        print("Please input one of the following numbers followed by <enter>:", str(legalMoves)[1:-1])
        move = input()
        print()

    board[int(move)-1] = symbol     # make the move
    return None

def legalMoves(board):
    ''' return a list of all legal moves for the board position '''
    legalMoves = []
    for i in range(len(board)):
        if board[i] == ' ':
            legalMoves.append(str(i))
    legalMoves.sort()
    return legalMoves

def makeRandmove(board, moves, symbol):
    ''' make a random move given a list of moves and the symbol '''
    random.seed(datetime.now())
    move = int(random.choice(moves))
    
    board[move] = symbol
    return None

def randPlayout(board, compSymbol, playSymbol, move):
    ''' A random playout is when the computer simulates playing the game until it is over.
        During a random playout, the computer makes random moves for each player until 
        a win, loss, or draw is reached 
        
        Returns true if the computer lost, else false'''

    # copy the board to avoid changing the original
    tempBoard = [' '] * 9
    for i in range(len(board)):
        tempBoard[i] = board[i]
    
    tempBoard[int(move)] = compSymbol    # make the given move
    
    turn = compSymbol
    
    while not checkWin(tempBoard, turn) and not checkDraw(tempBoard):
        # switch turns 
        if turn == compSymbol:
            turn = playSymbol
        else:
            turn = compSymbol
        
        possibleMoves = legalMoves(tempBoard)
        makeRandmove(tempBoard, possibleMoves, turn)
    
    if turn == playSymbol and (not checkDraw(tempBoard)):
        # Player won and it is not a draw
        #print("here")
        return True
    else:
        return False

def play_a_new_game():
    ''' Runs one game of tic tac toe against the AI '''
    print()
    print("***** STARTING A GAME OF TIC TAC TOE ******\n")
    # intialize a new board
    board = [' '] * 9       # ' ' represents a free space
    numRandPlayouts = 1000  # Tested minimal number of playouts to ensure it never loses

    # Determine who goes first
    turn = firstMove()

    # Set up player and computer symbols
    playerSymbol = 'X' if turn == "player" else 'O'
    computerSymbol = 'O' if turn == "player" else 'X'

    turn = 'X'  # first move is always X
    while not checkWin(board, turn) and not checkDraw(board):
        print("***** This is the current board *****\n")
        printBoard(board)
        # Player's turn
        if turn == playerSymbol:
            print("***** It is the PLAYER'S turn *****\n")
            playerMove(board, playerSymbol)
            if checkWin(board, turn):
                break
            turn = computerSymbol   # switch turns

        # Computer's turn
        else:
            possibleMoves = legalMoves(board)
            numLoss = [0] * len(possibleMoves)

            for i in range(len(possibleMoves)):
                for j in range(numRandPlayouts):
                    # Do numRandPlayouts of times 
                    # if rand playout is a win, then increment that move
                    if randPlayout(board, computerSymbol, playerSymbol, possibleMoves[i]):
                        numLoss[i] += 1

            indexOfMinLoss = int(numLoss.index(min(numLoss)))
            moveIndex = int(possibleMoves[indexOfMinLoss])
            board[moveIndex] = computerSymbol
            print("***** The computer has made their move *****\n")

            if checkWin(board, turn):
                break
            turn = playerSymbol
            
    print()
    print("***** The game has ended *****\n")
    if checkDraw(board) and not checkWin(board, turn):
        print("    The game ended in a draw")
    else:
        if turn == computerSymbol:
            print("    The computer won!!!!")
        else:
            print("    The player won!!!!")

    print("    This is the final board:")
    printBoard(board)
    
if __name__ == '__main__':    
    play_a_new_game()