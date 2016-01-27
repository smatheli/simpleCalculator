#!/usr/bin/env python
# -*- coding: utf-8 -*-

# termProject.py

# Sebastien Mathelier, smatheli, M

import math, string, random, os
from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass

class simpleCalculator(EventBasedAnimationClass):
    # Constuctor for Calculator class
    def __init__(self):
        self.width = 1280
        self.height = 640
        super(simpleCalculator, self).__init__(self.width, self.height)
    
    # Initializes the self variables for the class
    def initAnimation(self):
        self.initSidebarVar()
        self.initCalcVar()
        self.initGraphVar()
        self.initHistoryVar()
        self.initThemeVar()
        self.initHelpScreenVar()    
        self.colorTheme = self.readFile("calculatorColor.txt")
                
    # Initializes variables for sidebar
    def initSidebarVar(self):
        self.margin = 20
        self.radius = 52
        self.sideCenX = 72
        self.sideWidth = 144
        self.numOfCircles = 5
        self.diameter = self.radius * 2
        self.sideCenY = [72,196,320,444,568]
    
    # Initializes variables for calculator
    def initCalcVar(self):
        self.calculator = True
        self.restart = False
        self.trig = False
        self.isAnswer = False
        self.highlight = False
        self.outputHeight = 140
        self.cellWidth = (float(1136) / 10)
        self.appearEq = []
        self.calcEq = []
    
    # Initalizes variables for history
    def initHistoryVar(self):
        self.history = False
        self.eqHistory = self.readFile("equationHistory.txt")
        self.resultHistory = self.readFile("resultHistory.txt")

    # Initializes variables for graph
    def initGraphVar(self):
        self.graph = False
        self.evaluate = False
        self.inFunc = False
        self.inXMax = self.inYMax = self.inXStep = self.inYStep = False
        self.cxGraph = 605.5
        self.cyGraph = 280
        self.graphWidth = 923
        self.graphHeight = 560
        self.numOfParam = 4
        self.count = 1
        self.nums = "0123456789"
        self.operators = "()/*-+.^"
        self.function=self.xmax=self.ymax=self.xstep=self.ystep = ""
        self.evalFunc = ""
    
    # Initializes theme variables
    def initThemeVar(self):
        self.theme = False
        self.colorCenY = 320
        self.colorCenX = [480,650.4,820.8,991.8,1161.6]
        self.colors = ["red", "blue", "yellow", "pink", "orange"]

    # Initializes help screen variables
    def initHelpScreenVar(self):
        self.helpScreen = False

    # Checks current section
    def checkCurrentSection(self, x, y):
        (sideCenX, sideCenY) = (self.sideCenX, self.sideCenY)
        (t, f) = (3, 4)

        if (x <= self.sideWidth):
            if (self.distance(x, y, sideCenX, sideCenY[0]) <= self.radius):
                (self.calculator, self.theme) = (True, False)
                self.helpScreen = self.graph = self.history = False
            elif (self.distance(x, y, sideCenX, sideCenY[1]) <= self.radius):
                (self.history, self.theme) = (True, False)
                self.calculator = self.helpScreen = self.graph = False
            elif (self.distance(x, y, sideCenX, sideCenY[2]) <= self.radius):
                (self.graph, self.history) = (True, False)
                self.theme = self.calculator = self.helpScreen = False
            elif (self.distance(x, y, sideCenX, sideCenY[t]) <= self.radius):
                (self.theme, self.helpScreen) = (True, False)
                self.calculator = self.graph = self.history = False
            elif (self.distance(x, y, sideCenX, sideCenY[f]) <= self.radius):
                (self.helpScreen, self.theme) = (True, False)
                self.calculator = self.graph = self.history = False

    # Draws the screen in tkinter window
    def drawScreen(self):
        self.drawSidebar()
        self.drawCalculator()
        self.drawGraph()
        self.drawHistory()
        self.drawTheme()
        self.drawHelpScreen()

