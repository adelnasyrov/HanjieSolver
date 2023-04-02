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

    def getMatrixRow(self, row):
        return self._matrix[row]

    def getMatrixColumn(self, column):
        matrixColumn = []
        for row in range(self._matrixHeight):
            matrixColumn.append(self._matrix[row][column])
        return matrixColumn

    def initializeFreeMatrix(self):

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

    def outputMatrix(self):
        for i in range(self._matrixHeight):
            for j in range(self._matrixWidth):
                if self._matrix[i][j] == 1:
                    print('🟩', end="")
                elif self._matrix[i][j] == -1:
                    print('🟦', end="")
                else:
                    print('🟥', end="")
            print()


class TopClues:  # A class that stores clues from the top of a puzzle
    _topClues = []

    def __init__(self, numbers):  # Initialization requires a 2-d array with clues to be provided
        self._topClues = numbers

    def getClues(self):  # Returns the whole topClues array
        return self._topClues

    def getTopCluesByIndex(self, index):  # A getter returning an exact column's clues
        return self._topClues[index]

    def getSumOfCluesInAColumnByIndex(self, index):
        sumOfClues = 0
        for elem in self._topClues[index]:
            if elem > 0:
                sumOfClues += elem + 1
        return sumOfClues - 1

    def getSize(self):
        return len(self._topClues)


class SideClues:  # A class that stores clues from a side of a puzzle
    _sideClues = []

    def __init__(self, numbers):  # Initialization requires a 2-d array with clues to be provided
        self._sideClues = numbers

    def getClues(self):  # Returns the whole sideClues array
        return self._sideClues

    def getSideCluesByIndex(self, index):  # A getter returning an exact row's clues
        return self._sideClues[index]

    def getSumOfCluesInARowByIndex(self, index):
        sumOfClues = 0
        for elem in self._sideClues[index]:
            if elem > 0:
                sumOfClues += elem + 1
        return sumOfClues - 1

    def getSize(self):
        return len(self._sideClues)


# class User will be coded soon

def askUserForTopClues():
    topClues_ = []

    print("Type in top clues column by column, when you finish input 'STOP', start with a clue for the first column:")
    columnClueUserInput = input()

    while columnClueUserInput.upper() != "STOP":
        try:
            columnClue = list(map(int, columnClueUserInput.split()))
            topClues_.append(columnClue)
            print("Type a clue for the next column:")
        except ValueError:
            print("You are not typing it right, try again")

        columnClueUserInput = input()

    return topClues_


def askUserForSideClues():
    sideClues_ = []

    print("Type in side clues row by row, when you finish input 'STOP', start with a clue for the first row:")
    rowClueUserInput = input()

    while rowClueUserInput.upper() != "STOP":
        try:
            rowClue = list(map(int, rowClueUserInput.split()))
            sideClues_.append(rowClue)
            print("Type a clue for the next row:")
        except ValueError:
            print("You are not typing it right, try again")

        rowClueUserInput = input()

    return sideClues_


def fullRow(hanjieMatrix, sideClues):
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for row in range(matrixHeight):
        finalRow = []
        if sideClues.getSumOfCluesInARowByIndex(row) == matrixWidth:
            for clue in range(len(sideClues.getSideCluesByIndex(row))):
                if clue != 0:
                    finalRow += [-1]
                finalRow += sideClues.getSideCluesByIndex(row)[clue] * [1]

            hanjieMatrix.updateMatrix(row, -1, finalRow)
        if sum(sideClues.getSideCluesByIndex(row)) == 0:
            finalRow = [-1] * matrixWidth
            hanjieMatrix.updateMatrix(row, -1, finalRow)


