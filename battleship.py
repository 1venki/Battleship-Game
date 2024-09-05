
import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random
EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"]=10
    data["cols"]=10
    data["boardsize"]=500
    data["cellsize"]=data["boardsize"]//(data["rows"])
    '''data["computer"]=data["rows"],data["cols"]
    data["user"]=data["rows"],data["cols"]'''
    data["computer"]=emptyGrid(data["rows"],data["cols"])
    data["user"]=emptyGrid(data["rows"],data["cols"])
    data["numShips"]=5
    data["tempship"]=[]
    data["userShip"]=0
    data["winner"]=None
    data["maxnumofterms"]=100
    data["currentturns"]=0
    #data["computer"]=addShips(grid,numShips)
    data["computer"]=addShips(data["computer"],data["numShips"])
    return


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data,userCanvas,data["user"],True)
    drawGrid(data,compCanvas,data["computer"],False)
    drawShip(data, userCanvas, data["tempship"])
    drawGameOver(data,userCanvas)
    return



'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym=="Return":
        makeModel(data)


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    if data["winner"]==None:
        a=getClickedCell(data,event)
        if(board=="user"):
            clickUserBoard(data,a[0],a[1])
            if data["userShip"]==5:
                return
        if board=="comp" and data["numShips"]==5 and data["userShip"]==5:
            runGameTurn(data,a[0],a[1])
  

#### STAGE 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid=[]
    for i in range(rows):
        row=[]
        for j in range(cols):
            row.append(1)
        grid.append(row)
    return grid
#print(emptyGrid(5,5))

'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    row=random.randint(1,8) #Generates a random row index between 1 and 8 
    col=random.randint(1,8) #Generates a random column index between 1 and 8
    horver=random.choice([0,1]) #Chooses a random value (0 or 1) to determine if the ship should be placed horizontally or vertically
    ship=[] #Initializes an empty list called ship
    if(horver==0): #Checks if the ship should be placed horizontally (when horver is 0).
        ship=[[row,col-1],[row,col],[row,col+1]]  #If horizontal, creates a ship with three coordinates in the same row.
    else: #Executes if the ship should be placed vertically.
        ship=[[row-1,col],[row,col],[row+1,col]] #If vertical, creates a ship with three coordinates in the same column.
    return ship #Returns the generated ship, which is a list of three coordinates representing the ship's position.

'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for i,j in ship:
        #Checks if the value in the grid at position (i, j) is not equal to EMPTY_UNCLICKED. This means the cell is not empty and has already been clicked or contains a ship.
        if grid[i][j]!=EMPTY_UNCLICKED:
            return False # If the condition in the if statement is met, the function returns False, indicating that the ship cannot be placed on the grid.
    return True  #If the loop completes without returning False, it means all coordinates in the ship can be placed on the grid, so the function returns True, indicating that the ship can be placed.


'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    count=0
    while(True):
        x=createShip() #Calls a function createShip() to generate a new ship
        if checkShip(grid, x) : #Checks if the generated ship x can be placed on the grid without overlapping with existing ships. 
            for i,j in x:  #Iterates over each coordinate (i, j) in the generated ship x
                grid[i][j]=SHIP_UNCLICKED #Marks the grid cell at coordinates (i, j) as containing an unclicked ship
            count+=1 #Increments the count of successfully placed ships.
        if(count==numShips):
            break
    return grid



'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for row in range (len(grid)):
        for col in range (len(grid[row])):
            x0,y0=col*data["cellsize"],row*data["cellsize"]
            x1,y1=x0+data["cellsize"],y0+data["cellsize"]
            if showShips==False:
                color="blue"
                if grid[row][col]==SHIP_CLICKED:
                    color="red"
                if grid[row][col]==EMPTY_CLICKED:
                    color="white"
            elif grid[row][col]==SHIP_UNCLICKED:
                color="yellow"
            elif grid[row][col]==EMPTY_UNCLICKED:
                color="blue"
            elif grid[row][col]==SHIP_CLICKED:
                color="red"
            elif grid[row][col]==EMPTY_CLICKED:
                color="white"
            canvas.create_rectangle(x0,y0,x1,y1,fill=color)
    return

### STAGE 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship): 
    ship.sort()
    if ship[0][1]==ship[1][1]==ship[2][1]: #checks for columns
        if ship[0][0]+1==ship[1][0]==ship[2][0]-1: #for rows
            return True
    return False
 
'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    ship.sort()
    if ship[0][0]==ship[1][0]==ship[2][0]:
        if ship[0][1]+1==ship[1][1]==ship[2][1]-1:
            return True
    return False
    