################################################################################
############################onMousePressed Methods##############################
################################################################################

    # Acts on calc mouse press
    def onMousePressedCalc(self, x, y):
        self.determineSelectedButton()
        self.createEquation()
        self.highlight = True

    # Acts on graph mouse press
    def onMousePressedGraph(self, x, y):
        (fStartX, fStartY, fEndX, fEndY, t) = (200, 575, 1052, 625, 3)
        pStartX,pEndX,pStartY,pEndY=1082,1265,[79,207,335,463],[113,241,369,497]

        if (fStartX <= x <= fEndX) and (fStartY <= y <= fEndY):
            self.inFunc = True
            self.inXMax = self.inYMax = self.inXStep = self.inYStep = False
        elif (pStartX <= x <= pEndX) and (pStartY[0] <= y <= pEndY[0]):
            self.inXMax = True
            self.inFunc=self.inYMax=self.inXStep=self.inYStep=False
        elif (pStartX <= x <= pEndX) and (pStartY[1] <= y <= pEndY[1]):
            self.inYMax = True
            self.inXMax=self.inFunc=self.inXStep=self.inYStep=False
        elif (pStartX <= x <= pEndX) and (pStartY[2] <= y <= pEndY[2]):
            self.inXStep = True
            self.inXMax=self.inYMax=self.inFunc=self.inYStep=False
        elif (pStartX <= x <= pEndX) and (pStartY[t] <= y <= pEndY[t]):
            self.inYStep = True
            self.inXMax = self.inYMax = self.inXStep = self.inFunc = False
        else:
            self.inXMax=self.inYMax=self.inXStep=self.inYStep=self.inFunc=False

    # Acts on help screen mouse press
    def onMousePressedHelp(self, x, y):
        (colorCenX, colorCenY) = (self.colorCenX, self.colorCenY)
        for cir in xrange(len(self.colors)):
            if (self.distance(x,y,colorCenX[cir],colorCenY)<=self.radius):
                self.colorTheme = self.colors[cir]
                self.writeColor()

    # Acts accordingly to the key pressed by the user
    def onMousePressed(self, event):
        (x, y) = (self.x, self.y) = (event.x, event.y)

        self.checkCurrentSection(x, y)

        if (self.calculator) and (y >= self.outputHeight):
            self.onMousePressedCalc(x, y)

        elif (self.graph):
            self.onMousePressedGraph(x, y)

        elif (self.theme):
            self.onMousePressedHelp(x, y)
            
################################################################################
#############################onKeyPressed Methods###############################
################################################################################

    # Key press for function box
    def onKeyPressedInFunction(self, event):
        if (event.keysym == "BackSpace"):
            self.function = self.function[:len(self.function)-1]
        elif (event.keysym == "Return"):
            self.evaluate = True
        elif ((event.char in string.ascii_lowercase) or 
            (event.char in string.digits)or(event.char in self.operators)):
            self.function += event.char

    # Key Press for xmax box
    def onKeyPressedInXMax(self, event):
        if (event.keysym == "BackSpace"):
            self.xmax = self.xmax[:len(self.xmax)-1]
        elif (event.keysym == "Return"):
            self.evaluate = True
        elif (event.char in string.digits) or (event.char == '.'):
            self.xmax += event.char

    # Key press for ymax box
    def onKeyPressedInYMax(self, event):
        if (event.keysym == "BackSpace"):
            self.ymax = self.ymax[:len(self.ymax)-1]
        elif (event.keysym == "Return"):
            self.evaluate = True
        elif (event.char in string.digits) or (event.char == '.'):
            self.ymax += event.char

    # Key press for xstep box
    def onKeyPressedInXStep(self, event):
        if (event.keysym == "BackSpace"):
            self.xstep = self.xstep[:len(self.xstep)-1]
        elif (event.keysym == "Return"):
            self.evaluate = True
        elif (event.char in string.digits) or (event.char == '.'):
            self.xstep += event.char

    # Key press for ystep box
    def onKeyPressedInYStep(self, event):
        if (event.keysym == "BackSpace"):
            self.ystep = self.ystep[:len(self.ystep)-1]
        elif (event.keysym == "Return"):
            self.evaluate = True
        elif (event.char in string.digits) or (event.char == '.'):
            self.ystep += event.char

    # Takes in key press event
    def onKeyPressed(self, event):
        if (self.graph) and (event.char == "c"):
            self.function=self.xmax=self.ymax=self.xstep=self.ystep = ""
            self.evaluate = False

        elif (self.inFunc) and (self.graph):
            self.onKeyPressedInFunction(event)

        elif (self.inXMax) and (self.graph):
            self.onKeyPressedInXMax(event)

        elif (self.inYMax) and (self.graph):
            self.onKeyPressedInYMax(event)

        elif (self.inXStep) and (self.graph):
            self.onKeyPressedInXStep(event)

        elif (self.inYStep) and (self.graph):
            self.onKeyPressedInYStep(event)

################################################################################
##############################Read/Write Methods################################
################################################################################

    # Reads file method
    def readFile(self, filename, mode="rt"):
        # rt = "read text"
        with open(filename, mode) as fin:
            return fin.read()

    # Write file method
    def writeFile(self, filename, contents, mode="wt"):
        # wt = "write text"
        with open(filename, mode) as fout:
            fout.write(contents)

    # Write equation method
    def writeEquation(self):
        path = "equationHistory.txt"
        self.eqHistory += self.finalAppearEq + ","
        self.writeFile(path, self.eqHistory)

    # Write resul method
    def writeResult(self):
        path = "resultHistory.txt"
        self.resultHistory += self.appearEq[0] + ","
        self.writeFile(path, self.resultHistory)

    # Write color method
    def writeColor(self):
        path = "calculatorColor.txt"
        self.contents = self.colorTheme
        self.writeFile(path, self.contents)

