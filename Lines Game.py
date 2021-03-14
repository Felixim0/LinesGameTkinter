from tkinter import *
from time import sleep
from random import randint
import math

window =Tk()
window.configure(background='black')

w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.overrideredirect(1)
window.geometry("%dx%d+0+0" % (w, h))

canvasHeight = round(h, -1)
canvasWidth = round(w, -1)

window.title("Snake Game 2.0")
canvas = Canvas(bg="black",height=canvasHeight,width=canvasWidth,highlightthickness=0)
canvas.grid(column=1,row=1,columnspan=2)

# Constants only to be declared here
startMenuPresent = False
squareNumbers = []
for i in range (2,13):
    nextSquareNumber = i*i
    squareNumbers.append(nextSquareNumber)

def var_states():
    print(singlePlayer.get())

def startGame():
    global noOfDots,firstPlayerName,secondPlayerName,gameType,gt,startMenuPresent
    noOfDots = int(userNoDots.get())
    firstPlayerName = str(p1Name.get())
    secondPlayerName = str(p2Name.get())
    if int(gameType.get()) == 2:
        gt = ("multiPlayer")
    elif int(gameType.get()) == 1:
        gt = ("singlePlayer")
    else:
        gt = "Null"
            
    if (gt == ("multiPlayer")) and (firstPlayerName != "") and (secondPlayerName != ""):
        print("MultiPlayer")
        startMenuPresent = False
        resetGame("None")
    elif gt == ("singlePlayer"):
        print("Single Player")
    else:
        startMenu()

def startMenu():
    global gameType,p1Name,p2Name,userNoDots,startMenuPresent
    startMenuPresent = True
    backgroundColour = "Dark Violet"
    textColour = "Yellow"
    defaultFont = "Helvetica 25 bold"
    
    frame = Frame(window,bg=str(backgroundColour))

    x0 = frame.winfo_screenwidth()/2
    y0 = frame.winfo_screenheight()/2
    canvas.create_window((x0,y0), window=frame, anchor = "center")

    titleLabel= Label(frame, text="The Dot Game 2.0",font = "Arial 40 underline",bg=str(backgroundColour))
    titleLabel.grid(row=0,column=0,columnspan = 3,padx=5,pady=30)
    
    dotsLabel= Label(frame, text="Select Number Of Dots",font = str(defaultFont),bg=str(backgroundColour))
    dotsLabel.grid(row=1,column=0,padx = 10)

    userNoDots = StringVar(frame)
    userNoDots.set("25")
    dotNumber = OptionMenu(frame, userNoDots, *squareNumbers)
    
    dotNumber.config(bg = "Green",font = "Helvetica 10 bold")
    
    dotNumber.grid(row=1,column=1,columnspan = 2,padx = 10)
    dotNumber.config(width=int(canvasWidth/20))

    gameType = IntVar()
    gameType.set(2)
    p1Name = StringVar()
    p2Name = StringVar()
    
    singlePlayerCB = Radiobutton(frame, value = 1, text = "Single Player",fg=str(textColour),selectcolor="black", variable = gameType,font = str(defaultFont),bg=str(backgroundColour),activebackground=str(backgroundColour))
    singlePlayerCB.grid(row = 2, column = 1)
    
    multiPlayerCB = Radiobutton(frame, value = 2, text = "Multi Player",fg=str(textColour),selectcolor="black", variable = gameType,font = str(defaultFont),bg=str(backgroundColour),activebackground=str(backgroundColour))
    multiPlayerCB.grid(row = 2, column = 2)   

    p1EntryBox = Entry(frame,textvariable=p1Name,fg=str(textColour),bg=str(backgroundColour), font = str(defaultFont))
    p1EntryBox.grid(row = 3,column = 1,pady=5)
    p2EntryBox = Entry(frame,textvariable=p2Name,fg=str(textColour),bg=str(backgroundColour), font = str(defaultFont))
    p2EntryBox.grid(row = 4,column = 1,pady=5)

    p1NameLabel= Label(frame, text="Name of P1",font = str(defaultFont),bg=str(backgroundColour))
    p1NameLabel.grid(row=3,column=0,pady=5)
    
    p2NameLabel= Label(frame, text="Name of P2",font = str(defaultFont),bg=str(backgroundColour))
    p2NameLabel.grid(row=4,column=0,pady=5)
    
    button = Button(frame, text="Start Game",font = str(defaultFont),bg=str(backgroundColour),activebackground=str(backgroundColour), command=startGame)
    button.grid(row = 5,column = 0, columnspan = 3,padx=5,pady=30)

    frame.grid_rowconfigure(1, weight=10)
    
