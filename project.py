class HanjieMatrix:  # A class that stores an answer to user's puzzle.
    _matrixWidth = 0
    _matrixHeight = 0
    _matrix = []

    def __init__(self, matrixWidth, matrixHeight, matrix):  # When initializing 3 parameters need to be provided.
        self._matrixHeight = matrixHeight  # These are matrixHeight - stores matrix's height
        self._matrixWidth = matrixWidth  # matrixWidth - stores matrix's width
        self._matrix = matrix  # matrix - stores matrix itself

    def getWidth(self):  # A method to get matrix width value
        return self._matrixWidth

    def getHeight(self):  # A method to get matrix height value
        return self._matrixHeight

    def getMatrix(self):  # A method to get the matrix itself
        return self._matrix

    def getMatrixRow(self, row):  # A method returning matrix row
        return self._matrix[row]

    def getMatrixColumn(self, column):  # A method returning matrix column
        matrixColumn = []
        for row in range(self._matrixHeight):
            matrixColumn.append(self._matrix[row][column])
        return matrixColumn

    def initializeFreeMatrix(self):  # initializes a starting matrix full of 0s

        for columns in range(self._matrixHeight):
            line = []
            for rows in range(self._matrixWidth):
                line.append(0)
            self._matrix.append(line)

    def updateMatrix(self, row, column,
                     newPattern):  # A method standing for updating the matrix. Parameters need to be provided are:
        # row - particular row that should be updated(-1 means a column is getting updated), column -
        # particular column that should be updated(-1 means a row is getting updated)
        if row != -1:
            for i in range(len(newPattern)):
                if self._matrix[row][i] == 0:
                    self._matrix[row][i] = newPattern[i]
        else:
            for i in range(len(newPattern)):
                if self._matrix[i][column] == 0:
                    self._matrix[i][column] = newPattern[i]

    def outputMatrix(self):  # function to output matrix in console for user
        for i in range(self._matrixHeight):
            for j in range(self._matrixWidth):
                if self._matrix[i][j] == 1:  # in case box is a block it outputs a green square
                    print('🟩', end="")
                elif self._matrix[i][j] == -1:  # in case box is a space it outputs a blue square
                    print('🟦', end="")
                else:
                    print('🟥', end="")  # in case box is not defined yet, it outputs a red square
            print()


class TopClues:  # A class that stores clues from the top of a puzzle
    _topClues = []

    def __init__(self, numbers):  # Initialization requires a 2-d array with clues to be provided
        self._topClues = numbers

    def getClues(self):  # Returns the whole topClues array
        return self._topClues

    def getCluesByIndex(self, index):  # A getter returning an exact column's clues
        return self._topClues[index]

    def getSumOfCluesInAColumnByIndex(self, index):  # This method returns sum of clues for particular column
        sumOfClues = 0
        for elem in self._topClues[index]:
            if elem > 0:
                sumOfClues += elem + 1  # it adds 1 to length for each clue, because there
                # should be at least one space between clues
        return sumOfClues - 1

    def getSize(self):  # This method returns amount of set of clues for each column
        return len(self._topClues)


class SideClues:  # A class that stores clues from a side of a puzzle
    _sideClues = []

    def __init__(self, numbers):  # Initialization requires a 2-d array with clues to be provided
        self._sideClues = numbers

    def getClues(self):  # Returns the whole sideClues array
        return self._sideClues

    def getCluesByIndex(self, index):  # A getter returning an exact row's clues
        return self._sideClues[index]

    def getSumOfCluesInARowByIndex(self, index):  # This method returns sum of clues for particular row
        sumOfClues = 0
        for elem in self._sideClues[index]:
            if elem > 0:
                sumOfClues += elem + 1  # it adds 1 to length for each clue, because there
                # should be at least one space between clues,
        return sumOfClues - 1

    def getSize(self):  # This method returns amount of set of clues for each row
        return len(self._sideClues)


def askUserForTopClues():  # this function is used to collect clues for columns from console
    topClues_ = []

    columnClueUserInput = input(  # guidance for user what to do
        "Type in top clues column by column, when you finish input 'STOP', start with a clue for the first column:\n")

    while columnClueUserInput.upper() != "STOP":  # user inputs clues column by column and types "STOP" in the end
        try:
            columnClue = list(map(int, columnClueUserInput.split()))

            if not columnClue:  # if user's input is blank, 0 wil be added as a clue
                topClues_.append([0])
            else:
                topClues_.append(columnClue)

            print("Type a clue for the next column:")
        except ValueError:  # in case not integers were inputted, it will ask to retype clues for a column
            print("You are not typing it right, try again")

        columnClueUserInput = input()  # asks to input clues for the next column

    return topClues_


def askUserForSideClues():  # this function is used to collect clues for rows from console
    sideClues_ = []

    rowClueUserInput = input(  # guidance for user what to do
        "Type in side clues row by row, when you finish input 'STOP', start with a clue for the first row:\n")

    while rowClueUserInput.upper() != "STOP":  # user inputs clues row by row and types "STOP" in the end

        try:
            rowClue = list(map(int, rowClueUserInput.split()))

            if not rowClue:  # if user's input is blank, 0 wil be added as a clue
                sideClues_.append([0])
            else:
                sideClues_.append(rowClue)

            print("Type a clue for the next row:")
        except ValueError:  # in case not integers were inputted, it will ask to retype clues for a row
            print("You are not typing it right, try again")

        rowClueUserInput = input()  # asks to input clues for the next row

    return sideClues_


def fullRow(hanjieMatrix, sideClues):  # this solution technique fills rows
    # where length of clues fits matrix width exactly or where row is blank(no clues)
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for row in range(matrixHeight):
        finalRow = []  # variable that stores all changes that happen to a row under this technique
        if sideClues.getSumOfCluesInARowByIndex(row) == matrixWidth:
            for clue in range(len(sideClues.getCluesByIndex(row))):
                if clue != 0:
                    finalRow += [-1]
                finalRow += sideClues.getCluesByIndex(row)[clue] * [1]

            hanjieMatrix.updateMatrix(row, -1, finalRow)  # updates hanjieMatrix's row

        if sideClues.getSumOfCluesInARowByIndex(row) == 0:
            finalRow = [-1] * matrixWidth

            hanjieMatrix.updateMatrix(row, -1, finalRow)  # updates hanjieMatrix's row


