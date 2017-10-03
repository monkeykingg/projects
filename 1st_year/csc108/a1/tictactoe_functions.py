import math

EMPTY = '-'

def is_between(value, min_value, max_value):
    """ (number, number, number) -> bool

    Precondition: min_value <= max_value

    Return True if and only if value is between min_value and max_value,
    or equal to one or both of them.

    >>> is_between(1.0, 0.0, 2)
    True
    >>> is_between(0, 1, 2)
    False
    """
    if value >= min_value and value <= max_value:  
    #Check value between min_value and max_value
        return True   #so let min_value <= value <= max_value. 
                      #If this statement is correct, return true.
    else:             #Else, return false.
        return False
   
    # Students are to complete the body of this function, and then put their
    # solutions for the other required functions below this function.

def game_board_full(game_board):
    """ (str) -> bool
    
    Return True if and only if all of the cells in the game board 
    have been chosen.
     
    >>> game_board_full("XOOXXOOX")
    True
    >>> game_board_full("XX-OO-XO-")
    False
    """
    if EMPTY not in game_board:  #Check whether EMPTY in string or not
        return True              #Only if EMPTY is not in the str, return true.
    else:                        #Else, return false.
        return False
    
def get_board_size(game_board):
    """(str) -> int
    
    Return the length of each side of the given tic-tac-toe game board.
    
    >>> get_board_size("XXOOXXOOX")
    3
    >>> get_board_size("OOXX")
    2
    """
    return int(len(game_board) ** 0.5) 
    #Let str become a number which is equal to str's length, 
    #then find the square root of this length and int it. 
    #get the side of game board finally.

def make_empty_board(size):
    """(int) -> str
    
    Return a string for storing information about a tic-tac-toe game board 
    whose size is given by the parameter.
    Each character in the returned string is to have been set to the EMPTY 
    character, to indicate that no cells have been chosen yet.
    
    >>> make_empty_board(2)
    "----"
    >>> make_empty_board(3)
    "---------"
    """
    return size * size * EMPTY 
    #Creat an empty board which is satisfied the size.
    #Square the size and become the length of 
    #game board, then time the string which stand for EMPTY. 
    #Finally, get an empty board.

def get_position(row_index, col_index, board_size):
    """(int, int, int) -> int
    
    Return the str_index of the cell in the string representation of 
    the game board corresponding to the given row and column indices.
    
    >>> get_position(2, 1, 2)
    2
    >>> get_position(1, 2, 2)
    1
    """
    return (row_index - 1) * board_size + col_index - 1  
    #Imagine the game board is a long string, find the position of every 
    #char in this long string, and the first one's index is 0. 
    #Find the regulation between row, col, size and position index. 
    #Finally, locate the position.

def make_move(symbol, row, col, game_board):
    """(str, int, int, str) -> str
    
    Return the tic-tac-toe game board that results when the given symbol is 
    placed at the given cell position in the given tic-tac-toe game board.
    
    >>> make_move("O", 2, 1, "X--O")
    "X-OO"
    >>> make_move("X", 1, 2, "X--O")
    "XX-O"
    """
    game_board_size = int(len(game_board) ** 0.5)         
    #According to get_board_size function, get game board size again
    str_index = (row - 1) * game_board_size + col - 1     
    #According to get_position function,
    #find the position of char in this str
    return game_board[:str_index] + symbol + game_board[str_index + 1:]  
    #Use the result above, apart the whole str and erase the EMPTY str. 
    #Then place the new "X" or "O" in this whole str. 
    #Finally, get a new game board with a new char.

def extract_line(game_board, direction, row_or_column):
    """(str, str, int) -> str 
    
    Return the characters that make up the specified row 
    (when the second parameter is 'across'), 
    column (when the second parameter is 'down') or 
    diagonal from the given tic-tac-toe game board. 
    When the second parameter is 'down_diagonal' or 'up_diagonal', 
    the value of the third parameter should not be used, 
    since the 'down_diagonal' is known to start in 
    the upper-left corner of the game_board, 
    and the 'up_diagonal' is known to start in 
    the lower-left corner of the game_board.
    
    >>> extract_line("XXOO", "down", 2)
    "XO"
    >>> extract_line("XXXOOOXXX", "across", 1)
    "XXX"
    """
    game_board_size = int(len(game_board) ** 0.5)  
    #According to get_board_size function, get game board size again
    if direction == "across":  
        return game_board[game_board_size * (row_or_column - 1):
                          (game_board_size * (row_or_column - 1)) 
                          + game_board_size]
    #Use the result above and numbers of row or col, 
    #imagine the game board is a long string(started char's index is 0), 
    #find the regulation between row, col, size and position index, 
    #then use game_board[:] and get one of the rows in this board.     
    elif direction == "down": 
        return game_board[row_or_column - 1:
                          game_board_size * (game_board_size - 1) 
                          + row_or_column:game_board_size]
    #Use game board size and numbers of row or col, 
    #imagine the game board is a long string(started char's index is 0), 
    #find the regulation between row, col, size and position index, 
    #then use game_board[::] and get one of the columns in this board.     
    elif direction == "down_diagonal":  
        return game_board[::game_board_size + 1]
    #Use game board size and numbers of row or col, 
    #imagine the game board is a long string(starting char's index is 0), 
    #find the regulation between row, col, size and position index, 
    #then use game_board[::] and get down_diagonal in this board.     
    elif direction == "up_diagonal":  
        return game_board[game_board_size ** 2 - 
                          game_board_size:game_board_size - 2:
                          -(game_board_size - 1)]
    #Use game board size and numbers of row or col, 
    #imagine the game board is a long string(starting char's index is 0), 
    #find the regulation between row, col, size and position index, 
    #then use game_board[::] and get up_diagonal in this board.     