def fullColumn(hanjieMatrix, topClues):
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for column in range(matrixWidth):
        finalColumn = []
        if topClues.getSumOfCluesInAColumnByIndex(column) == matrixHeight:
            for clue in range(len(topClues.getTopCluesByIndex(column))):
                if clue != 0:
                    finalColumn += [-1]
                finalColumn += topClues.getTopCluesByIndex(column)[clue] * [1]

            hanjieMatrix.updateMatrix(-1, column, finalColumn)

        if sum(topClues.getTopCluesByIndex(column)) == 0:
            finalColumn = [-1] * matrixHeight
            hanjieMatrix.updateMatrix(-1, column, finalColumn)


def simpleBoxesOnRows(hanjieMatrix, sideClues):
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for row in range(matrixHeight):

        boxesToTheLeft = []
        boxesToTheRight = []
        finalRow = [0] * matrixWidth
        clues = sideClues.getSideCluesByIndex(row)

        for clue in range(len(clues)):
            if clue != 0:
                boxesToTheLeft += [0]
            boxesToTheLeft += clues[clue] * [1]

        boxesToTheRight = [0] * (matrixWidth - len(boxesToTheLeft)) + boxesToTheLeft
        boxesToTheLeft += [0] * (matrixWidth - len(boxesToTheLeft))

        print(boxesToTheLeft)
        print(boxesToTheRight)

        isBetweenSpaces = False
        anyBlocksMet = False

        for i in range(matrixWidth):
            if boxesToTheLeft[i] == 0:
                isBetweenSpaces = True

            if boxesToTheRight[i] == 0 and boxesToTheLeft[i] != 0 and anyBlocksMet:
                isBetweenSpaces = False

            if boxesToTheRight[i] == 1:
                anyBlocksMet = True

            if boxesToTheRight[i] == 1 and boxesToTheLeft[i] == 1 and \
                    matrixWidth / sideClues.getSumOfCluesInARowByIndex(
                row) < 2.0 and not isBetweenSpaces:
                finalRow[i] = 1

        hanjieMatrix.updateMatrix(row, -1, finalRow)


def simpleBoxesOnColumns(hanjieMatrix, topClues):
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for column in range(matrixWidth):

        boxesToTheTop = []
        boxesToTheBottom = []

        finalColumn = [0] * matrixHeight
        clues = topClues.getTopCluesByIndex(column)

        for clue in range(len(clues)):
            if clue != 0:
                boxesToTheTop += [0]
            boxesToTheTop += clues[clue] * [1]

        boxesToTheBottom = [0] * (matrixHeight - len(boxesToTheTop)) + boxesToTheTop
        boxesToTheTop += [0] * (matrixHeight - len(boxesToTheTop))

        print(boxesToTheTop, boxesToTheBottom)

        isBetweenSpaces = False
        anyBlocksMet = False

        for i in range(matrixHeight):

            if boxesToTheTop[i] == 0:
                isBetweenSpaces = True

            if boxesToTheBottom[i] == 1:
                anyBlocksMet = True

            if boxesToTheBottom[i] == 0 and boxesToTheTop[i] != 0 and anyBlocksMet:
                isBetweenSpaces = False

            if boxesToTheTop[i] == 1 and boxesToTheBottom[i] == 1 and \
                    matrixHeight / topClues.getSumOfCluesInAColumnByIndex(column) < 2.0 and not isBetweenSpaces:
                finalColumn[i] = 1

        hanjieMatrix.updateMatrix(-1, column, finalColumn)