def fullColumn(hanjieMatrix, topClues):  # does absolutely same thing as fullRow but to columns now

    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for column in range(matrixWidth):
        finalColumn = []  # variable that stores all changes that happen to a column under this technique
        if topClues.getSumOfCluesInAColumnByIndex(column) == matrixHeight:
            for clue in range(len(topClues.getCluesByIndex(column))):
                if clue != 0:
                    finalColumn += [-1]
                finalColumn += topClues.getCluesByIndex(column)[clue] * [1]

            hanjieMatrix.updateMatrix(-1, column, finalColumn)  # updates hanjieMatrix' column

        if sum(topClues.getCluesByIndex(column)) == 0:
            finalColumn = [-1] * matrixHeight
            hanjieMatrix.updateMatrix(-1, column, finalColumn)  # updates hanjieMatrix' column


def simpleBoxesOnRows(hanjieMatrix, sideClues):  # Simple Boxes technique coded
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for row in range(matrixHeight):

        boxesToTheLeft = []  # this array will be filled considering squeezing all clues to the left side of the row
        boxesToTheRight = []  # this array will be filled considering squeezing all clues to the right side of the row

        finalRow = [0] * matrixWidth  # finalRow set to by full of 0s and if any blocks determined, it will be
        # changed to 1
        clues = sideClues.getCluesByIndex(row)  # clues for particular row imported from SideClues

        for clue in range(len(clues)):  # fill both boxesToTheLeft and boxesToTheRight
            if clue != 0:
                boxesToTheLeft += [0]
            boxesToTheLeft += clues[clue] * [1]

        boxesToTheRight = [0] * (matrixWidth - len(boxesToTheLeft)) + boxesToTheLeft
        boxesToTheLeft += [0] * (matrixWidth - len(boxesToTheLeft))

        spacesMet = 0
        anyBlocksMet = False

        for i in range(matrixWidth):  # if a box is 1 in both boxesToTheLeft and boxesToTheRight, then it is
            # definitely a box
            if boxesToTheLeft[i] == 0:
                spacesMet += 1

            if boxesToTheRight[i] == 1:
                anyBlocksMet = True

            if boxesToTheRight[i] == 0 and anyBlocksMet:
                spacesMet -= 1

            if boxesToTheRight[i] == 1 and boxesToTheLeft[i] == 1 and \
                    matrixWidth / sideClues.getSumOfCluesInARowByIndex(
                row) < 2.0 and spacesMet == 0:
                finalRow[i] = 1

        hanjieMatrix.updateMatrix(row, -1, finalRow)  # updates hanjieMatrix's row


def simpleBoxesOnColumns(hanjieMatrix, topClues):  # Simple boxes for columns
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for column in range(matrixWidth):

        boxesToTheTop = []  # this array will be filled considering squeezing all clues to top of the column
        boxesToTheBottom = []  # this array will be filled considering squeezing all clues to bottom of the column

        finalColumn = [0] * matrixHeight  # finalRow set to by full of 0s and if any blocks determined, it will be
        # changed to 1
        clues = topClues.getCluesByIndex(column)  # clues for particular column imported from TopClues

        for clue in range(len(clues)):  # fill both boxesToTheTop and boxesToTheBottom
            if clue != 0:
                boxesToTheTop += [0]
            boxesToTheTop += clues[clue] * [1]

        boxesToTheBottom = [0] * (matrixHeight - len(boxesToTheTop)) + boxesToTheTop
        boxesToTheTop += [0] * (matrixHeight - len(boxesToTheTop))

        spacesMet = 0
        anyBlocksMet = False

        for i in range(matrixHeight):  # if a box is 1 in both boxesToTheTop and boxesToTheBottom, then it is
            # definitely a box

            if boxesToTheTop[i] == 0:
                spacesMet += 1

            if boxesToTheBottom[i] == 1:
                anyBlocksMet = True

            if boxesToTheBottom[i] == 0 and anyBlocksMet:
                spacesMet -= 1

            if boxesToTheTop[i] == 1 and boxesToTheBottom[i] == 1 and \
                    matrixHeight / topClues.getSumOfCluesInAColumnByIndex(column) < 2.0 and spacesMet == 0:
                finalColumn[i] = 1

        hanjieMatrix.updateMatrix(-1, column, finalColumn)  # updates hanjieMatrix's column


def simpleSpacesOnRows(hanjieMatrix, sideClues):
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for row in range(matrixHeight):

        matrixRow = hanjieMatrix.getMatrixRow(row)  # stores matrix's row to analyze existing blocks and spaces
        clues = sideClues.getCluesByIndex(row)  # clues for particular column imported from SideClues
        finalRow = []  # finalRow set to be blank and any blocks determined wil be added
        lengthOfSequenceOfBlocksFromStart = 0  # stores length of the first pattern of blocks met

        for box in range(matrixWidth):  # counts lengthOfSequenceOfBlocksFromStart
            if matrixRow[box] == 1:
                lengthOfSequenceOfBlocksFromStart += 1
            elif lengthOfSequenceOfBlocksFromStart != 0:
                break

        boxesPatternMetLength = 0
        maxBoxesPatternMetLength = 0
        previousSpace = -1  # stores previous space index

        for box in range(matrixWidth):  # determines what are new spaces

            if matrixRow[box] == 1:

                maxBoxesPatternMetLength = max(boxesPatternMetLength, maxBoxesPatternMetLength)

                if maxBoxesPatternMetLength < clues[0] + 1:
                    amountOfSpaces = max(box + lengthOfSequenceOfBlocksFromStart - clues[0], previousSpace + 1)
                    finalRow = amountOfSpaces * [-1] + (box - amountOfSpaces) * [0] + (
                            clues[0] - (box - amountOfSpaces)) * [1]
                    hanjieMatrix.updateMatrix(row, -1, finalRow)

                break

            elif matrixRow[box] == 0:
                boxesPatternMetLength += 1
            else:
                previousSpace = box
                boxesPatternMetLength += 1
                maxBoxesPatternMetLength = max(boxesPatternMetLength, maxBoxesPatternMetLength)
                boxesPatternMetLength = 0

        reversedMatrixRow = matrixRow.copy()[::-1]  # same algorithm applied but from the back of matrixRow
        reversedClues = sideClues.getCluesByIndex(row).copy()[::-1]
        finalRow = []
        lengthOfSequenceOfBlocksFromEnd = 0

        for box in range(matrixWidth):  # counts lengthOfSequenceOfBlocksFromStart
            if reversedMatrixRow[box] == 1:
                lengthOfSequenceOfBlocksFromEnd += 1
            elif lengthOfSequenceOfBlocksFromEnd != 0:
                break

        boxesPatternMetLength = 0
        maxBoxesPatternMetLength = 0
        previousSpace = -1  # stores previous space index

        for box in range(matrixWidth):  # determines what are new spaces

            if reversedMatrixRow[box] == 1:

                maxBoxesPatternMetLength = max(boxesPatternMetLength, maxBoxesPatternMetLength)

                if maxBoxesPatternMetLength < reversedClues[0] + 1:
                    amountOfSpaces = max(box + lengthOfSequenceOfBlocksFromEnd - reversedClues[0], previousSpace + 1)
                    finalRow = amountOfSpaces * [-1] + (box - amountOfSpaces) * [0] + (
                            reversedClues[0] - (box - amountOfSpaces)) * [1]
                    finalRow += [0] * (matrixWidth - len(finalRow))
                    hanjieMatrix.updateMatrix(row, -1, finalRow[::-1])

                break

            elif reversedMatrixRow[box] == 0:
                boxesPatternMetLength += 1
            else:
                previousSpace = box
                boxesPatternMetLength += 1

                maxBoxesPatternMetLength = max(boxesPatternMetLength, maxBoxesPatternMetLength)
                boxesPatternMetLength = 0