def resetGame(winner):
    global dotLocations, perminantLineLocations,squareLocations,rowNumber,playerTurn,greyLines,lineLocations,noOfDots,noOfDotsSQ
    dontRunDots = False
    # if winner is "p1, p2" make stuff happen then startMenu()
    if (winner == "p1") or (winner == "p2") or (winner == "draw"):
        startMenu()
        dontRunDots = True
                
    noOfDotsSQ = math.sqrt( int(noOfDots) )

    print(noOfDots)
    print(noOfDotsSQ)
    
    dotLocations = []
    lineLocations = []
    perminantLineLocations = []
    squareLocations = []

    x = canvasWidth/(noOfDotsSQ + 1)
    y = canvasHeight/(noOfDotsSQ + 1)

    counter = 0
    rowNumber = 0
    playerTurn = 1
    greyLines = False
    
    for i in range (0,int(noOfDots)):
        
        tempArray = [int(x),int(y),"Not Selected",int(i),rowNumber,"Unused",[0,0,0,0]]
        
        dotLocations.append(tempArray[:])
        
        x = x + canvasWidth/(noOfDotsSQ + 1)
        counter = counter + 1
        if counter == (noOfDotsSQ):
            
            x = canvasWidth/(noOfDotsSQ + 1)
            y = y + canvasHeight/(noOfDotsSQ + 1)
            rowNumber = rowNumber + 1
            counter = 0
            
    dotLocations[0][2] = (str("Selected"))
    if dontRunDots == False:
        drawDots()

def drawPerminantLines(): 
    global dotLocations, perminantLineLocations
    
    for i in range(0, len(perminantLineLocations)):
        colour = str(perminantLineLocations[i][0])
        
        canvas.create_line(int(perminantLineLocations[i][1]),int(perminantLineLocations[i][2]),int(perminantLineLocations[i][3]),int(perminantLineLocations[i][4]), fill=colour, width=10)

def checkForWin():
    global dotLocations,squareLocations,noOfDots,noOfDotsSQ
    p2 = p1 = 0

    finishSquares = (int(noOfDotsSQ) - 1)*(int(noOfDotsSQ) - 1)
    
    if len(squareLocations) >= finishSquares:
        for i in range (0,len(squareLocations)):
            if squareLocations[i][0] == "Yellow":
                p2 = p2 + 1
            else:
                p1 = p1 + 1
        if p2 > p1:
            resetGame("p2")
        elif p2 == p1:
            resetGame("Draw")
        elif p1 > p2:
            resetGame("p1")

def drawDots():
    global dotLocations
    canvas.delete("all")
    drawPerminantLines()
    drawBoxes()
    drawLines()
    checkForWin()
    
    for i in range (0,len(dotLocations)):

        halfDifference = 10
        
        if dotLocations[i][2] == "Selected":
            colour = "Red"
        elif dotLocations[i][2] == "hardSelected":
            colour = "grey"
        else:
            colour = "White"
        
        xZ = int(dotLocations[i][0]) - halfDifference
        yZ = int(dotLocations[i][1]) + halfDifference

        xO = int(dotLocations[i][0]) + halfDifference
        yO = int(dotLocations[i][1]) - halfDifference
        
        canvas.create_oval(xZ, yZ, xO,yO, fill=str(colour))#    id = C.create_oval(x0, y0, x1, y1, option, ...)
        
def escape(e):
    global lineLocations, dotLocations, greyLines,startMenuPresent
    if startMenuPresent == False:
        greyLines = False
        for i in range(0,len(dotLocations)):
            if dotLocations[i][2] == "hardSelected":
                dotLocations[i][2] = "Selected"
        lineLocations = []

        drawDots()

def drawLines():
    global lineLocations,greyLines,playerTurn
    if len(lineLocations) > 0:
        greyLines = True

    if int(len(lineLocations)) > 3:
        for i in range (0,len(lineLocations)):
            if lineLocations[i][0] == "highlighted":
                if playerTurn == 1:
                    colour = "Blue"
                else:
                    colour = "Yellow"
            elif lineLocations[i][0] == "unconfirmed":
                colour = "grey"

            if lineLocations[i][0] != "placeholder":
                canvas.create_line(int(lineLocations[i][1]),int(lineLocations[i][2]),int(lineLocations[i][3]),int(lineLocations[i][4]), fill=colour, width=10)