################################################################################
###############################Sidebar Methods##################################
################################################################################
    # Determines distance between two points
    def distance(self, x1, y1, x2, y2):
        sq1 = (x1 - x2)**2
        sq2 = (y1 - y2)**2
        return math.sqrt(sq1 + sq2)

    # Draws text in sidebar
    def drawSidebarText(self):
        x = 72
        y = [72, 196, 320, 444, 568]
        text = ["Calculate", "History", "Graph", "Theme", "?"]

        for c in xrange(self.numOfCircles):
            self.canvas.create_text(x, y[c], text=text[c], fill=self.colorTheme,
                                    font="Helvetica 20")

    # Draws the sidebar seen in window
    def drawSidebar(self):
        sideWidth = self.sideWidth
        height = self.height
        margin = self.margin
        diameter = self.diameter
        width = 3

        self.canvas.create_rectangle(0, 0, sideWidth, height, outline="white",
                                    fill="white")

        for cirNum in xrange(self.numOfCircles):
            (x1, x2) = (margin, (margin + diameter))
            y1  = margin + (x2 * cirNum)
            y2 = y1 + diameter
            self.canvas.create_oval(x1,y1,x2,y2,activefill='gray',
                            outline=self.colorTheme,fill='white',width=width)

        self.drawSidebarText()