def simpleSpacesOnColumns(hanjieMatrix, topClues):  # same algorithm as simpleSpacesOnRow but on columns
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for column in range(matrixWidth):

        matrixColumn = hanjieMatrix.getMatrixColumn(column)  # stores matrix's row to analyze existing blocks and spaces
        clues = topClues.getCluesByIndex(column)  # clues for particular column imported from SideClues
        finalColumn = []  # finalRow set to be blank and any blocks determined wil be added
        lengthOfSequenceOfBlocksFromTop = 0  # stores length of the first pattern of blocks met

        for box in range(matrixHeight):  # counts lengthOfSequenceOfBlocksFromStart
            if matrixColumn[box] == 1:
                lengthOfSequenceOfBlocksFromTop += 1
            elif lengthOfSequenceOfBlocksFromTop != 0:
                break

        boxesPatternMetLength = 0
        maxBoxesPatternMetLength = 0
        previousSpace = -1  # stores previous space index

        for box in range(matrixHeight):  # determines what are new spaces

            if matrixColumn[box] == 1:

                maxBoxesPatternMetLength = max(boxesPatternMetLength, maxBoxesPatternMetLength)

                if maxBoxesPatternMetLength < clues[0] + 1:
                    amountOfSpaces = max(box + lengthOfSequenceOfBlocksFromTop - clues[0], previousSpace + 1)
                    finalColumn = amountOfSpaces * [-1] + (box - amountOfSpaces) * [0] + (
                            clues[0] - (box - amountOfSpaces)) * [1]
                    hanjieMatrix.updateMatrix(-1, column, finalColumn)

                break

            elif matrixColumn[box] == 0:
                boxesPatternMetLength += 1
            else:
                previousSpace = box
                boxesPatternMetLength += 1

                maxBoxesPatternMetLength = max(boxesPatternMetLength, maxBoxesPatternMetLength)
                boxesPatternMetLength = 0

        reversedMatrixColumn = matrixColumn.copy()[::-1]  # same algorithm applied but from the back of matrixRow
        reversedClues = topClues.getCluesByIndex(column).copy()[::-1]
        finalColumn = []
        lengthOfSequenceOfBlocksFromBottom = 0

        for box in range(matrixHeight):  # counts lengthOfSequenceOfBlocksFromStart
            if reversedMatrixColumn[box] == 1:
                lengthOfSequenceOfBlocksFromBottom += 1
            elif lengthOfSequenceOfBlocksFromBottom != 0:
                break

        boxesPatternMetLength = 0
        maxBoxesPatternMetLength = 0
        previousSpace = -1  # stores previous space index

        for box in range(matrixHeight):  # determines what are new spaces

            if reversedMatrixColumn[box] == 1:

                maxBoxesPatternMetLength = max(boxesPatternMetLength, maxBoxesPatternMetLength)

                if maxBoxesPatternMetLength < reversedClues[0] + 1:
                    amountOfSpaces = max(box + lengthOfSequenceOfBlocksFromBottom - reversedClues[0], previousSpace + 1)
                    finalColumn = amountOfSpaces * [-1] + (box - amountOfSpaces) * [0] + (
                            reversedClues[0] - (box - amountOfSpaces)) * [1]
                    finalColumn += [0] * (matrixWidth - len(finalColumn))
                    hanjieMatrix.updateMatrix(-1, column, finalColumn[::-1])

                break

            elif reversedMatrixColumn[box] == 0:
                boxesPatternMetLength += 1
            else:
                previousSpace = box
                boxesPatternMetLength += 1
                maxBoxesPatternMetLength = max(boxesPatternMetLength, maxBoxesPatternMetLength)
                boxesPatternMetLength = 0