def simpleSpacesOnRows(hanjieMatrix, sideClues):
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for row in range(matrixHeight):

        finalRow = []
        matrixRow = hanjieMatrix.getMatrix()[row]
        clues = sideClues.getSideCluesByIndex(row)
        lengthOfSequenceOfOnesFromStart = 0
        lengthOfSequenceOfOnesFromEnd = 0

        for box in range(len(matrixRow)):
            if matrixRow[box] == 1:
                lengthOfSequenceOfOnesFromStart += 1
            elif lengthOfSequenceOfOnesFromStart != 0:
                break

        for box in range(len(matrixRow) - 1, -1, -1):
            if matrixRow[box] == 1:
                lengthOfSequenceOfOnesFromEnd += 1
            elif matrixRow[box] == 0 and lengthOfSequenceOfOnesFromEnd != 0:
                break

        for box in range(len(matrixRow)):
            if matrixRow[box] == 1:
                if len(clues) == 1 and lengthOfSequenceOfOnesFromStart != 0:
                    finalRow = (box - (clues[0] - lengthOfSequenceOfOnesFromStart)) * [-1] + min(
                        lengthOfSequenceOfOnesFromStart + (clues[0] - lengthOfSequenceOfOnesFromStart) * 2,
                        matrixWidth) * [0]
                    finalRow += (matrixWidth - len(finalRow)) * [-1]
                elif box <= clues[0]:
                    finalRow += (box - (clues[0] - lengthOfSequenceOfOnesFromStart)) * [-1]
                break
        hanjieMatrix.updateMatrix(row, -1, finalRow)

        finalRow = []

        for box in range(len(matrixRow) - 1, -1, -1):
            if matrixRow[box] == 1:
                if len(matrixRow) - box - 1 <= clues[-1]:
                    finalRow += ((len(matrixRow) - box - 1) - (clues[-1] - lengthOfSequenceOfOnesFromStart)) * [-1]
                break

        finalRow = [0] * (matrixWidth - len(finalRow)) + finalRow
        hanjieMatrix.updateMatrix(row, -1, finalRow)


def simpleSpacesOnColumns(hanjieMatrix, topClues):
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for column in range(matrixWidth):

        finalColumn = []
        matrixColumn = hanjieMatrix.getMatrixColumn(column)
        clues = topClues.getTopCluesByIndex(column)
        lengthOfSequenceOfOnesFromTop = 0
        lengthOfSequenceOfOnesFromBottom = 0

        for box in range(len(matrixColumn)):
            if matrixColumn[box] == 1:
                lengthOfSequenceOfOnesFromTop += 1
            elif lengthOfSequenceOfOnesFromTop != 0:
                break

        for box in range(len(matrixColumn) - 1, -1, -1):
            if matrixColumn[box] == 1:
                lengthOfSequenceOfOnesFromBottom += 1
            elif matrixColumn[box] == 0 and lengthOfSequenceOfOnesFromBottom != 0:
                break

        for box in range(len(matrixColumn)):
            if matrixColumn[box] == 1:
                if len(clues) == 1 and lengthOfSequenceOfOnesFromTop != 0:
                    finalColumn = (box - (clues[0] - lengthOfSequenceOfOnesFromTop)) * [-1] + min(
                        lengthOfSequenceOfOnesFromTop + (clues[0] - lengthOfSequenceOfOnesFromTop) * 2,
                        matrixHeight) * [0]
                    finalColumn += (matrixHeight - len(finalColumn)) * [-1]
                elif box <= clues[0]:
                    finalColumn += (box - (clues[0] - lengthOfSequenceOfOnesFromTop)) * [-1]
                break
        hanjieMatrix.updateMatrix(-1, column, finalColumn)

        finalColumn = []

        for box in range(len(matrixColumn) - 1, -1, -1):
            if matrixColumn[box] == 1:
                if len(matrixColumn) - box - 1 <= clues[-1]:
                    finalColumn += ((len(matrixColumn) - box - 1) - (clues[-1] - lengthOfSequenceOfOnesFromBottom)) * [
                        -1]
                break

        finalColumn = [0] * (matrixHeight - len(finalColumn)) + finalColumn
        hanjieMatrix.updateMatrix(-1, column, finalColumn)


