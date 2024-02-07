import pygame, sys, os
from board import Board
from pieces import *

LIGHT = (204, 183, 174)
DARK = (112, 102, 119)

SCREENSIZE = (800, 800)
BOARDSIZE = 800
SQUARESIZE = BOARDSIZE // 8

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Chess God")
        self.screen = pygame.display.set_mode(SCREENSIZE)

        self.boardSize = BOARDSIZE
        self.squareSize = SQUARESIZE
        self.light = LIGHT
        self.dark = DARK
        self.players = ['white', 'black']
        self.renderOffset = self.squareSize / 8

        self.images = {'white': {}, 'black': {}}
        for name in os.listdir('assets/piece_images/'):
            img = pygame.transform.scale(pygame.image.load('assets/piece_images/' + name), (SQUARESIZE * 0.8, SQUARESIZE * 0.8))
            #img.set_colorkey((255, 255, 255))
            color, piece = name.split('_')
            self.images[color][piece[:-4]] = img
        self.selectedDot = pygame.transform.scale(pygame.image.load('assets/selected.png'), (SQUARESIZE, SQUARESIZE))
        self.selectedDot.set_colorkey((255, 255, 255))
        self.selectedCorners = pygame.transform.scale(pygame.image.load('assets/piece_selected.png'), (SQUARESIZE, SQUARESIZE))
        self.selectedCorners.set_colorkey((255, 255, 255))

        self.pieces = []
        self.kings = {}
        self.board = Board(self)
        self.enPassantDummy = [None, None, 0]
        self.castleSquares = {}

        self.clock = pygame.time.Clock()

        self.pieceSelected = None
        self.deselected = False
        self.activePlayer = 'white'

    def changeTurn(self):
        current = self.players.index(self.activePlayer)
        self.activePlayer = self.players[1 - current]

        self.enPassantDummy[2] -= 1
        if self.enPassantDummy[2] == 0:
            self.enPassantDummy = [None, None, 0]

        if type(self.pieceSelected) == Pawn:
            self.pieceSelected.moved()
        elif type(self.pieceSelected) == Rook:
            self.pieceSelected.hasMoved = True
        elif type(self.pieceSelected) == King:
            self.pieceSelected.hasMoved = True

            if self.pieceSelected.square in self.castleSquares:
                self.pieceSelected.square = self.castleSquares[self.pieceSelected.square]['king']
                corner = self.castleSquares[self.pieceSelected.square]['corner']
                self.board.board[corner[0]][corner[1]].square = self.castleSquares[self.pieceSelected.square]['rook']
            self.castleSquares = {}

        self.board.generateArray()

        gameOver = self.gameOver()
        if gameOver: print(gameOver)
    
    def gameOver(self):
        for piece in self.pieces:
            if piece.color == self.activePlayer:
                if piece.availSquares() != []:
                    return False
        if self.kings[self.activePlayer].isAttacked():
            return 'Checkmate'
        else:
            return 'Stalemate'  

    def run(self):
        while True:
            self.screen.blit(self.board.emptyBoard, (0, 0))
            mpos = pygame.mouse.get_pos()
            mouseSquare = (mpos[1] // SQUARESIZE, mpos[0] // SQUARESIZE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        onSquare = self.board.board[mouseSquare[0]][mouseSquare[1]]

                        if onSquare == self.pieceSelected:
                            self.pieceSelected.isPickedUp = True
                            self.deselected = True

                        elif onSquare != 0 and onSquare.color == self.activePlayer:
                            if not mouseSquare in self.castleSquares:
                                self.pieceSelected = onSquare
                                self.pieceSelected.isPickedUp = True
                            else:   # if king is selected and the rook is clicked to castle
                                self.pieceSelected.square = mouseSquare
                                self.changeTurn()
                                self.pieceSelected = None

                        elif self.pieceSelected:
                            if not mouseSquare in self.pieceSelected.availSquares():
                                self.pieceSelected = None
                            else:
                                self.pieceSelected.square = mouseSquare

                                if onSquare != 0:
                                    self.pieces.remove(onSquare)

                                self.changeTurn()

                                self.pieceSelected = None

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.deselected:
                            self.deselected = False
                            self.pieceSelected.isPickedUp = False
                            self.pieceSelected = None

                        if self.pieceSelected:
                            self.pieceSelected.isPickedUp = False

                            if mouseSquare in self.pieceSelected.availSquares():
                                onSquare = self.board.board[mouseSquare[0]][mouseSquare[1]]
                                
                                if onSquare != 0:
                                    if onSquare.color != self.activePlayer:
                                        self.pieceSelected.square = mouseSquare
                                        self.pieces.remove(onSquare)
                                        self.changeTurn()
                                    elif mouseSquare in self.castleSquares:
                                        self.pieceSelected.square = mouseSquare
                                        self.changeTurn()

                                else:
                                    self.pieceSelected.square = mouseSquare
                                    self.changeTurn()

                                self.pieceSelected = None
                            elif self.pieceSelected.square != mouseSquare:
                                self.pieceSelected = None

            for piece in self.pieces:
                piece.render(self.screen, mpos)
            
            if self.pieceSelected:
                self.pieceSelected.render(self.screen, mpos)

                availSquares = self.pieceSelected.availSquares()
                for square in availSquares:
                    img = self.selectedDot
                    if self.board.board[square[0]][square[1]] != 0: img = self.selectedCorners
                    self.screen.blit(img, (square[1] * self.squareSize, square[0] * self.squareSize, self.squareSize, self.squareSize))

            self.board.generateArray()

            self.clock.tick(60)
            pygame.display.update()

Game().run()