def forcingOnRows(hanjieMatrix, sideClues):  # Forcing on rows technique coded
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for row in range(matrixHeight):

        matrixRow = hanjieMatrix.getMatrixRow(row)  # a row we will be operating with
        clues = sideClues.getCluesByIndex(row)  # clues for the row

        finalRow = []
        anyNonSpacesMet = False  # whenever we meet 0 or 1 this turns True
        anyOtherNonSpacesMet = False  # if there is 2 or more 0s or 1s this turns True
        sequenceOfNonSpacesLength = 0  # counts length of the first pattern of 0s or 1s met
        amountOfOtherNonSpaces = 0  # counts amount of other 0s or 1s that are not included in sequenceOfNonSpacesLength

        for box in range(matrixWidth):
            if matrixRow[box] == -1 and anyNonSpacesMet:
                if sequenceOfNonSpacesLength < clues[0]:
                    finalRow = [-1] * box
                    hanjieMatrix.updateMatrix(row, -1, finalRow)
                else:
                    for i in range(box, matrixWidth):
                        if matrixRow[i] != -1:
                            anyOtherNonSpacesMet = True
                            amountOfOtherNonSpaces += 1
                        elif matrixRow[i] == -1:
                            if anyOtherNonSpacesMet:
                                amountOfOtherNonSpaces += 1
                                anyOtherNonSpacesMet = False

                    if amountOfOtherNonSpaces < len(clues) - 1 + sum(clues):
                        try:
                            if sequenceOfNonSpacesLength < clues[0] + clues[1] + 1:
                                if sequenceOfNonSpacesLength > (sequenceOfNonSpacesLength - clues[0]) * 2:
                                    finalRow = (box - sequenceOfNonSpacesLength) * [-1] + (
                                            sequenceOfNonSpacesLength - clues[0]) * [0] + (
                                                       sequenceOfNonSpacesLength - (
                                                       sequenceOfNonSpacesLength - clues[0]) * 2) * [1]
                                    hanjieMatrix.updateMatrix(row, -1, finalRow)
                        except IndexError:
                            if sequenceOfNonSpacesLength > (sequenceOfNonSpacesLength - clues[0]) * 2:
                                finalRow = (box - sequenceOfNonSpacesLength) * [-1] + (
                                        sequenceOfNonSpacesLength - clues[0]) * [0] + (
                                                   sequenceOfNonSpacesLength - (
                                                   sequenceOfNonSpacesLength - clues[0]) * 2) * [1]
                                hanjieMatrix.updateMatrix(row, -1, finalRow)
                break
            elif matrixRow[box] == 0 or matrixRow[box] == 1:
                sequenceOfNonSpacesLength += 1
                anyNonSpacesMet = True

        finalRow = []  # All the variables are set to initial values, because same
        anyNonSpacesMet = False  # algorithm implemented, but from left side of the row
        anyOtherNonSpacesMet = False
        sequenceOfNonSpacesLength = 0
        amountOfOtherNonSpaces = 0

        for box in range(matrixWidth - 1, -1, -1):
            if matrixRow[box] == -1 and anyNonSpacesMet:
                if sequenceOfNonSpacesLength < clues[-1]:
                    finalRow = [0] * box + [-1] * (matrixWidth - box)
                    hanjieMatrix.updateMatrix(row, -1, finalRow)
                else:
                    for i in range(box, -1, -1):
                        if matrixRow[i] != -1:
                            anyOtherNonSpacesMet = True
                            amountOfOtherNonSpaces += 1
                        elif matrixRow[i] == -1:
                            if anyOtherNonSpacesMet:
                                amountOfOtherNonSpaces += 1
                                anyOtherNonSpacesMet = False

                    if amountOfOtherNonSpaces < len(clues) - 1 + sum(clues):
                        try:

                            if sequenceOfNonSpacesLength < clues[-1] + clues[-2] + 1:
                                if sequenceOfNonSpacesLength > (sequenceOfNonSpacesLength - clues[-1]) * 2:
                                    finalRow = (box + 1) * [0] + (sequenceOfNonSpacesLength - clues[-1]) * [0] + (
                                            sequenceOfNonSpacesLength - (sequenceOfNonSpacesLength - clues[-1]) * 2) * [
                                                   1]
                                    hanjieMatrix.updateMatrix(row, -1, finalRow)
                        except IndexError:
                            if sequenceOfNonSpacesLength > (sequenceOfNonSpacesLength - clues[-1]) * 2:
                                finalRow = (box + 1) * [0] + (sequenceOfNonSpacesLength - clues[-1]) * [0] + (
                                        sequenceOfNonSpacesLength - (sequenceOfNonSpacesLength - clues[-1]) * 2) * [1]
                                hanjieMatrix.updateMatrix(row, -1, finalRow)
                break

            elif matrixRow[box] == 0 or matrixRow[box] == 1:
                sequenceOfNonSpacesLength += 1
                anyNonSpacesMet = True


def forcingOnColumns(hanjieMatrix, topClues):  # same algorithm implemented as forcing on rows but on columns now
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for column in range(matrixWidth):

        matrixColumn = hanjieMatrix.getMatrixColumn(column)
        clues = topClues.getCluesByIndex(column)

        finalColumn = []
        anyNonSpacesMet = False
        anyOtherNonSpacesMet = False
        sequenceLength = 0
        amountOfOtherNonSpaces = 0  # ones that are not counted in sequenceLength

        for box in range(matrixHeight):
            if matrixColumn[box] == -1 and anyNonSpacesMet:
                if sequenceLength < clues[0]:
                    finalColumn = [-1] * box
                    hanjieMatrix.updateMatrix(-1, column, finalColumn)
                else:
                    for i in range(box, matrixWidth):
                        if matrixColumn[i] != -1:
                            amountOfOtherNonSpaces += 1
                            anyOtherNonSpacesMet = True
                        elif matrixColumn[i] == -1:
                            if anyOtherNonSpacesMet:
                                amountOfOtherNonSpaces += 1
                                anyOtherNonSpacesMet = False

                    if amountOfOtherNonSpaces < len(clues) - 1 + sum(clues):
                        try:
                            if sequenceLength < clues[0] + clues[1] + 1:
                                if sequenceLength > (sequenceLength - clues[0]) * 2:
                                    finalColumn = (box - sequenceLength) * [-1] + (sequenceLength - clues[0]) * [0] + (
                                            sequenceLength - (sequenceLength - clues[0]) * 2) * [1]
                                    hanjieMatrix.updateMatrix(-1, column, finalColumn)
                        except IndexError:
                            if sequenceLength > (sequenceLength - clues[0]) * 2:
                                finalColumn = (box - sequenceLength) * [-1] + (sequenceLength - clues[0]) * [0] + (
                                        sequenceLength - (sequenceLength - clues[0]) * 2) * [1]
                                hanjieMatrix.updateMatrix(-1, column, finalColumn)
                break

            elif matrixColumn[box] == 0 or matrixColumn[box] == 1:
                sequenceLength += 1
                anyNonSpacesMet = True

        finalColumn = []  # All the variables are set to initial values, because same
        anyNonSpacesMet = False  # algorithm implemented, but from left side of the row
        anyOtherNonSpacesMet = False

        sequenceLength = 0
        amountOfOtherNonSpaces = 0

        for box in range(matrixHeight - 1, -1, -1):
            if matrixColumn[box] == -1 and anyNonSpacesMet:
                if sequenceLength < clues[-1]:
                    finalColumn = [0] * box + [-1] * (matrixWidth - box)
                    hanjieMatrix.updateMatrix(-1, column, finalColumn)
                else:
                    for i in range(box, -1, -1):
                        if matrixColumn[i] != -1:
                            amountOfOtherNonSpaces += 1
                            anyOtherNonSpacesMet = True
                        elif matrixColumn[i] == -1:
                            if anyOtherNonSpacesMet:
                                amountOfOtherNonSpaces += 1
                                anyOtherNonSpacesMet = False
                    if amountOfOtherNonSpaces < len(clues) - 1 + sum(clues):
                        try:
                            if sequenceLength < clues[-1] + clues[-2] + 1:
                                if sequenceLength > (sequenceLength - clues[-1]) * 2:
                                    finalColumn = (box + 1) * [0] + (sequenceLength - clues[-1]) * [0] + (
                                            sequenceLength - (sequenceLength - clues[-1]) * 2) * [1]
                                    hanjieMatrix.updateMatrix(-1, column, finalColumn)
                        except IndexError:
                            if sequenceLength > (sequenceLength - clues[-1]) * 2:
                                finalColumn = (box + 1) * [0] + (sequenceLength - clues[-1]) * [0] + (
                                        sequenceLength - (sequenceLength - clues[-1]) * 2) * [1]
                                hanjieMatrix.updateMatrix(-1, column, finalColumn)
                break

            elif matrixColumn[box] == 0 or matrixColumn[box] == 1:
                sequenceLength += 1
                anyNonSpacesMet = True