def forcingOnRows(hanjieMatrix, sideClues):
    matrixHeight = hanjieMatrix.getHeight()
    matrixWidth = hanjieMatrix.getWidth()

    for row in range(matrixHeight):

        matrixRow = hanjieMatrix.getMatrixRow(row)
        clues = sideClues.getSideCluesByIndex(row)

        finalRow = []
        anyNonSpacesMet = False
        sequenceLength = 0
        amountOfOtherNonSpaces = 0  # ones that are not counted in sequenceLength

        print(matrixRow)
        print(matrixWidth)

        for box in range(matrixWidth):
            if matrixRow[box] == -1 and anyNonSpacesMet:
                if sequenceLength < clues[0]:
                    finalRow = [-1] * box
                    hanjieMatrix.updateMatrix(row, -1, finalRow)
                else:
                    for i in range(box, matrixWidth):
                        if matrixRow[i] != -1:
                            amountOfOtherNonSpaces += 1
                    if amountOfOtherNonSpaces < len(clues) - 1 + sum(clues):
                        try:
                            if sequenceLength < clues[0] + clues[1] + 1:
                                if sequenceLength > (sequenceLength - clues[0]) * 2:
                                    finalRow = (box - sequenceLength) * [-1] + (sequenceLength - clues[0]) * [0] + (
                                            sequenceLength - (sequenceLength - clues[0]) * 2) * [1]
                                    hanjieMatrix.updateMatrix(row, -1, finalRow)
                        except IndexError:
                            if sequenceLength > (sequenceLength - clues[0]) * 2:
                                finalRow = (box - sequenceLength) * [-1] + (sequenceLength - clues[0]) * [0] + (
                                        sequenceLength - (sequenceLength - clues[0]) * 2) * [1]
                                hanjieMatrix.updateMatrix(row, -1, finalRow)
                break
            elif matrixRow[box] == 0 or matrixRow[box] == 1:
                sequenceLength += 1
                anyNonSpacesMet = True

        finalRow = []               # All the variables are set to initial values, because same
        anyNonSpacesMet = False     # algorithm implemented, but from left side of the row
        sequenceLength = 0
        amountOfOtherNonSpaces = 0

        for box in range(matrixWidth - 1, -1, -1):
            if matrixRow[box] == -1 and anyNonSpacesMet:
                if sequenceLength < clues[-1]:
                    finalRow = [0] * box + [-1] * (matrixWidth - box)
                    hanjieMatrix.updateMatrix(row, -1, finalRow)
                else:
                    for i in range(box, matrixWidth):
                        if matrixRow[i] != -1:
                            amountOfOtherNonSpaces += 1
                    if amountOfOtherNonSpaces < len(clues) - 1 + sum(clues):
                        try:
                            if sequenceLength < clues[-1] + clues[-2] + 1:
                                if sequenceLength > (sequenceLength - clues[-1]) * 2:
                                    finalRow = (box + 1) * [0]
                                    finalRow = (box - sequenceLength) * [-1] + (sequenceLength - clues[0]) * [0] + (
                                            sequenceLength - (sequenceLength - clues[0]) * 2) * [1]
                                    hanjieMatrix.updateMatrix(row, -1, finalRow)
                        except IndexError:
                            if sequenceLength > (sequenceLength - clues[0]) * 2:
                                finalRow = (box - sequenceLength) * [-1] + (sequenceLength - clues[0]) * [0] + (
                                        sequenceLength - (sequenceLength - clues[0]) * 2) * [1]
                                hanjieMatrix.updateMatrix(row, -1, finalRow)
                break

            elif matrixRow[box] == 0 or matrixRow[box] == 1:
                sequenceLength += 1
                anyNonSpacesMet = True


def main():
    topClues = TopClues(askUserForTopClues())
    sideClues = SideClues(askUserForSideClues())

    hanjieMatrix = HanjieMatrix(topClues.getSize(), sideClues.getSize(), [])
    hanjieMatrix.initializeFreeMatrix()
    fullRow(hanjieMatrix, sideClues)
    fullColumn(hanjieMatrix, topClues)
    simpleBoxesOnRows(hanjieMatrix, sideClues)
    simpleBoxesOnColumns(hanjieMatrix, topClues)
    simpleSpacesOnRows(hanjieMatrix, sideClues)
    simpleSpacesOnColumns(hanjieMatrix, topClues)
    forcingOnRows(hanjieMatrix, sideClues)
    hanjieMatrix.outputMatrix()


main()