'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
#to know which row and column are clicked
def getClickedCell(data, event):
    #print(event.x,event.y)
    grid=data["user"]   
    #to identify row 
    #event.x = x coordinate
    #event.y means y-coordinate of the mouse event
    #drawgrid x0,y0=col first
    a=[event.y//data["cellsize"], event.x//data["cellsize"]] #dividing the vertical position (y-coordinate) by the size of each cell to find out which row the mouse click corresponds to.
    if a[0]<len(grid) and a[1]<len(grid[0]):  
        return a #returns the list a, which contains the row and column indices of the clicked cell.


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for row,col in ship:
        x0,y0=col*data["cellsize"],row*data["cellsize"]
        x1,y1=x0+data["cellsize"],y0+data["cellsize"]
        color="white"
        canvas.create_rectangle(x0,y0,x1,y1,fill=color)
    return
 
  

'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if checkShip(grid,ship)==True:
        if isVertical(ship)==True or isHorizontal(ship)==True:
            return True    
    return False


'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if(shipIsValid(data["user"],data["tempship"]))==True:
        for row,col in data["tempship"]:
            data["user"][row][col]=SHIP_UNCLICKED  #inorder to make full ship
        data["userShip"]+=1
    else:
        print("Error")
    data["tempship"]=[]
    return


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["userShip"]==5: #no more ships can be placed.
        return
    if[row,col] in data["tempship"]:
        return #if row,col is aready in tempship it doesnot add again
    if data["user"][row][col]!=EMPTY_UNCLICKED:
        return
    else:
        data["tempship"].append([row,col]) 
        if len(data["tempship"])==3: 
            placeShip(data)
    return


### STAGE 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col]==SHIP_UNCLICKED:
        board[row][col]=SHIP_CLICKED
        if isGameOver(board)==True:
            data["winner"]=player
    elif board[row][col]==EMPTY_UNCLICKED:
        board[row][col]=EMPTY_CLICKED
        if(isGameOver(board))==True:
            data["winner"]=player
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if data["computer"][row][col]==SHIP_CLICKED or data["computer"][row][col]==EMPTY_CLICKED :  #if the user clicks on a cell that has already been clicked (either a ship or an empty space), it doesn't affect the game, but the turn count increases.
        return
    else:
        updateBoard(data, data["computer"], row, col, "user")
    if data["currentturns"]==data["maxnumofterms"]:
        if not (isGameOver(data["user"])==True or isGameOver(data["computer"])==True):
            data["winner"]="draw"
        #data["currentturns"]+=1
    [row,col]=getComputerGuess(data["user"])
    #data["currentturns"]+=1
    updateBoard(data, data["user"], row, col, "comp")
    data["currentturns"]+=1


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''

def getComputerGuess(board):
    while True: #keep generating random guesses until a valid guess is found.
        row=random.randint(0,9)
        col=random.randint(0,9)
        if board[row][col]==SHIP_UNCLICKED:
            return [row,col]
        elif board[row][col]==EMPTY_UNCLICKED:
            return [row,col]



'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in range(len(board)):
        for col in range(len(board)):
            if(board[row][col]==SHIP_UNCLICKED):
                return False #indicating that the game is not over.
    return True #If the function completes both nested loops without finding any unclicked ships, it means that all cells on the board have either been clicked or are empty. 
    

'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner"]=="user":
        canvas.create_rectangle(50, 200, 450, 300, fill = "white")
        canvas.create_text(240,250,text="Congratulations!! You won the game",font=("Calibri",16),fill="green")
        canvas.create_text(250,280,text="Press enter to play again",font=("Calibri",16),fill="green")
    elif data["winner"]=="draw":
        canvas.create_rectangle(50, 200, 450, 300, fill = "white")
        canvas.create_text(250,250,text="Out of moves",font=("Calibri",16),fill="green")
        canvas.create_text(250,280,text="Press enter to play again",font=("Calibri",16),fill="green")
    elif data["winner"]=="comp":
        canvas.create_rectangle(50, 200, 450, 300, fill = "white")
        canvas.create_text(250,250,text="Sorry! You lost",font=("Calibri",16),fill="green")
        canvas.create_text(250,280,text="Press enter to play again",font=("Calibri",16),fill="green")
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data) 
    #data["name"]=value

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop() #runs until main window is closed
    


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":

    print("\n" + "#"*15 + " STAGE 1 TESTS " +  "#" * 16 + "\n")
    test.stage1Tests()

    ## Uncomment these for STAGE 2 
    
    print("\n" + "#"*15 + " STAGE 2 TESTS " +  "#" * 16 + "\n")
    test.stage2Tests()
    

    ## Uncomment these for STAGE 3 ##
  
    print("\n" + "#"*15 + " STAGE 3 TESTS " +  "#" * 16 + "\n")
    test.stage3Tests()
  

    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