def glueOnRows(hanjieMatrix, sideClues):  # Glues technique coded
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for row in range(matrixHeight):

        matrixRow = hanjieMatrix.getMatrixRow(row)  # a row we will be operating with
        clues = sideClues.getCluesByIndex(row)  # clues for the row imported
        finalRow = []
        previousSpace = -1  # this stores index of last -1 met

        for box in range(matrixWidth):
            if matrixRow[box] == -1:
                previousSpace = box  # whenever we meet a space, previousSpace is updated
            if matrixRow[box] == 1:
                if box - (previousSpace + 1) - 1 < clues[0]:
                    amountOfBoxesToColor = clues[0] - (box - (previousSpace + 1))
                    finalRow = [0] * box + [1] * amountOfBoxesToColor
                    hanjieMatrix.updateMatrix(row, -1, finalRow)
                    break

        finalRow = []  # same thing done but from the other side of row
        previousSpace = matrixWidth

        for box in range(matrixWidth - 1, -1, -1):
            if matrixRow[box] == -1:
                previousSpace = box
            if matrixRow[box] == 1:
                if (previousSpace - 1) - box - 1 < clues[-1]:
                    amountOfBoxesToColor = clues[-1] - ((previousSpace - 1) - box)
                    finalRow = [0] * (matrixWidth - (matrixWidth - box - 1) - amountOfBoxesToColor) + [
                        1] * amountOfBoxesToColor
                    hanjieMatrix.updateMatrix(row, -1, finalRow)
                    break


def glueOnColumns(hanjieMatrix, topClues):  # same technique as glueOnRows, but on columns now
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for column in range(matrixWidth):

        matrixColumn = hanjieMatrix.getMatrixColumn(column)
        clues = topClues.getCluesByIndex(column)
        finalRow = []
        previousSpace = -1

        for box in range(matrixHeight):
            if matrixColumn[box] == -1:
                previousSpace = box
            if matrixColumn[box] == 1:
                if box - (previousSpace + 1) - 1 < clues[0]:
                    amountOfBoxesToColor = clues[0] - (box - (previousSpace + 1))
                    finalColumn = [0] * box + [1] * amountOfBoxesToColor
                    hanjieMatrix.updateMatrix(-1, column, finalColumn)
                    break

        finalRow = []
        previousSpace = matrixHeight

        for box in range(matrixHeight - 1, -1, -1):
            if matrixColumn[box] == -1:
                previousSpace = box
            if matrixColumn[box] == 1:
                if (previousSpace - 1) - box - 1 < clues[-1]:
                    amountOfBoxesToColor = clues[-1] - ((previousSpace - 1) - box)
                    finalColumn = [0] * (matrixWidth - (matrixWidth - box - 1) - amountOfBoxesToColor) + [
                        1] * amountOfBoxesToColor
                    hanjieMatrix.updateMatrix(-1, column, finalColumn)
                    break


def splittingOnRows(hanjieMatrix, sideClues):  # splitting on rows technique coded
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for row in range(matrixHeight):

        matrixRow = hanjieMatrix.getMatrixRow(row)  # a row we will be operating with
        clues = sideClues.getCluesByIndex(row)  # clues for the row implemented
        finalRow = []  # this will store all changes to existing row

        patternOfBlocksLength = 0  # counts length of first pattern of blocks met
        patternOfBlocksStart = 0  # stores an index at which pattern of blocks starts
        patternOfSpacesLength = 0  # counts length of every pattern of spaces
        maxPatternOfSpacesLength = 0  # stores maximum from all pattern of spaces lengths
        anyBlocksMet = False  # whenever a block met this changes to True

        for box in range(matrixWidth):

            if matrixRow[box] == -1 and not anyBlocksMet:
                maxPatternOfSpacesLength = max(maxPatternOfSpacesLength, patternOfSpacesLength)
                patternOfSpacesLength = 0

            elif matrixRow[box] == 0 and not anyBlocksMet:
                patternOfSpacesLength += 1

            elif matrixRow[box] == 1:

                if not anyBlocksMet:
                    patternOfSpacesLength -= 1
                    maxPatternOfSpacesLength = max(maxPatternOfSpacesLength, patternOfSpacesLength)
                    patternOfSpacesLength = 0
                    patternOfBlocksStart = box

                anyBlocksMet = True
                patternOfBlocksLength += 1

            elif anyBlocksMet:
                break

        if clues[0] == patternOfBlocksLength and maxPatternOfSpacesLength < clues[0]:
            finalRow = [-1] * patternOfBlocksStart + [1] * patternOfBlocksLength + [-1] * min(
                1, matrixWidth - patternOfBlocksStart - patternOfBlocksLength)
            hanjieMatrix.updateMatrix(row, -1, finalRow)

        patternOfBlocksLength = 0  # all variables set to initial values because same algorithm
        # implemented but from the other side of the row
        patternOfSpacesLength = 0
        maxPatternOfSpacesLength = 0
        patternOfBlocksStart = 0
        anyBlocksMet = False

        for box in range(matrixWidth - 1, -1, -1):

            if matrixRow[box] == -1 and not anyBlocksMet:
                maxPatternOfSpacesLength = max(maxPatternOfSpacesLength, patternOfSpacesLength)
                patternOfSpacesLength = 0

            if matrixRow[box] == 0 and not anyBlocksMet:
                patternOfSpacesLength += 1

            if matrixRow[box] == 1:

                if not anyBlocksMet:
                    patternOfSpacesLength -= 1
                    maxPatternOfSpacesLength = max(maxPatternOfSpacesLength, patternOfSpacesLength)
                    patternOfSpacesLength = 0
                    patternOfBlocksStart = box

                anyBlocksMet = True
                patternOfBlocksLength += 1

            elif anyBlocksMet:
                break

        if clues[-1] == patternOfBlocksLength and maxPatternOfSpacesLength < clues[-1]:
            finalRow = [0] * (patternOfBlocksStart - patternOfBlocksLength) + [-1] * min(  # a new row built
                patternOfBlocksStart + 1 - patternOfBlocksLength, 1) + [1] * patternOfBlocksLength + [
                           -1] * (matrixWidth - 1 - patternOfBlocksStart)
            hanjieMatrix.updateMatrix(row, -1, finalRow)  # hanjieMatrix's row updated


