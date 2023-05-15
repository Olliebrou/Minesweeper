import random


def make_grid(difficulty):
    '''
    This function takes in a float value between 0 and 1 as the users chosen
    difficulty(1 being imposible to beat and 0 being impossible to not beat).
    It then produces a grid of -'s and #'s where the #'s are the 'bombs'
    The grid is then sent the adj_check function where all of the -'s are replaced with
    the number of adjacent #'s.

    :param difficulty: float value between 0 - 1
    :return: 2D array of integers and #'s
    '''

    grid = [["-"] * 10 for i in range(10)]
    for i in range(10):
        for j in range(10):
            if random.random() < difficulty:
                grid[i][j] = "#"
            else:
                grid[i][j] = "-"
    for i in range(10):
        for j in range(10):
            grid[i][j] = adj_count(grid, i, j)
    return grid


def adj_count(grid,row,col):
    '''
    Takes in a 2D array of #'s and -'s and the indices of the value to be tested.
    Then counts and returns the adjacent number of #'s to the value.

    :param grid: 10x10 array of #'s and -'s
    :param row: index of the row
    :param col: index of the column
    :return: integer as the number of #'s adjacent to the item in a grid
    '''
    count = 0
    if grid[row][col] != "#":               # Making sure number is not a "#"
        for i in range(max(0, row-1), min(row+2, 10)):        # Loops through rows before and after item
            for j in range(max(0, col-1), min(col+2, 10)):    # Loops through columns before and after
                if grid[i][j] == "#":
                    count += 1              # Adds 1 to count when "#" is encountered
        # Returns the number of "#" adjacent to item
    else:
        # If the item itself is a "#" it just returns "#"
        count = "#"
    return count


def print_grid(grid, score):
    # Print the column numbers
    print("   " + " ".join("{:2d}".format(col) for col in range(1, 11)) + "  Score: " + str(score))

    # Print the row numbers and the grid
    for i, row in enumerate(grid):
        print("{:2d}  ".format(i+1) + "  ".join("{:2>}".format(element) for element in row))


def empty_space(grid, player_grid, row, col):
    '''
    Function to recursively expose all adjacent open space(where there are no adjacent bombs) in
    the player's grid if the chosen tile is in an open space.

    :param grid: The hidden game grid as a 2D array of #'s and integers
    :param player_grid: The grid the player sees
    :param row: Index of the value's row
    :param col: Index of the value's column
    :return: The player's grid with all connected open space exposed
    '''
    player_grid[row][col] = " "                             # Exposing the chosen open block
    for i in range(max(0, row-1), min(row+2, 10)):          # Looping through adjacent blocks
        for j in range(max(0, col - 1), min(col + 2, 10)):
            # When an open space is encountered, it is changed into a "-" in the hidden grid
            # This is to avoid an endless recursion as the function would keep going back and forwards
            # between the open spaces.
            if grid[i][j] == 0:
                grid[i][j] = "-"
                empty_space(grid, player_grid, i, j)        # Recursively sending back into the function
            elif isinstance(grid[i][j], int):               # Checking if it is an int(edge of open space)
                player_grid[i][j] = grid[i][j]              # Exposing that value on the player's grid

    return player_grid

def count(grid, value):
    '''
    Counts number of times a value appears in the grid
    :param grid: 2D array
    :param value: String value
    :return: integer
    '''
    count = 0
    for row in grid:
        for col in row:
            if col == value:
                count += 1
    return count

def heading():
    header = r'''
 __  __ ___ _   _ _____ ______        _______ _____ ____  _____ ____  
|  \/  |_ _| \ | | ____/ ___\ \      / / ____| ____|  _ \| ____|  _ \ 
| |\/| || ||  \| |  _| \___ \\ \ /\ / /|  _| |  _| | |_) |  _| | |_) |
| |  | || || |\  | |___ ___) |\ V  V / | |___| |___|  __/| |___|  _ < 
|_|  |_|___|_| \_|_____|____/  \_/\_/  |_____|_____|_|   |_____|_| \_\
        '''
    print(header)
    print("\nWelcome to MINESWEEPR!\n\n"
          "How to play:\n"
          "Choose a difficulty from 1(easy) - 10(impossible)\n"
          "Enter the row and column of the tile you would like to expose\n"
          "If the number in the tile shows the number of bombs in the adjacent tiles\n"
          "Choose wisely! If you choose a tile that is a bomb you loose!\n"
          "Try and choose all of the empty tiles until there are only bombs left\n"
          "Good luck!\n\n")

def play_game():
    '''
    Main game function. Initialises the game by letting user choose a difficulty
    then uses that difficulty to make a game grid. Uses error handling to make sure the
    user inputs valid numbers.
    Then uses a while loop to keep the game going until a bomb is chosen or there are no
    more unrevealed tiles.
    '''
    player_grid = [["*" for i in range(10)] for j in range(10)]
    difficulty = input("Enter the number of your chosen difficulty. 1(easy) - 10(impossible): ")
    if difficulty.isdigit() and 0 < int(difficulty) < 11:
        difficulty = int(difficulty)
        difficulty /= 15
        game_grid = make_grid(difficulty)
    else:
        print("Invalid input. Please enter a number from 1 - 9")
        play_game()
    available_tiles = 100 - count(game_grid, "#")
    score = 0
    while available_tiles >= 0:
        print_grid(player_grid, score)
        try:
            row = int(input("Choose a row")) - 1
            col = int(input("Choose a column")) - 1
            player_grid[row][col] = game_grid[row][col]
            if game_grid[row][col] == 0:
                player_grid = empty_space(game_grid, player_grid, row, col)
            elif game_grid[row][col] == "#":
                print("!!!YOU HIT A BOMB!!!")
                print_grid(player_grid, score)
                break
        except TypeError:
            print("That's not a number! Please only enter numbers 1,2,3,4,5,6,7,8,9,10")
        except IndexError:
            print("That's not a valid row/column! Please only enter numbers 1,2,3,4,5,6,7,8,9,10")
        finally:
            score = int(((100 - count(player_grid, "*")) / (100 - count(game_grid, "#"))) * 10)
            available_tiles = count(player_grid, "*") - count(game_grid, "#")
    print("Game over!")
    print(f"SCORE: {score}")

heading()
play_game()