################################################################################
############################Calculator Methods##################################
################################################################################
    # Draws the calculator
    def drawCalculator(self):
        if (self.calculator):
            self.drawCalculatorColors()
            self.drawCalculatorLines()
            self.highlightSelectedButton()
            self.drawCalculatorText()
            self.drawCalculatorOutput()

    # Draws the calculator colors
    def drawCalculatorColors(self):
        (width, height, cellWidth) = (self.width, self.height, self.cellWidth)

        self.canvas.create_rectangle(self.sideWidth, 0, width, height,
                                outline=self.colorTheme, fill=self.colorTheme)

        (x1, x2, y1, y2) = (self.sideWidth, width, 0, 140)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")

        (x1, x2, y1, y2) = (self.sideWidth, (6*cellWidth+x1), 140, height)
        self.canvas.create_rectangle(x1, y1, x2, y2,fill="gray")

        (x1, x2, y1, y2) = ((6*cellWidth+144), (9*cellWidth+144), 140, 240)
        self.canvas.create_rectangle(x1, y1, x2, y2,fill="gray")

        (x1, x2, y1, y2) = ((6*cellWidth+144), (9*cellWidth+144), 240, height)
        self.canvas.create_rectangle(x1, y1, x2, y2,fill="light gray")

    # Draws the calculator lines
    def drawCalculatorLines(self):
        (width, height, cellWidth) = (self.width, self.height, self.cellWidth)
        (numOfHor, numOfVert) = (6, 10)

        (x1, x2, y) = (self.sideWidth, width, 140)
        for hor in xrange(numOfHor):
            self.canvas.create_line(x1, y, x2, y, fill="dark gray")
            y += 100

        (x, y1, y2) = (self.sideWidth, 140, height)
        for vert in xrange(numOfVert):
            self.canvas.create_line(x, y1, x, y2, fill="dark gray")
            x += cellWidth

        (x, y1, y2) = ((7*cellWidth+144), (height-100), height)
        self.canvas.create_line(x,y1,x,y2, fill="light grey")

    # Highlights the selected calc button
    def highlightSelectedButton(self):
        zeroRow = 4
        zeroCol = [6, 7]

        if (self.highlight):
            if (self.rowNum == zeroRow) and (self.colNum == zeroCol[0]):
                right = self.right + self.cellWidth
                self.canvas.create_rectangle(self.left, self.top, right, 
                    self.bottom,fill="dark grey",outline="dark grey")
            elif (self.rowNum == zeroRow) and (self.colNum == zeroCol[1]):
                left = self.left - self.cellWidth
                self.canvas.create_rectangle(left, self.top, self.right, 
                    self.bottom,fill="dark grey",outline="dark grey")
            else:
                self.canvas.create_rectangle(self.left, self.top, self.right, 
                    self.bottom,fill="dark grey",outline="dark grey")

        self.highlight = False

    # Draws the calc text
    def drawCalculatorText(self):
        centerY = 190
        self.symbols = [['(',')','mc','m+','m-','mr','C','Bksp','%','/'],
            ['Rand','x²','x³','x^y','e^x','10^x','7','8','9','*'],
            ['1/x','√x','³√x','y^(1/x)','ln','log₁₀','4','5','6','-'],
            ['x!','e','sin','cos','tan','π','1','2','3','+'],
            ['Solve','x','sinh','cosh','tanh','','0','','.','=']]

        for x in xrange(len(self.symbols)):
            centerX = self.sideWidth + (self.cellWidth/2)
            for y in xrange(len(self.symbols[0])):
                self.canvas.create_text(centerX,centerY,text=self.symbols[x][y],
                                        font="Helvetica 28")
                centerX += self.cellWidth
            centerY += 100

    # Draws the calc output
    def drawCalculatorOutput(self):
        text = ''.join(self.appearEq)
        text = text.strip()
        textLimit = 20
        if len(text) > textLimit: text = text[(len(text)-textLimit):len(text)]

        (x, y) = (1270, 70)
        self.canvas.create_text(x, y, text=text, anchor=E, 
                                fill="white", font="Helvetica 100")

    # Determines the slected button in the calc
    def determineSelectedButton(self):
        self.left = self.right = self.top = self.bottom = 0
        self.colNum = self.rowNum = -1
        sideWidth = self.sideWidth
        (rows, cols) = (5, 10)
        # Determines col number in which user clicked
        for vert in xrange(cols):
            leftX = sideWidth + (self.cellWidth * vert)
            rightX = leftX + self.cellWidth
            if leftX < self.x and rightX > self.x:
                self.colNum = vert
                self.left = leftX
                self.right = rightX
                break
        # Determines row number in which user clicked
        for hor in xrange(rows):
            topY = 140 + (100 * hor)
            bottY = topY + 100
            if topY < self.y and bottY > self.y:
                self.rowNum = hor
                self.top = topY
                self.bottom = bottY
                break

    # Clears equation
    def clearEquation(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append("0")
        self.calcEq.append("0")

    # Accounts for number inputs
    def inputNum(self, row, col):
        symbols = self.symbols
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append(symbols[row][col])
        self.calcEq.append(symbols[row][col])
        self.isAnswer = False

    # Accounts for operator
    def inputOperator(self, row, col):
        symbols = self.symbols
        if (symbols[row][col] == ")") and (self.trig):
            self.appearEq.append(")")
            self.calcEq.append("))")
            self.trig = False
            self.isAnswer = False
        else:
            self.appearEq.append(symbols[row][col])
            self.calcEq.append(symbols[row][col])
            self.restart = False
            self.isAnswer = False

    # Accounts for equal
    def inputEqual(self):
        self.finalAppearEq = ''.join(self.appearEq)
        finalCalcEq = "1.0*" + ''.join(self.calcEq)
        try:
            if (round(eval(finalCalcEq)) == eval(finalCalcEq)):
                if "e" in str(eval(finalCalcEq)):
                    self.appearEq = [str(eval(finalCalcEq))]
                else: self.appearEq = [str(int(eval(finalCalcEq)))]
            else: self.appearEq = [str(eval(finalCalcEq))]

            self.isAnswer = True
            self.calcEq = [str(eval(finalCalcEq))]
            self.writeEquation()
            self.writeResult()
        except: self.appearEq = "ERROR"
        self.restart = True

    # Accounts for clear
    def inputClear(self):
        self.appearEq = []
        self.calcEq = []
        self.trig = False
        self.isAnswer = False

    # Accounts for backspace
    def inputBksp(self):
        self.appearEq = self.appearEq[:len(self.appearEq)-1]
        self.calcEq = self.calcEq[:len(self.calcEq)-1]
        self.isAnswer = False

    # Accounts for random
    def inputRand(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        randNum = random.random()
        self.appearEq.append(str(randNum))
        self.calcEq.append(str(randNum))
        self.isAnswer = False   

    # Accounts for decimal
    def inputDecimal(self):
        if (len(self.calcEq) == 0):
            self.appearEq.append("0.")
            self.calcEq.append("0.")
            self.isAnswer = False
        else:
            self.appearEq.append(".")
            self.calcEq.append(".")
            self.isAnswer = False

    # Accounts for e
    def inputE(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append("e")
        self.calcEq.append("math.e")
        self.isAnswer = False

    # Accounts for pi
    def inputPi(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append("π")
        self.calcEq.append("math.pi")
        self.isAnswer = False

    # Accounts for sin
    def inputSin(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append("sin(")
        self.calcEq.append("math.sin(math.radians(")
        self.trig = True
        self.isAnswer = False

    # Accounts for cas
    def inputCos(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append("cos(")
        self.calcEq.append("math.cos(math.radians(")
        self.trig = True
        self.isAnswer = False

    # Accounts for tan
    def inputTan(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append("tan(")
        self.calcEq.append("math.tan(math.radians(")
        self.trig = True
        self.isAnswer = False

    # Accounts for sinh
    def inputSinh(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append("sinh(")
        self.calcEq.append("math.sinh(")
        self.isAnswer = False

    # Accounts for cosh
    def inputCosh(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append("cosh(")
        self.calcEq.append("math.cosh(")
        self.isAnswer = False

    # Accounts for tanh
    def inputTanh(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append("tanh(")
        self.calcEq.append("math.tanh(")
        self.isAnswer = False

    # Accounts for square
    def inputSquare(self):
        self.appearEq.append("²")
        self.calcEq.append("**2")
        self.isAnswer = False

    # Accounts for cube
    def inputCube(self):
        self.appearEq.append("³")
        self.calcEq.append("**3")
        self.isAnswer = False

    # Accounts for power
    def inputPower(self):
        self.appearEq.append("^")
        self.calcEq.append("**")
        self.restart = False
        self.isAnswer = False

    # Accounts for e to the power
    def inputEPower(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append("e^")
        self.calcEq.append("math.e**")
        self.isAnswer = False

    # Accounts for 10 to the power
    def inputTenPower(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append("10^")
        self.calcEq.append("10**")
        self.isAnswer = False

    # Accounts for reciprical
    def inputReciprical(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append("(1/")
        self.calcEq.append("(float(1)/")
        self.isAnswer = False

    # Accounts for square root
    def inputSquareRoot(self):
        self.appearEq.append("^(1/2)")
        self.calcEq.append("**(float(1)/2)")
        self.isAnswer = False

    # Accounts for cube root
    def inputCubeRoot(self):
        self.appearEq.append("^(1/3)")
        self.calcEq.append("**(float(1)/3)")
        self.isAnswer = False

    # Accounts for nth root
    def inputRoot(self):
        self.appearEq.append("^(1/")
        self.calcEq.append("**(float(1)/")
        self.isAnswer = False

    # Accounts for natural log
    def inputNaturalLog(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append("ln(")
        self.calcEq.append("math.log(")
        self.isAnswer = False

    # Accounts for log
    def inputLog(self):
        if (self.restart):
            self.appearEq = []
            self.calcEq = []
            self.restart = False
        self.appearEq.append("log(")
        self.calcEq.append("math.log10(")
        self.isAnswer = False

    # Create the equation to be evaluated
    def createEquation(self):
        (row, col, eqRow, eqCol) = (self.rowNum, self.colNum, 4, 7)
        symbols = self.symbols
        nums = "0123456789"
        operators = "()/*-+"
        isNum = True

        if (row == eqRow) and (col == eqCol): self.clearEquation()
        elif ((row == -1) or (col == -1)) or (symbols[row][col] == ''): pass
        elif (symbols[row][col] in nums): self.inputNum(row, col)
        elif (symbols[row][col] in operators): self.inputOperator(row, col)
        elif (symbols[row][col] == "="): self.inputEqual()
        elif (symbols[row][col] == "C"): self.inputClear()
        elif (symbols[row][col] == "Bksp"): self.inputBksp()
        elif (symbols[row][col] == "Rand"): self.inputRand()
        elif (symbols[row][col] == "."): self.inputDecimal()
        elif (symbols[row][col] == "e"): self.inputE()
        elif (symbols[row][col] == "π"): self.inputPi()
        elif (symbols[row][col] == "sin"): self.inputSin()
        elif (symbols[row][col] == "cos"): self.inputCos()
        elif (symbols[row][col] == "tan"): self.inputTan()
        elif (symbols[row][col] == "sinh"): self.inputSinh()
        elif (symbols[row][col] == "cosh"): self.inputCosh()
        elif (symbols[row][col] == "tanh"): self.inputTanh()
        elif (symbols[row][col] == "x²"): self.inputSquare()
        elif (symbols[row][col] == "x³"): self.inputCube()
        elif (symbols[row][col] == "x^y"): self.inputPower()
        elif (symbols[row][col] == "e^x"): self.inputEPower()
        elif (symbols[row][col] == "10^x"): self.inputTenPower()
        elif (symbols[row][col] == "1/x"): self.inputReciprical()
        elif (symbols[row][col] == "√x"): self.inputSquareRoot()
        elif (symbols[row][col] == "³√x"): self.inputCubeRoot()
        elif (symbols[row][col] == "y^(1/x)"): self.inputRoot()
        elif (symbols[row][col] == "ln"): self.inputNaturalLog()
        elif (symbols[row][col] == "log₁₀"): self.inputLog()
        elif (symbols[row][col] == "%"):
            numList = nums + "."

            finalCalcEq = ''.join(self.calcEq)
            for string in xrange(len(self.calcEq)):
                if (self.calcEq[string] not in numList):
                    isNum = False
                    break

            if (isNum) or ((self.isAnswer) and (finalCalcEq != "ERROR")):
                finalCalcEq = "(" + finalCalcEq + ")/float(100)"
                self.appearEq = [str(eval(finalCalcEq))]
                self.calcEq = [str(eval(finalCalcEq))]
                self.isAnswer = True
            else: pass

################################################################################
################################Graph Methods###################################
################################################################################

    # Draws the graoh input boxes
    def drawInputBoxes(self):
        text = ["x-max:", "y-max:", "x-step:", "y-step:"]
        
        self.canvas.create_line(self.cxGraph,0,self.cxGraph,self.graphHeight)
        (x1, x2, y) = (self.sideWidth, 1067, self.cyGraph)
        self.canvas.create_line(x1,y,x2,y)

        (x1, x2, y2) = (self.sideWidth, self.width, self.height)
        self.canvas.create_rectangle(x1,0,x2,y2,outline="dark grey",width=2)

        (x1, x2, y2) = (self.sideWidth, self.width, self.graphHeight)
        self.canvas.create_rectangle(x1,0,x2,y2,outline="dark grey",width=2)

        (x1, x2, y2) = (self.width-213, self.width, self.graphHeight)
        self.canvas.create_rectangle(x1,0,x2,y2,outline="dark grey",width=2)

        (x1, y1, x2, y2) = (200, self.graphHeight+15, 1052, self.graphHeight+65)
        self.canvas.create_rectangle(x1,y1,x2,y2,outline="dark grey")

        (x, y) = (178, 600)
        self.canvas.create_text(x, y, text="f(x)=", font="Helvetica 18")

        for box in xrange(self.numOfParam):
            (x, y) = (1082, 56 + (box * 128))
            self.canvas.create_text(x,y,text=text[box],anchor=W,
                                    font="Helvetica 18")

            (x1, y1, x2, y2) = (1082, 79 + (box * 128), 1265, 113 + (box * 128))
            self.canvas.create_rectangle(x1, y1, x2, y2,outline="dark grey")

    # Highlights selected input box
    def highlightSelectedInput(self):
        (fStartX, fStartY, fEndX, fEndY) = (200, 575, 1052, 625)
        (pStartX, pEndX, t, width) = (1082, 1265, 3, 3)
        pStartY = [79, 207, 335, 463]
        pEndY = [113, 241, 369, 497]

        if (self.inFunc):
            self.canvas.create_rectangle(fStartX,fStartY,fEndX,fEndY,
                                        outline="dark grey", width=width)
        elif (self.inXMax):
            self.canvas.create_rectangle(pStartX, pStartY[0], pEndX, pEndY[0],
                                        outline="dark grey", width=width)
        elif (self.inYMax):
            self.canvas.create_rectangle(pStartX, pStartY[1], pEndX, pEndY[1],
                                        outline="dark grey", width=width)
        elif (self.inXStep):
            self.canvas.create_rectangle(pStartX, pStartY[2], pEndX, pEndY[2],
                                        outline="dark grey", width=width)
        elif (self.inYStep):
            self.canvas.create_rectangle(pStartX, pStartY[t], pEndX, pEndY[t],
                                        outline="dark grey", width=width)

    # Draws the input from the user key press
    def drawInput(self):
        (x, y) = (220, 600)
        (text, fnLen) = (self.function, 81)
        if len(text) > fnLen: text = text[(len(text)-fnLen):len(text)]
        self.canvas.create_text(x, y, text=text, anchor=W, font="Helvetica 18")

        (x, y1, space) = (1096, 96, 128)
        (text, pLen) = ([self.xmax, self.ymax, self.xstep, self.ystep], 19)
        for p in xrange(self.numOfParam):
            if len(text) > pLen: text[p] = text[p][(len(text)-pLen):len(text)]
            self.canvas.create_text(x, y1+space*p, text=text[p], anchor=W,
                                    font="Helvetica 16")

    # Fixes equation
    def fixEquation(self, loc, exp):
        left = self.evalFunc[loc-5:loc]
        (l, s, e) = (4, 5, 3)

        if (loc != -1) and (exp == "pi") and (left != "math."):
            self.evalFunc = self.evalFunc[:loc] + "math." + self.evalFunc[loc:]
            self.count += 1
        elif (loc != -1) and (exp == "trig") and (left != "math."):
            locClosed = self.evalFunc.find(")")
            self.evalFunc=(self.evalFunc[:loc]+"math."+self.evalFunc[loc:loc+l]+
                           "math.radians("+self.evalFunc[loc+l:locClosed]+"))")
            self.count += 1
        elif (loc != -1) and (exp == "trigh") and (left != "math."):
            locClosed = self.evalFunc.find(")")
            self.evalFunc=(self.evalFunc[:loc]+"math."+self.evalFunc[loc:loc+s]+
                           "math.radians("+self.evalFunc[loc+s:locClosed]+"))")
            self.count += 1
        elif (loc != -1) and (exp == "ln") and (left != "math."):
            self.evalFunc = self.evalFunc[:loc]+"math.log"+self.evalFunc[loc+2:]
            self.count += 1
        elif (loc != -1) and (exp == "log") and (left != "math."):
            self.evalFunc=self.evalFunc[:loc]+"math.log10"+self.evalFunc[loc+e:]
            self.count += 1
        elif (loc != -1) and (exp == "exponent") and (left != "math."):
            self.evalFunc = self.evalFunc[:loc]+"**"+self.evalFunc[loc+1:]
            self.count += 1
        elif (loc != -1) and (exp == "symbol"):
            self.evalFunc = self.evalFunc[:loc]+"math.pi"+self.evalFunc[loc+2:]
            self.count += 1
        elif (loc != -1) and (exp == "cube"):
            self.evalFunc = self.evalFunc[:loc]+"**3"+self.evalFunc[loc+2:]
            self.count += 1
        elif (loc != -1) and (exp == "square"):
            self.evalFunc = self.evalFunc[:loc]+"**2"+self.evalFunc[loc+2:]
            self.count += 1  
        elif ((loc != -1) and (exp == "e") and (left != "math.")):
            self.evalFunc = self.evalFunc[:loc] + "math." + self.evalFunc[loc:]
            self.count += 1

    # Converts fuction into pythin language equation
    def convertFunction(self):
        self.count = 1
        while (self.count > 0):
            self.count = 0
            self.fixEquation(self.evalFunc.find("sinh"), "trigh")
            self.fixEquation(self.evalFunc.find("cosh"), "trigh")
            self.fixEquation(self.evalFunc.find("tanh"), "trigh")
            self.fixEquation(self.evalFunc.find("sin"), "trig")
            self.fixEquation(self.evalFunc.find("cos"), "trig")
            self.fixEquation(self.evalFunc.find("tan"), "trig")
            self.fixEquation(self.evalFunc.find("e"), "e")
            self.fixEquation(self.evalFunc.find("pi"), "pi")
            self.fixEquation(self.evalFunc.find("ln"), "ln")
            self.fixEquation(self.evalFunc.find("log"), "log")
            self.fixEquation(self.evalFunc.find("^"), "exponent")
            self.fixEquation(self.evalFunc.find("³"), "cube")
            self.fixEquation(self.evalFunc.find("²"), "square")
            self.fixEquation(self.evalFunc.find("π"), "symbol")

    # Evaluates the graph to be shown
    def evaluateGraph(self):
        if ((self.function != "") and (self.xmax != "") and (self.ymax != "")
            and (self.xstep != "") and (self.ystep != "")):
            self.evalFunc = self.function
            self.convertFunction()
            
            self.createGraph(self.evalFunc,int(self.xmax),int(self.xstep),
                            int(self.ymax),int(self.ystep))

    # Creates the graph axis
    def createAxis(self, xmax, xstep, ymax, ystep, winWidth, winHeight):
        (cx, cy) = (605.5, 280)
        (hashLen, textDis) = (10, 20)
        self.canvas.create_line(self.sideWidth, cy, winWidth+self.sideWidth, cy)
        self.canvas.create_line(cx, 0, cx, winHeight)

        xHashNum = ((xmax / xstep) * 2) - 1
        xHashSpace = winWidth / ((float(xmax) / xstep) * 2)

        for vert in xrange(1, xHashNum+1):
            x = self.sideWidth + (vert * xHashSpace)
            value = (xmax * -1) + (xstep * vert)
            value = str(value)
            self.canvas.create_line(x,cy-hashLen,x,cy+hashLen)
            self.canvas.create_text(x,cy+textDis,text=value,font="Helvetica 10")

        yHashNum = ((ymax / ystep) * 2) - 1
        self.yHashSpace = yHashSpace = winHeight / ((float(ymax) / ystep) * 2)

        for hor in xrange(1, yHashNum+1):
            y = hor * yHashSpace
            value = ymax + (ystep * hor * -1)
            self.canvas.create_line(cx-hashLen,y,cx+hashLen,y)
            self.canvas.create_text(cx-textDis,y,text=value,font="Helvetica 10")

    # Creates the function for the graph
    def createFunction(self, fn, xmax, ystep, winWidth, winHeight):
        (cx, cy, graphWidth, screenx) = (605.5, 280, xmax*2, 0)
        (graphStepX, oldX, oldY) = (float(graphWidth)/winWidth, None, None)

        for pixel in xrange(self.sideWidth, winWidth+self.sideWidth):
            try:
                x = screenx - xmax
                if ("x" in fn):
                    loc = fn.find("x")
                    if (fn[loc-1]in"0123456789") and (fn[loc-1]!=fn[len(fn)-1]):
                        function = fn[:loc] + "*" + str(x) + fn[loc+1:]
                    else: function = fn[:loc] + "("+str(x)+")" + fn[loc+1:]
                else: function = fn

                y = eval(function) * self.yHashSpace / ystep
                screeny = cy - y
                if ((oldX != None) and (oldY <= winHeight) and 
                    (screeny<=winHeight)):
                    self.canvas.create_line(oldX,oldY,pixel,screeny,
                                        fill=self.colorTheme)
                (oldX, oldY) = (pixel,screeny)
                screenx += graphStepX
            except: pass

    # Creates the function for the log graph
    def createLogFunction(self, fn, xmax, ystep, winWidth, winHeight):
        (cx, cy, graphWidth, screenx) = (605.5, 280, xmax*2, 0)
        (graphStepX, oldX, oldY) = (float(graphWidth)/winWidth, None, None)

        for pixel in xrange(self.sideWidth, winWidth+self.sideWidth):
            try:
                x = screenx - xmax
                if (x >= 0):
                    if ("x" in fn):
                        loc = fn.find("x")
                        if (fn[loc-1] in "0123456789"):
                            function = fn[:loc] + "*" + str(x) + fn[loc+1:]
                        else: function = fn[:loc] + "("+str(x)+")" + fn[loc+1:]
                    else: function = fn

                    y = eval(function) * self.yHashSpace / ystep
                    screeny = cy - y
                    if ((oldX!=None) and (oldY<=winHeight) and 
                        (screeny<=winHeight)):
                        self.canvas.create_line(oldX,oldY,pixel,screeny,
                                            fill=self.colorTheme)
                    (oldX, oldY) = (pixel,screeny)
                screenx += graphStepX
            except: pass

    # Creates the appropriate grapgh
    def createGraph(self,fn,xmax,xstep,ymax,ystep,winWidth=923,winHeight=560):
        self.createAxis(xmax, xstep, ymax, ystep, winWidth, winHeight)

        if ("log" in fn):
            self.createLogFunction(fn, xmax, ystep, winWidth, winHeight)
        else: self.createFunction(fn, xmax, ystep, winWidth, winHeight)

    # Draws the graph main screen
    def drawGraph(self):
        if (self.graph):
            self.drawInputBoxes()
            self.highlightSelectedInput()
            self.drawInput()
            if (self.evaluate):
                self.evaluateGraph()

################################################################################
###############################History Methods##################################
################################################################################
    
    # Draws the equations in the history
    def drawEquations(self, equations, results):
        (x1, y1, x2, y2) = (712, self.outputHeight, 712, self.height)
        (colSize, historySize) = (5, 10)
        self.canvas.create_line(x1, y1, x2, y2, fill = "dark gray")

        for left in xrange(colSize):
            try:
                final = equations[left] + " = " + results[left]
                (x, y) = (428, 190+(left * 100))
                self.canvas.create_text(x,y,text=final,font="Helvetica 28")
            except: pass

        for right in xrange(colSize,historySize):
            try:
                final = equations[right] + " = " + results[right]
                (x, y) = (996, 190+((right-5) * 100))
                self.canvas.create_text(x,y,text=final,font="Helvetica 28")
            except: pass

        self.drawCalculatorOutput()

    # Draws the history main screen
    def drawHistory(self):
        if (self.history):
            (sideWidth, numOfHor, lim) = (self.sideWidth, 5, 10)
            self.canvas.create_rectangle(sideWidth, 0, self.width, self.height,
                                        fill="grey", outline="gray")

            equations = self.eqHistory.split(',')
            equations = equations[:len(equations)-1]
            if (len(equations)>lim): equations = equations[len(equations)-lim:]

            results = self.resultHistory.split(',')
            results = results[:len(results)-1]
            if (len(results) > lim): results = results[len(results)-lim:]

            (x1, x2, y1, y2) = (self.sideWidth, self.width, 0, 140)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")

            (x1, x2, y) = (self.sideWidth, self.width, 140)
            for hor in xrange(numOfHor):
                self.canvas.create_line(x1, y, x2, y, fill="dark gray")
                y += 100

            self.drawEquations(equations, results)

################################################################################
#################################Theme Methods##################################
################################################################################
    
    # Draws the theme main screen
    def drawTheme(self):
        if (self.theme):
            width = 3
            sideWidth = self.sideWidth
            (space, margin, radius) = (66.4, self.margin, self.diameter/2)

            self.canvas.create_rectangle(sideWidth, 0, self.width, self.height,
                                        fill="grey", outline="gray")

            (x, y) = (290, 320)
            self.canvas.create_text(x, y, text="Color Themes:",
                                    fill="black", font="Helvetica 30")

            for cirNum in xrange(self.numOfCircles):
                (y1, y2) = (y - radius, y + radius)
                x1 = 428 + ((space + self.diameter) * cirNum)
                x2 = x1 + self.diameter
                self.canvas.create_oval(x1,y1,x2,y2,outline="black",
                    fill=self.colors[cirNum],activeoutline="white",width=width)

################################################################################
############################Help Screen Methods#################################
################################################################################
    # Creates the text of the help screen
    def createHelpScreenText(self):
        self.helpScreenText = "Sidebar:\n\
    - Left click any button to enter its respective location\n\nCalculator:\n\
    - Left click on any of the calculator buttons to input its value\n\
    - When you're ready to evaluate your equation hit the '-' button\n\
    - Your evaluated equation will replace your actual equation in the \
output bar\n\
    - When the term 'ERROR' appears in the output bar it means the equation\n\
      you evaluated was incorrectly written out\n\nHistory:\n\
    - The calculator button pad is replaced by a grid holding the last 10\n\
    - evaluated equations and their results\n\nGraph:\n\
    - Left click on the textbar under the graph to begin entering a function\n\
    - Left click and enter in values in the textbars on the right for the \
maximum x and y values\n\
      and the step for each hash on the x and y axes\n\
    - Hit the 'Enter/Return' key to see your function graphed only after all \
textbars have been filled\n\
    - Hit the 'c' key to clear all inputs in the textbars and input a new \
graph function\n\nTheme:\n\
    - Left click on any of the five colored circles to change the color \
scheme throughout the calculator"

    # Draws the help screen main screen
    def drawHelpScreen(self):
        if (self.helpScreen):
            sideWidth = self.sideWidth
            self.canvas.create_rectangle(sideWidth, 0, self.width, self.height,
                                        fill="grey", outline="gray")

            self.createHelpScreenText()
            text = self.helpScreenText
            
            (x, y) = (712, 50)
            self.canvas.create_text(x,y,text="Help Screen",font="Helvetica 35")
            y = self.height / 2 + 35
            self.canvas.create_text(x,y,text=text,font="Helvetica 19")

    # Redraws the screen
    def redrawAll(self):
        self.canvas.delete(ALL)
        self.drawScreen()

def runSimpleCalculator():
    calc = simpleCalculator()
    calc.run()

runSimpleCalculator()