def splittingOnColumns(hanjieMatrix, topClues):  # same algorithm as splittingOnRows, but on columns now
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for column in range(matrixWidth):

        matrixColumn = hanjieMatrix.getMatrixColumn(column)
        clues = topClues.getCluesByIndex(column)
        finalColumn = []

        patternOfBlocksLength = 0
        patternOfSpacesLength = 0
        maxPatternOfSpacesLength = 0
        patternOfBlocksStart = 0
        anyBlocksMet = False

        for box in range(matrixHeight):
            if matrixColumn[box] == -1 and not anyBlocksMet:
                maxPatternOfSpacesLength = max(maxPatternOfSpacesLength, patternOfSpacesLength)
                patternOfSpacesLength = 0

            if matrixColumn[box] == 0 and not anyBlocksMet:
                patternOfSpacesLength += 1

            if matrixColumn[box] == 1:

                if not anyBlocksMet:
                    patternOfSpacesLength -= 1
                    maxPatternOfSpacesLength = max(maxPatternOfSpacesLength, patternOfSpacesLength)
                    patternOfSpacesLength = 0
                    patternOfBlocksStart = box

                anyBlocksMet = True
                patternOfBlocksLength += 1

            elif anyBlocksMet:
                break

        if clues[0] == patternOfBlocksLength and maxPatternOfSpacesLength < clues[0]:
            finalColumn = [-1] * patternOfBlocksStart + [
                1] * patternOfBlocksLength + [-1] * min(1, matrixHeight - patternOfBlocksStart - patternOfBlocksLength)
            hanjieMatrix.updateMatrix(-1, column, finalColumn)

        patternOfBlocksLength = 0
        patternOfSpacesLength = 0
        maxPatternOfSpacesLength = 0
        patternOfBlocksStart = 0
        anyBlocksMet = False

        for box in range(matrixHeight - 1, -1, -1):
            if matrixColumn[box] == -1 and not anyBlocksMet:
                maxPatternOfSpacesLength = max(maxPatternOfSpacesLength, patternOfSpacesLength)
                patternOfSpacesLength = 0

            if matrixColumn[box] == 0 and not anyBlocksMet:
                patternOfSpacesLength += 1

            if matrixColumn[box] == 1:

                if not anyBlocksMet:
                    patternOfSpacesLength -= 1
                    maxPatternOfSpacesLength = max(maxPatternOfSpacesLength, patternOfSpacesLength)
                    patternOfSpacesLength = 0
                    patternOfBlocksStart = box

                anyBlocksMet = True
                patternOfBlocksLength += 1

            elif anyBlocksMet:
                break

        if clues[-1] == patternOfBlocksLength and maxPatternOfSpacesLength < clues[-1]:
            finalColumn = [0] * (patternOfBlocksStart - patternOfBlocksLength) + [-1] * min(
                patternOfBlocksStart + 1 - patternOfBlocksLength, 1) + [1] * patternOfBlocksLength + [
                              -1] * (matrixHeight - 1 - patternOfBlocksStart)
            hanjieMatrix.updateMatrix(-1, column, finalColumn)


def joiningOnRows(hanjieMatrix, sideClues):  # joining on rows technique coded
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for row in range(matrixHeight):

        matrixRow = hanjieMatrix.getMatrixRow(row)  # row we will be working with imported from hanjieMatrix
        clues = sideClues.getCluesByIndex(row)  # clues for the row imported
        finalRow = []

        firstPatternOfBlocksMet = False  # we are looking for a pattern that start with blocks, then spaces and
        patternOfSpacesMet = False  # finishes with blocks again, these three variables turn True when each pattern met
        secondPatternOfBlocksMet = False

        # where the whole pattern to join starts and ends
        toJoinStart = -1
        toJoinEnd = -1

        for box in range(matrixWidth):

            if matrixRow[box] == 1:
                if not patternOfSpacesMet:
                    if not firstPatternOfBlocksMet:
                        toJoinStart = box
                    firstPatternOfBlocksMet = True

                else:
                    secondPatternOfBlocksMet = True

            elif matrixRow[box] == 0:
                if secondPatternOfBlocksMet:
                    toJoinEnd = box - 1
                    break
                elif firstPatternOfBlocksMet:
                    patternOfSpacesMet = True

            elif matrixRow[box] == -1:
                if secondPatternOfBlocksMet:
                    toJoinEnd = box - 1
                    break
                else:
                    firstPatternOfBlocksMet = False
                    patternOfSpacesMet = False
                    secondPatternOfBlocksMet = False

        if toJoinEnd == -1 and firstPatternOfBlocksMet and patternOfSpacesMet and secondPatternOfBlocksMet:
            toJoinEnd = matrixWidth - 1

        if toJoinEnd != -1:
            minClueLength = toJoinEnd - toJoinStart + 1
            if minClueLength <= max(clues):
                for clue in range(len(clues)):
                    if clues[clue] >= minClueLength:
                        if sum(clues[:clue + 1]) + len(clues[:clue + 1]) - 1 > toJoinStart > sum(clues[:clue]) + len(
                                clues[:clue]) - 1:
                            # new row to update matrix built
                            if clues[clue] == minClueLength:
                                finalRow = [0] * (toJoinStart - 1) + [-1] * min(1, toJoinStart) + [
                                    1] * minClueLength + [-1]
                            else:
                                finalRow = [0] * toJoinStart + [1] * minClueLength

                            hanjieMatrix.updateMatrix(row, -1, finalRow)  # hanjieMatrix's row updated
                            break

        reversedMatrixRow = hanjieMatrix.getMatrixRow(row)[
                            ::-1]  # row we will be working with imported from hanjieMatrix
        reversedClues = sideClues.getCluesByIndex(row)[::-1]  # clues for the row imported
        finalRow = []

        firstPatternOfBlocksMet = False  # we are looking for a pattern that start with blocks, then spaces and
        patternOfSpacesMet = False  # finishes with blocks again, these three variables turn True when each pattern met
        secondPatternOfBlocksMet = False

        # where the whole pattern to join starts and ends
        toJoinStart = -1
        toJoinEnd = -1

        for box in range(matrixWidth):

            if reversedMatrixRow[box] == 1:
                if not patternOfSpacesMet:
                    if not firstPatternOfBlocksMet:
                        toJoinStart = box
                    firstPatternOfBlocksMet = True

                else:
                    secondPatternOfBlocksMet = True

            elif reversedMatrixRow[box] == 0:
                if secondPatternOfBlocksMet:
                    toJoinEnd = box - 1
                    break
                elif firstPatternOfBlocksMet:
                    patternOfSpacesMet = True

            elif reversedMatrixRow[box] == -1:
                if secondPatternOfBlocksMet:
                    toJoinEnd = box - 1
                    break
                else:
                    firstPatternOfBlocksMet = False
                    patternOfSpacesMet = False
                    secondPatternOfBlocksMet = False

        if toJoinEnd == -1 and firstPatternOfBlocksMet and patternOfSpacesMet and secondPatternOfBlocksMet:
            toJoinEnd = matrixWidth - 1

        if toJoinEnd != -1:
            minClueLength = toJoinEnd - toJoinStart + 1
            if minClueLength <= max(reversedClues):
                for clue in range(len(clues)):
                    if reversedClues[clue] >= minClueLength:
                        if sum(reversedClues[:clue + 1]) + len(reversedClues[:clue + 1]) - 1 > toJoinStart > sum(
                                reversedClues[:clue]) + len(reversedClues[:clue]) - 1:
                            # new row to update matrix built
                            if reversedClues[clue] == minClueLength:
                                finalRow = [0] * (toJoinStart - 1) + [-1] * min(1, toJoinStart) + [
                                    1] * minClueLength + [-1]
                            else:
                                finalRow = [0] * toJoinStart + [1] * minClueLength

                            hanjieMatrix.updateMatrix(row, -1, finalRow[::-1])  # hanjieMatrix's row updated
                            break


