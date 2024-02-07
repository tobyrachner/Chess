from copy import deepcopy

KNIGHT_OFFSETS = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
KING_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

class Piece():
    def __init__(self, game, type, color, square):
        self.game = game
        self.type = type
        self.color = color
        self.image = self.game.images[color][type]
        self.square = square
        self.isPickedUp = False

    def render(self, surface, mpos = None):
        if self.isPickedUp:
            surface.blit(self.image, (mpos[0] - self.game.squareSize // 2, mpos[1] - self.game.squareSize // 2))
        else:
            surface.blit(self.image, (self.square[1] * self.game.squareSize + self.game.renderOffset, self.square[0] * self.game.squareSize + self.game.renderOffset))

    def removeSelfFromBoard(self):
        # Function needed to check if piece a in front of piece b attacks square behind piece b
        board = [x.copy() for x in self.game.board.board]
        board[self.square[0]][self.square[1]] = 0
        return board
    
    def seeIfCheck(self, square):
        board = [x.copy() for x in self.game.board.board]
        board[self.square[0]][self.square[1]] = 0
        board[square[0]][square[1]] = self
        if self.game.kings[self.color].isAttacked(board=board):
            return True

    def isAttacked(self, square=0, returnPieces=False, color=False, countKing=True, board=None):
        if square == 0:
            square = self.square
        if not color:
            color = self.color
        if not board:
            board = self.game.board.board    

        validSquares = range(8)
        piecesInVision = []
        # Diagonals
        stop = [True, True, True, True]
        for i in range(1, 8):
            
            testSquares = [(square[0] + i, square[1] + i), (square[0] - i, square[1] + i), (square[0] + i, square[1] - i), (square[0] - i, square[1] - i)]
            for x in range(4):
                if stop[x]:
                    if testSquares[x][0] in validSquares and testSquares[x][1] in validSquares:
                        onSquare = board[testSquares[x][0]][testSquares[x][1]]
                        if onSquare != 0:
                            stop[x] = False
                            if onSquare.color != color:
                                piecesInVision.append(onSquare)
                    else:
                        stop[x] = False

        # straights              
        stop = [True, True, True, True]
        for i in range(1, 8):
            
            testSquares = [(square[0], square[1] + i), (square[0], square[1] - i), (square[0] + i, square[1]), (square[0] - i, square[1])]
            for x in range(4):
                if stop[x]:
                    if testSquares[x][0] in validSquares and testSquares[x][1] in validSquares:
                        onSquare = board[testSquares[x][0]][testSquares[x][1]]
                        if onSquare != 0:
                            stop[x] = False
                            if onSquare.color != color:
                                piecesInVision.append(onSquare)
                    else:
                        stop[x] = False

        # knight moves
        for offset in KNIGHT_OFFSETS:
            checkSquare = (square[0] + offset[0], square[1] + offset[1])
            if checkSquare[0] in validSquares and checkSquare[1] in validSquares:
                onSquare = board[checkSquare[0]][checkSquare[1]]
                if onSquare != 0 and onSquare.color != color:
                    piecesInVision.append(onSquare)

        
        if returnPieces:
            pieces = []
            for piece in piecesInVision:
                if type(piece) in [Pawn, King]:
                    if square in piece.squaresAttacking(): 
                        pieces.append(piece)
                elif square in piece.availSquares():
                    pieces.append(piece)
            return pieces
        
        for piece in piecesInVision:
            if type(piece) == Pawn:
                if square in piece.squaresAttacking(): 
                    return True
            elif type(piece) == King:
                if square in piece.squaresAttacking() and not countKing:
                    return True 
            elif square in piece.availSquares(getSquaresAttacking=True, board=board):
                return True
            
        return False

class Rook(Piece):
    def __init__(self, game,  color, square):
        super().__init__(game, 'rook', color, square)
        self.hasMoved = False

    def availSquares(self, getSquaresAttacking=False, board=None):
        if not board:
            board = self.game.board.board

        validSquares = range(8)
        squares = []
        stop = [True, True, True, True]
        for i in range(1, 8):
            
            testSquares = [(self.square[0], self.square[1] + i), (self.square[0], self.square[1] - i), (self.square[0] + i, self.square[1]), (self.square[0] - i, self.square[1])]
            for x in range(4):
                if stop[x]:
                    if testSquares[x][0] in validSquares and testSquares[x][1] in validSquares:
                        onSquare = board[testSquares[x][0]][testSquares[x][1]]
                        if onSquare == 0:
                            squares.append(testSquares[x])
                            continue
                        stop[x] = False
                        if onSquare.color != self.color:
                            squares.append(testSquares[x])
                        if getSquaresAttacking:
                            if onSquare.color == self.color:
                                squares.append(testSquares[x])

        returnSquares = []
        for square in squares:
            if not self.seeIfCheck(square):
                returnSquares.append(square)
        return returnSquares

class Bishop(Piece):
    def __init__(self, game,  color, square):
        super().__init__(game, 'bishop', color, square)

    def availSquares(self, getSquaresAttacking=False, board=None):
        if not board:
            board = self.game.board.board

        validSquares = range(8)
        squares = []
        stop = [True, True, True, True]
        for i in range(1, 8):
            
            testSquares = [(self.square[0] + i, self.square[1] + i), (self.square[0] - i, self.square[1] + i), (self.square[0] + i, self.square[1] - i), (self.square[0] - i, self.square[1] - i)]
            for x in range(4):
                if stop[x]:
                    if testSquares[x][0] in validSquares and testSquares[x][1] in validSquares:
                        onSquare = board[testSquares[x][0]][testSquares[x][1]]
                        if onSquare == 0:
                            squares.append(testSquares[x])
                            continue
                        stop[x] = False
                        if onSquare.color != self.color:
                            squares.append(testSquares[x])
                        if getSquaresAttacking:
                            if onSquare.color == self.color:
                                squares.append(testSquares[x])

        returnSquares = []
        for square in squares:
            if not self.seeIfCheck(square):
                returnSquares.append(square)
        return returnSquares

class Queen(Piece):
    def __init__(self, game,  color, square):
        super().__init__(game, 'queen', color, square)

    def availSquares(self, getSquaresAttacking=False, board=None):
        if not board:
            board = self.game.board.board

        validSquares = range(8)
        squares = []

        # Diagonals
        stop = [True, True, True, True]
        for i in range(1, 8):
            
            testSquares = [(self.square[0] + i, self.square[1] + i), (self.square[0] - i, self.square[1] + i), (self.square[0] + i, self.square[1] - i), (self.square[0] - i, self.square[1] - i)]
            for x in range(4):
                if stop[x]:
                    if testSquares[x][0] in validSquares and testSquares[x][1] in validSquares:
                        onSquare = board[testSquares[x][0]][testSquares[x][1]]
                        if onSquare == 0:
                            squares.append(testSquares[x])
                            continue
                        stop[x] = False
                        if onSquare.color != self.color:
                            squares.append(testSquares[x])
                        if getSquaresAttacking:
                            if onSquare.color == self.color:
                                squares.append(testSquares[x])

        # straights
                            
        stop = [True, True, True, True]
        for i in range(1, 8):
            
            testSquares = [(self.square[0], self.square[1] + i), (self.square[0], self.square[1] - i), (self.square[0] + i, self.square[1]), (self.square[0] - i, self.square[1])]
            for x in range(4):
                if stop[x]:
                    if testSquares[x][0] in validSquares and testSquares[x][1] in validSquares:
                        onSquare = board[testSquares[x][0]][testSquares[x][1]]
                        if onSquare == 0:
                            squares.append(testSquares[x])
                            continue
                        stop[x] = False
                        if onSquare.color != self.color:
                            squares.append(testSquares[x])
                        if getSquaresAttacking:
                            if onSquare.color == self.color:
                                squares.append(testSquares[x])

        returnSquares = []
        for square in squares:
            if not self.seeIfCheck(square):
                returnSquares.append(square)
        return returnSquares

class Knight(Piece):
    def __init__(self, game,  color, square):
        super().__init__(game, 'knight', color, square)

    def availSquares(self, getSquaresAttacking=False, board=None):
        squares = []
        returnSquares = []
        validSquares = range(8)
        for offset in KNIGHT_OFFSETS:
            square = (self.square[0] + offset[0], self.square[1] + offset[1])
            if square[0] in validSquares and square[1] in validSquares:
                onSquare = self.game.board.board[square[0]][square[1]]
                if onSquare == 0 or onSquare.color != self.color or getSquaresAttacking:
                    squares.append(square)

        for square in squares:
            if not self.seeIfCheck(square):
                returnSquares.append(square)
        return returnSquares

class Pawn(Piece):
    def __init__(self, game,  color, square):
        super().__init__(game, 'pawn', color, square)

        self.direction = -1
        self.startingRow = 6
        self.backrow = 0
        if color == 'black':
            self.direction = 1
            self.backrow = 7
            self.startingRow = 1
        self.previosRow = self.startingRow

    def moved(self):
        if self.square[0] == self.backrow:
            self.game.pieces.append(Queen(self.game, self.color, self.square))
            self.game.pieces.remove(self)

        if self.square == self.game.enPassantDummy[0]:
            self.game.pieces.remove(self.game.enPassantDummy[1])

        if self.previosRow == self.startingRow == self.square[0] - 2 * self.direction:
            self.game.enPassantDummy = [(self.square[0] - self.direction, self.square[1]), self, 1]
        
        self.previosRow = self.square[0]

    def availSquares(self):
        squares = []
        nextRow = self.square[0] + self.direction
        if self.game.board.board[nextRow][self.square[1]] == 0:
            squares.append((nextRow, self.square[1]))

            if nextRow - self.direction == self.startingRow and self.game.board.board[nextRow + self.direction][self.square[1]] == 0:
                squares.append((nextRow + self.direction, self.square[1]))

        for col in [self.square[1] - 1, self.square[1] + 1]:
            if not col in range(8):
                continue

            onSquare = self.game.board.board[nextRow][col]
            if onSquare != 0 and onSquare.color != self.color:
                squares.append((nextRow, col))
            if (nextRow, col) == self.game.enPassantDummy[0]:
                squares.append((nextRow, col))

        returnSquares = []
        for square in squares:
            if not self.seeIfCheck(square):
                returnSquares.append(square)
        return returnSquares
    
    def squaresAttacking(self):
        squares = []
        for col in [self.square[1] - 1, self.square[1] + 1]:
            if col in range(8):
                squares.append((self.square[0] + self.direction, col))
        return squares

class King(Piece):
    def __init__(self, game,  color, square):
        super().__init__(game, 'king', color, square)
        self.hasMoved = False

    def availSquares(self, getSquaresAttacking=False):
        squares = []
        validSquares = range(8)
        for offset in KING_OFFSETS:
            square = (self.square[0] + offset[0], self.square[1] + offset[1])
            if square[0] in validSquares and square[1] in validSquares:
                onSquare = self.game.board.board[square[0]][square[1]]
                if onSquare == 0 or onSquare.color != self.color or getSquaresAttacking:
                    if not self.isAttacked(square, board=self.removeSelfFromBoard()) or getSquaresAttacking:
                        squares.append(square)
        
        castleSquares = self.canCastle()
        if castleSquares: squares += castleSquares
            
        return squares
    
    def canCastle(self):
        castleSquares = []

        if self.hasMoved or self.isAttacked(): return False
        rooks = []
        for piece in self.game.pieces:
            if type(piece) == Rook and piece.color == self.color and not piece.hasMoved:
                rooks.append(piece)
        if len(rooks) == 0: return False

        row = self.square[0]
        for rook in rooks:
            if rook.square[1] == 7:      # kingside rook
                can = True
                for square in [(row, 5), (row, 6)]:
                    if self.game.board.board[row][square[1]] != 0 or self.isAttacked(square=square):
                        can = False
                if can: 
                    castleSquares += [(row, 6), (row, 7)]
                    self.game.castleSquares[(row, 6)] = {'king': (row, 6), 'rook': (row, 5), 'corner': (row, 7)}
                    self.game.castleSquares[(row, 7)] = {'king': (row, 6), 'rook': (row, 5), 'corner': (row, 7)}

            if rook.square[1] == 0:      # queenside rook
                KingSquares = [(row, 2), (row, 3)]
                emptySquares = [(row, 1), (row, 2), (row, 3)]
                can = True
                for square in emptySquares:
                    if self.game.board.board[row][square[1]] != 0:
                        can = False
                for square in KingSquares:
                    if self.isAttacked(square=square):
                        can = False
                if can: 
                    castleSquares += [(row, 0), (row, 2)]
                    self.game.castleSquares[(row, 0)] = {'king': (row, 2), 'rook': (row, 3), 'corner': (row, 0)}
                    self.game.castleSquares[(row, 2)] = {'king': (row, 2), 'rook': (row, 3), 'corner': (row, 0)}
                    
        return castleSquares
    
    def squaresAttacking(self):
        squares = []
        for x in KING_OFFSETS:
            squares.append((self.square[0] + x[0], self.square[1] + x[1]))
        return squares