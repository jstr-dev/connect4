# Connect 4

# Imports
from time import sleep
from os import system

# Class
class Connect4:
    # When a game is initialized 
    def __init__(self):
        self.gamestate = False
        self.currentPl = 1
        self.animDelay = 0.2 #seconds (initial if gravity is on)
        self.animGravity = 0.5 # Multiplier or false

        # Set up data
        self.data = []
        for x in range(0, 6):
            self.data.insert(len(self.data) + 1, ["  ", "  ", "  ", "  ", "  ", "  ", "  "])

        self.layout = """
            C1       C2       C3       C4       C5       C6       C7
        ----------------------------------------------------------------
        |        |        |        |        |        |        |        |
        |   %s   |   %s   |   %s   |   %s   |   %s   |   %s   |   %s   |
        |        |        |        |        |        |        |        |
        ----------------------------------------------------------------
        |        |        |        |        |        |        |        |
        |   %s   |   %s   |   %s   |   %s   |   %s   |   %s   |   %s   |
        |        |        |        |        |        |        |        |
        ----------------------------------------------------------------
        |        |        |        |        |        |        |        |
        |   %s   |   %s   |   %s   |   %s   |   %s   |   %s   |   %s   |
        |        |        |        |        |        |        |        |
        ----------------------------------------------------------------
        |        |        |        |        |        |        |        |
        |   %s   |   %s   |   %s   |   %s   |   %s   |   %s   |   %s   |
        |        |        |        |        |        |        |        |
        ----------------------------------------------------------------
        |        |        |        |        |        |        |        |
        |   %s   |   %s   |   %s   |   %s   |   %s   |   %s   |   %s   |
        |        |        |        |        |        |        |        |
        ----------------------------------------------------------------
        |        |        |        |        |        |        |        |
        |   %s   |   %s   |   %s   |   %s   |   %s   |   %s   |   %s   |
        |        |        |        |        |        |        |        |
        ----------------------------------------------------------------
"""

        # Logo
        self.logo = """
          _____                                         _       _  _   
         / ____|                                       | |     | || |  
        | |        ___    _ __    _ __     ___    ___  | |_    | || |_ 
        | |       / _ \  | '_ \  | '_ \   / _ \  / __| | __|   |__   _|
        | |____  | (_) | | | | | | | | | |  __/ | (__  | |_       | |  
         \_____|  \___/  |_| |_| |_| |_|  \___|  \___|  \__|      |_|
     
                                                                by Adam
  """

    def start(self, counter1="P1", counter2="P2"):
        self.counters = [counter1, counter2]
        self.shouldRestart = False
        self.run()


    def print(self, msg, isInput=False, inputRestrictions=False, isInt=False):
        if (not isInput):
            print("[Connect 4]", msg)
            return

        err = False
        while True:
            if (err): self.print("Incorrect input, please try again.")
            inputted = input("[Connect 4] " + msg)
            if (inputted.lower() == "_exit"): raise Exception("lol")

            if (isInt):
                try:
                    inputted = int(inputted)
                except:
                    err = True
                    self.refresh()
                    self.board()
                    continue
            else:
                inputted = inputted.lower()
            
            if (inputRestrictions != False) and (inputted not in inputRestrictions):
                err = True
                self.refresh()
                self.board()
                continue

            return inputted
            break
                
    
    def restart(self):
        response = self.print("Would you like to restart? [Y/N]: ", True, ["y", "n"])

        # Nope
        if (response == "n"):
            self.refresh()
            self.board()
            self.print("Alright, thanks for playing!")
            self.print("Press any key to exit the program...", True)
            return

        self.shouldRestart = True


    def getPlayer(self, counter):
        index = 1

        for c in self.counters:
            if (c == counter): return index
            index += 1
    

    def refresh(self):
        system("cls")
        print(self.logo)


    def board(self):
        tbl = []
    
        for row in self.data:
            tbl += row
            
        print(self.layout % tuple(tbl))
    

    def place(self, column):
        delay = self.animDelay
        
        for i, row in enumerate(self.data):
            if (row[column] == "  "):
                if (i != 0):
                    self.data[i - 1][column] = "  "
                    sleep(delay)

                    if (self.animGravity):
                        delay = delay * self.animGravity

                self.data[i][column] = self.counters[self.currentPl - 1]
                self.refresh()
                self.board()


    def check(self):
        rows = [0, 0, 0, 0, 0, 0]
        columns = [0, 0, 0, 0, 0, 0, 0]
        rev = self.data[::-1]
        
        for rowId, row in enumerate(reversed(self.data)):  
            # Horizontally
            for counter in row:
                data = rows[rowId]
                
                if (counter == "  "): continue 
                if (data == 0) or (data[0] != counter):
                    rows[rowId] = [counter, 1]
                    continue

                if (data[1] + 1) >= 4 and (data[0] != "  "):
                    return data[0]
                
                rows[rowId] = [counter, data[1] + 1]
                
            # Vertically 
            for colId, counter in enumerate(row):  
                data = columns[colId]
                
                if (counter == "  "): continue 
                if (data == 0) or (data[0] != counter):
                    columns[colId] = [counter, 1]
                    continue

                if (data[1] + 1) >= 4 and (data[0] != "  "):
                    return data[0]
                
                columns[colId] = [counter, data[1] + 1]

            # Diagonally
            for colId, counter in enumerate(row):
                # Lets check this direction [/]
                indiag = 1
                index = 1
                while True:
                    try:
                        nextCounter = rev[rowId + index][colId + index]
                        if (nextCounter == counter) and (counter != "  "):
                            indiag += 1

                            if (indiag >= 4):
                                return counter
                        elif (counter != "  "):
                            indiag = 1
                    except:
                        break
                    
                    index += 1

                # Lets check this direction [\]
                indiag = 1
                index = 1
                while True:
                    try:
                        nextCounter = rev[rowId + index][colId - index]
                        if (nextCounter == counter) and (counter != "  "):
                            indiag += 1

                            if (indiag >= 4):
                                return counter
                        elif (counter != "  "):
                            indiag = 1
                    except:
                        break
                    
                    index += 1

        return False
    
    # onTick
    def run(self):
        self.gamestate = True

        # Start
        self.refresh() 
        self.board()
        
        while self.gamestate:
            # Get column
            column = self.print("Player " + str(self.currentPl) + " please choose a column [1 - 7]: ", True, range(1, 8), True)

            # Place
            self.place(column - 1)

            # Check if a win occured
            win = self.check()

            if (win):
                player = str(self.getPlayer(win))
                self.print("Player " + player + " wins! Congratulations!")
                self.gamestate = False
            
            # Change player
            self.currentPl = (self.currentPl == 1 and 2 or 1)

        self.restart()


def init():
    game = Connect4()
    game.refresh()
    game.print("Welcome to Connect 4!")
    game.print("Press any key to begin...", True)
    game.start()

    # Restarted?
    if (game.shouldRestart):
        i = 3
        for x in range(1, 4):
            game.refresh() 
            game.board()
            game.print("Restarting in " + str(i) + " seconds...")
            sleep(1)
            i -= 1
        init()

init()