def drawBoxes():
    global squareLocations,secondPlayerName,firstPlayerName

    for i in range(0,len(squareLocations)):
        canvas.create_rectangle(int(squareLocations[i][1]),int(squareLocations[i][2]),int(squareLocations[i][3]),int(squareLocations[i][4]), fill=str(squareLocations[i][0]))

    for i in range(0,len(squareLocations)):
        if squareLocations[i][0] == "Yellow":
            # Player 2
            canvas.create_text(int((int(squareLocations[i][1]) + int(squareLocations[i][3]))/2),int((int(squareLocations[i][2]) + int(squareLocations[i][4]))/2), font = "Times 40 bold", text = str(secondPlayerName),fill = "Black")
        elif squareLocations[i][0] == "Blue":
            # Player 1
            canvas.create_text(int((int(squareLocations[i][1]) + int(squareLocations[i][3]))/2),int((int(squareLocations[i][2]) + int(squareLocations[i][4]))/2), font = "Times 40 bold", text = str(firstPlayerName),fill = "White")

def addPerminantSquare(dotNumber,pt):
    global squareLocations,dotLocations,noOfDotsSQ
    if pt == 1:
        colour = "Blue"
    else:
        colour = "Yellow"
    tempArray = [str(colour),int(dotLocations[dotNumber][0]),int(dotLocations[dotNumber][1]),int(dotLocations[dotNumber-(int(noOfDotsSQ) + 1)][0]),int(dotLocations[dotNumber-(int(noOfDotsSQ) + 1)][1])]

    squareLocations.append(tempArray[:])

def checkForSquares():
    global dotLocations,perminantLineLocations,playerTurn,noOfDotsSQ
    # Puts player turn back to what it originaly was for this check - doesn't effect global variable
    for i in range(0,len(dotLocations)):
        if ((dotLocations[i][6][0] == 1) and (dotLocations[i - int(noOfDotsSQ)][6][2] == 1) and (dotLocations[i - int(int(noOfDotsSQ) + 1)][6][1] == 1) and (dotLocations[i - 1][6][3] == 1)) and (dotLocations[i][5] == "Unused"):
            dotLocations[i][5] = "Used"

            # Square was made so go back to previous players go
            
            if (playerTurn == 1):
                playerTurn = 2
            else:
                playerTurn = 1
                
            addPerminantSquare(i,playerTurn)

        