def joiningOnColumns(hanjieMatrix, topClues):  # same algorithm as joiningOnRows but on columns
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for column in range(matrixWidth):

        matrixColumn = hanjieMatrix.getMatrixColumn(column)
        clues = topClues.getCluesByIndex(column)
        finalColumn = []

        firstPatternOfBlocksMet = False
        patternOfSpacesMet = False
        secondPatternOfBlocksMet = False

        toJoinStart = -1
        toJoinEnd = -1

        for box in range(matrixHeight):

            if matrixColumn[box] == 1:
                if not patternOfSpacesMet:
                    if not firstPatternOfBlocksMet:
                        toJoinStart = box
                    firstPatternOfBlocksMet = True

                else:
                    secondPatternOfBlocksMet = True

            elif matrixColumn[box] == 0:
                if firstPatternOfBlocksMet:
                    patternOfSpacesMet = True
                if secondPatternOfBlocksMet:
                    toJoinEnd = box - 1
                    break

            elif matrixColumn[box] == -1:
                if secondPatternOfBlocksMet:
                    toJoinEnd = box - 1
                    break
                else:
                    firstPatternOfBlocksMet = False
                    patternOfSpacesMet = False
                    secondPatternOfBlocksMet = False

        if toJoinEnd == -1 and firstPatternOfBlocksMet and patternOfSpacesMet and secondPatternOfBlocksMet:
            toJoinEnd = matrixHeight - 1

        if toJoinEnd != -1:
            minClueLength = toJoinEnd - toJoinStart + 1
            if minClueLength <= max(clues):
                for clue in range(len(clues)):
                    if clues[clue] >= minClueLength:
                        if sum(clues[:clue + 1]) + len(clues[:clue + 1]) - 1 > toJoinStart > sum(clues[:clue]) + len(
                                clues[:clue]) - 1:
                            if clues[clue] == minClueLength:
                                finalColumn = [0] * (toJoinStart - 1) + [-1] * min(1, toJoinStart) + [
                                    1] * minClueLength + [
                                                  -1]
                            else:
                                finalColumn = [0] * toJoinStart + [1] * minClueLength

                            hanjieMatrix.updateMatrix(-1, column, finalColumn)
                            break

        reversedMatrixColumn = hanjieMatrix.getMatrixColumn(column)[::-1]
        reversedClues = topClues.getCluesByIndex(column)[::-1]
        finalColumn = []

        firstPatternOfBlocksMet = False
        patternOfSpacesMet = False
        secondPatternOfBlocksMet = False

        toJoinStart = -1
        toJoinEnd = -1

        for box in range(matrixHeight):

            if reversedMatrixColumn[box] == 1:
                if not patternOfSpacesMet:
                    if not firstPatternOfBlocksMet:
                        toJoinStart = box
                    firstPatternOfBlocksMet = True

                else:
                    secondPatternOfBlocksMet = True

            elif reversedMatrixColumn[box] == 0:
                if firstPatternOfBlocksMet:
                    patternOfSpacesMet = True
                if secondPatternOfBlocksMet:
                    toJoinEnd = box - 1
                    break

            elif reversedMatrixColumn[box] == -1:
                if secondPatternOfBlocksMet:
                    toJoinEnd = box - 1
                    break
                else:
                    firstPatternOfBlocksMet = False
                    patternOfSpacesMet = False
                    secondPatternOfBlocksMet = False

        if toJoinEnd == -1 and firstPatternOfBlocksMet and patternOfSpacesMet and secondPatternOfBlocksMet:
            toJoinEnd = matrixHeight - 1

        if toJoinEnd != -1:
            minClueLength = toJoinEnd - toJoinStart + 1
            if minClueLength <= max(clues):
                for clue in range(len(clues)):
                    if reversedClues[clue] >= minClueLength:
                        if sum(reversedClues[:clue + 1]) + len(reversedClues[:clue + 1]) - 1 > toJoinStart > sum(
                                reversedClues[:clue]) + len(reversedClues[:clue]) - 1:
                            if reversedClues[clue] == minClueLength:
                                finalColumn = [0] * (toJoinStart - 1) + [-1] * min(1, toJoinStart) + [
                                    1] * minClueLength + [-1]
                            else:
                                finalColumn = [0] * toJoinStart + [1] * minClueLength

                            hanjieMatrix.updateMatrix(-1, column, finalColumn)
                            break