def enterPressed(e):
    global dotLocations,lineLocations, greyLines,perminantLineLocations,playerTurn,noOfDots,noOfDotsSQ
    if startMenuPresent == False:
        if greyLines == True:
            for i in range (0,len(lineLocations)):
                if lineLocations[i][0] == "highlighted":
                    if playerTurn == 1:
                        colour = "Blue"
                    else:
                        colour = "Yellow"
                    tempArray = [colour,int(lineLocations[i][1]),int(lineLocations[i][2]),int(lineLocations[i][3]),int(lineLocations[i][4])]
                    perminantLineLocations.append(tempArray[:])
            #Code to change player go was here

            # This code finds where the line goes to from or too a dot, and updates that dot's caractoristics []

            for i in range(0,len(perminantLineLocations)):
                for j in range (0,len(dotLocations)):
                    if (perminantLineLocations[i][1] == dotLocations[j][0]) and (perminantLineLocations[i][2] == dotLocations[j][1]):
                        
                        xOne = int(perminantLineLocations[i][1])
                        yOne = int(perminantLineLocations[i][2])

                        xTwo = int(perminantLineLocations[i][3])
                        yTwo = int(perminantLineLocations[i][4])

                        if (yOne == yTwo) and (xTwo > xOne):
                            lineDirection = "Right"
                            dotLocations[j][6][3] = 1
                            dotLocations[j + 1][6][2] = 1
                        elif (yOne == yTwo) and (xOne > xTwo):
                            lineDirection = "Left"
                            dotLocations[j][6][2] = 1
                            dotLocations[j - 1][6][3] = 1
                        elif (xOne == xTwo) and (yOne > yTwo):
                            lineDirection = "Up"
                            dotLocations[j][6][0] = 1
                            dotLocations[j - int(noOfDotsSQ)][6][1] = 1
                        elif (xOne == xTwo) and (yTwo > yOne):
                            lineDirection = "Down"
                            dotLocations[j][6][1] = 1
                            dotLocations[j + int(noOfDotsSQ)][6][0] = 1

            if (playerTurn == 1):
                playerTurn = 2
            else:
                playerTurn = 1
                
            checkForSquares()
            escape("e")
                    
        else: # This is where grey lines are made
            #Gets current selected (red) dot, and then makes it Hard Selected (Yellow)
            for i in range (0,len(dotLocations)):
                if dotLocations[i][2] == "Selected":
                    selectedDotNumber = int(dotLocations[i][3])

            dotLocations[selectedDotNumber][2] = "hardSelected" # Becomes Yellow - is the hard selected dot
            #            selectedDotNumber is the current yellow dot ID

            #Right
            checkRight = False
            for i in range (0,len(dotLocations)):
                if (int(dotLocations[i][3]) == int(selectedDotNumber+1)) and (dotLocations[selectedDotNumber][4] == dotLocations[selectedDotNumber+1][4]):
                    checkRight = True

            if checkRight == True:
                if dotLocations[int(selectedDotNumber + 1)][6][2] == 0:
                    tempArray = ["unconfirmed",int(dotLocations[selectedDotNumber][0]),int(dotLocations[selectedDotNumber][1]),int(dotLocations[selectedDotNumber + 1][0]),int(dotLocations[selectedDotNumber + 1][1])]
                    lineLocations.append(tempArray[:])

            if len(lineLocations) < 1:
                tempArray2 = ["placeholder",0,0,0,0]
                lineLocations.append(tempArray2[:])
            #Down
            checkDown = False
            for i in range (0,len(dotLocations)):
                if int(dotLocations[i][3]) == int(selectedDotNumber + int(noOfDotsSQ)):
                    checkDown = True

            if checkDown == True:
                if dotLocations[int(selectedDotNumber + int(noOfDotsSQ))][6][0] == 0:
                    tempArray = ["unconfirmed",int(dotLocations[selectedDotNumber][0]),int(dotLocations[selectedDotNumber][1]),int(dotLocations[selectedDotNumber + int(noOfDotsSQ)][0]),int(dotLocations[selectedDotNumber + int(noOfDotsSQ)][1])]
                    lineLocations.append(tempArray[:])
                    
            if len(lineLocations) < 2:
                tempArray2 = ["placeholder",0,0,0,0]
                lineLocations.append(tempArray2[:])
            #Left
            checkLeft = False
            for i in range (0,len(dotLocations)):
                if (int(dotLocations[i][3]) == int(selectedDotNumber-1)) and (dotLocations[selectedDotNumber][4] == dotLocations[selectedDotNumber-1][4]):
                    checkLeft = True

            if checkLeft == True:
                if dotLocations[int(selectedDotNumber - 1)][6][3] == 0:
                    tempArray = ["unconfirmed",int(dotLocations[selectedDotNumber][0]),int(dotLocations[selectedDotNumber][1]),int(dotLocations[selectedDotNumber - 1][0]),int(dotLocations[selectedDotNumber - 1][1])]
                    lineLocations.append(tempArray[:])

            if len(lineLocations) < 3:
                tempArray2 = ["placeholder",0,0,0,0]
                lineLocations.append(tempArray2[:])       
            #Up
            checkUp = False
            for i in range (0,len(dotLocations)):
                if int(dotLocations[i][3]) == int(selectedDotNumber-int(noOfDotsSQ)):
                    checkUp = True

            if checkUp == True:
                if dotLocations[int(selectedDotNumber - int(noOfDotsSQ))][6][1] == 0: # Checks if down space is available on dot above
                    tempArray = ["unconfirmed",int(dotLocations[selectedDotNumber][0]),int(dotLocations[selectedDotNumber][1]),int(dotLocations[selectedDotNumber - int(noOfDotsSQ)][0]),int(dotLocations[selectedDotNumber - int(noOfDotsSQ)][1])]
                    lineLocations.append(tempArray[:])

            if len(lineLocations) < 4:
                tempArray2 = ["placeholder",0,0,0,0]
                lineLocations.append(tempArray2[:])
                    
            drawDots()
    
def selectDown(e):
    global dotLocations, greyLines,lineLocations,noOfDotsSQ,startMenuPresent
    if startMenuPresent == False:
        if greyLines == False:
            for i in range (0,len(dotLocations)):
                if (dotLocations[i][2] == "Selected") or (dotLocations[i][2] == "hardSelected"):
                    selectedDotNumber = int(dotLocations[i][3])

            # CHECK IF "selectedDotNumber" + 5  exists in the array, if not, it is presumed that the selected dot is at the bottom, top, left or right
            check = False
            for i in range (0,len(dotLocations)):
                if int(dotLocations[i][3]) == int(selectedDotNumber+noOfDotsSQ):
                    check = True

            if check == True:
                dotLocations[selectedDotNumber][2] = "Not Selected"
                dotLocations[int(selectedDotNumber+noOfDotsSQ)][2] = "Selected"
        else:
            for i in range(0,len(lineLocations)):
                if lineLocations[i][0] == "highlighted":
                    lineLocations[i][0] = "unconfirmed"
            lineLocations[1][0] = "highlighted"
            
        drawDots()

def selectUp(e):
    global dotLocations, greyLines,noOfDotsSQ,startMenuPresent
    if startMenuPresent == False:
        if greyLines == False:
            for i in range (0,len(dotLocations)):
                if (dotLocations[i][2] == "Selected") or (dotLocations[i][2] == "hardSelected"):
                    selectedDotNumber = int(dotLocations[i][3])

            # CHECK IF "selectedDotNumber" - 5  exists in the array, if not, it is presumed that the selected dot is at the bottom, top, left or right
            check = False
            for i in range (0,len(dotLocations)):
                if int(dotLocations[i][3]) == int(selectedDotNumber-noOfDotsSQ):
                    check = True

            if check == True:
                dotLocations[selectedDotNumber][2] = "Not Selected"
                dotLocations[int(selectedDotNumber-noOfDotsSQ)][2] = "Selected"
        else:
            for i in range(0,len(lineLocations)):
                if lineLocations[i][0] == "highlighted":
                    lineLocations[i][0] = "unconfirmed"
            lineLocations[3][0] = "highlighted"        
        drawDots()

def selectRight(e):
    global dotLocations, greyLines,startMenuPresent
    if startMenuPresent == False:
        if greyLines == False:
            for i in range (0,len(dotLocations)):
                if (dotLocations[i][2] == "Selected") or (dotLocations[i][2] == "hardSelected"):
                    selectedDotNumber = int(dotLocations[i][3])

            # CHECK (Works by checking if the selected dot number +1 is in the array. 
            check = False
            for i in range (0,len(dotLocations)):
                if (int(dotLocations[i][3]) == int(selectedDotNumber+1)) and (dotLocations[selectedDotNumber][4] == dotLocations[selectedDotNumber+1][4]):
                    check = True

            if check == True:
                dotLocations[selectedDotNumber][2] = "Not Selected"
                dotLocations[int(selectedDotNumber+1)][2] = "Selected"
        else:
            for i in range(0,len(lineLocations)):
                if lineLocations[i][0] == "highlighted":
                    lineLocations[i][0] = "unconfirmed"
            lineLocations[0][0] = "highlighted"      
        drawDots()

def selectLeft(e):
    global dotLocations, greyLines,startMenuPresent
    if startMenuPresent == False:
        if greyLines == False:
            for i in range (0,len(dotLocations)):
                if (dotLocations[i][2] == "Selected") or (dotLocations[i][2] == "hardSelected"):
                    selectedDotNumber = int(dotLocations[i][3])

            # CHECK 
            check = False
            for i in range (0,len(dotLocations)):
                if (int(dotLocations[i][3]) == int(selectedDotNumber-1)) and (dotLocations[selectedDotNumber][4] == dotLocations[selectedDotNumber-1][4]):
                    check = True

            if check == True:
                dotLocations[selectedDotNumber][2] = "Not Selected"
                dotLocations[int(selectedDotNumber-1)][2] = "Selected"
        else:
            for i in range(0,len(lineLocations)):
                if lineLocations[i][0] == "highlighted":
                    lineLocations[i][0] = "unconfirmed"
            lineLocations[2][0] = "highlighted"            
        drawDots()

window.bind("<Up>",selectUp)
window.bind("<Down>",selectDown)
window.bind("<Right>",selectRight)
window.bind("<Left>",selectLeft)
window.bind("<Return>",enterPressed)
window.bind("w",selectUp)
window.bind("s",selectDown)
window.bind("d",selectRight)
window.bind("a",selectLeft)
window.bind("<space>",enterPressed)
window.bind("<Escape>",escape)

#resetGame("None") #Used to start game
startMenu()
window.mainloop()