def allCluesFilledOnRows(hanjieMatrix, sideClues):  # allCluesFilledOnRows coded
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for row in range(matrixHeight):

        matrixRow = hanjieMatrix.getMatrixRow(row)  # a row to work with
        clues = sideClues.getCluesByIndex(row)  # clues for the row
        finalRow = []  # final row to apply changes
        matrixRowCopy = matrixRow.copy()  # copy of a row from hanjieMatrix not to cause changes to global thing
        cluesCopy = clues.copy()  # copy of clues from SideClues not to cause changes to global thing

        allCluesFilled = True  # if not every clue already in a row, it will turn False
        patternOfBlocks = 0  # counts length of each pattern of blocks
        for box in range(matrixWidth):
            if matrixRow[box] == 1:
                patternOfBlocks += 1
            else:
                try:  # in case pattern of blocks does not fit any of clues it catches an exception and breaks the loop
                    if patternOfBlocks != 0:
                        cluesCopy.remove(patternOfBlocks)
                        patternOfBlocks = 0
                except ValueError:
                    allCluesFilled = False
                    patternOfBlocks = 0
                    break

        if patternOfBlocks != 0:
            try:
                cluesCopy.remove(patternOfBlocks)
            except ValueError:
                allCluesFilled = False

        # if all patterns fit all patterns of boxes, it means that any unknown boxes left are spaces
        if allCluesFilled and len(cluesCopy) == 0:
            for i in range(matrixWidth):
                if matrixRow[i] == 0:
                    matrixRowCopy[i] = -1
            hanjieMatrix.updateMatrix(row, -1, matrixRowCopy)  # update matrix with a new row


def allCluesFilledOnColumns(hanjieMatrix, topClues):  # same technique as allCluesFilledOnRows but on columns now
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for column in range(matrixWidth):

        matrixColumn = hanjieMatrix.getMatrixColumn(column)
        clues = topClues.getCluesByIndex(column)
        matrixColumnCopy = matrixColumn.copy()
        cluesCopy = clues.copy()
        finalRow = []

        allCluesFilled = True
        patternOfBlocks = 0
        for box in range(matrixHeight):
            if matrixColumn[box] == 1:
                patternOfBlocks += 1
            else:
                try:
                    if patternOfBlocks != 0:
                        cluesCopy.remove(patternOfBlocks)
                        patternOfBlocks = 0
                except ValueError:
                    allCluesFilled = False
                    patternOfBlocks = 0
                    break

        if patternOfBlocks != 0:
            try:
                cluesCopy.remove(patternOfBlocks)
            except ValueError:
                allCluesFilled = False

        if allCluesFilled and len(cluesCopy) == 0:
            for i in range(matrixHeight):
                if matrixColumn[i] == 0:
                    matrixColumnCopy[i] = -1
            hanjieMatrix.updateMatrix(-1, column, matrixColumnCopy)


def allSpacesFilledOnRows(hanjieMatrix, sideClues):  # allSpacesFilledOnRows technique coded
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for row in range(matrixHeight):

        matrixRow = hanjieMatrix.getMatrixRow(row)  # a row to operate with
        clues = sideClues.getCluesByIndex(row)  # clues for the row
        finalRow = []  # stores final result after all changes application
        previousSpace = -1  # stores previous space's index
        boxesPatternLength = 0

        for box in range(matrixWidth):

            if matrixRow[box] == -1:
                if previousSpace != -1:
                    boxesPatternLength = box - previousSpace - 1
                    if boxesPatternLength < min(clues):
                        finalRow = [0] * (previousSpace + 1) + [-1] * boxesPatternLength  # builds a new row
                        hanjieMatrix.updateMatrix(row, -1, finalRow)  # updates hanjieMatrix with a new row
                    previousSpace = box

            elif matrixRow[box] == 1:
                previousSpace = -1


def allSpacesFilledOnColumns(hanjieMatrix, topClues):  # same technique as allSpacedFilledOnRows but on columns
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for column in range(matrixWidth):

        matrixColumn = hanjieMatrix.getMatrixColumn(column)
        clues = topClues.getCluesByIndex(column)
        finalColumn = []
        previousSpace = -1
        boxesPatternLength = 0

        for box in range(matrixHeight):

            if matrixColumn[box] == -1:
                if previousSpace != -1:
                    boxesPatternLength = box - previousSpace - 1
                    if boxesPatternLength < min(clues):
                        finalColumn = [0] * (previousSpace + 1) + [-1] * boxesPatternLength
                        hanjieMatrix.updateMatrix(-1, column, finalColumn)
                previousSpace = box

            elif matrixColumn[box] == 1:
                previousSpace = -1


def main():  # this is main function that does all the functionality
    topClues = TopClues(askUserForTopClues())  # gets side clues from user input
    sideClues = SideClues(askUserForSideClues())  # gets side clues from user input

    hanjieMatrix = HanjieMatrix(topClues.getSize(), sideClues.getSize(), [])  # initializes a blank hanjieMatrix

    hanjieMatrix.initializeFreeMatrix()  # fills matrix with 0s

    # These techniques are not dependent on existing blocks and spaces, so they can be implemented once:
    fullRow(hanjieMatrix, sideClues)
    fullColumn(hanjieMatrix, topClues)
    simpleBoxesOnRows(hanjieMatrix, sideClues)
    simpleBoxesOnColumns(hanjieMatrix, topClues)
    simpleSpacesOnRows(hanjieMatrix, sideClues)
    simpleSpacesOnColumns(hanjieMatrix, topClues)
    i = 0
    while i <= 100:  # other techniques dependent on each other, so they all are repeated 10 times.
        forcingOnRows(hanjieMatrix, sideClues)
        forcingOnColumns(hanjieMatrix, topClues)
        glueOnRows(hanjieMatrix, sideClues)
        glueOnColumns(hanjieMatrix, topClues)
        splittingOnRows(hanjieMatrix, sideClues)
        splittingOnColumns(hanjieMatrix, topClues)
        joiningOnRows(hanjieMatrix, sideClues)
        joiningOnColumns(hanjieMatrix, topClues)
        allCluesFilledOnRows(hanjieMatrix, sideClues)
        allCluesFilledOnColumns(hanjieMatrix, topClues)
        allSpacesFilledOnRows(hanjieMatrix, sideClues)
        allSpacesFilledOnColumns(hanjieMatrix, topClues)
        i += 1

    hanjieMatrix.outputMatrix()  # outputs matrix to console in form of matrix of green, red and blue squares


# Main code
main()
