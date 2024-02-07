import pygame
from copy import deepcopy
from pieces import *

EMPTY_BOARD = [[0 for i in range(8)] for i in range(8)]

class Board():
    def __init__(self, game):
        self.game = game
        self.defaultBoard()
        self.generateArray()
        
        self.emptyBoard = pygame.Surface((self.game.boardSize, self.game.boardSize))
        self.emptyBoard.fill(self.game.dark)
        for row in range(8):
            for col in range(4):
                shift = 0
                if row % 2 == 1: shift = 1
                self.emptyBoard.fill(self.game.light, ((col * 2 + shift) * self.game.squareSize, row * self.game.squareSize, self.game.squareSize, self.game.squareSize))

    def generateArray(self):
        self.board = deepcopy(EMPTY_BOARD)

        for piece in self.game.pieces:
            s1, s2 = piece.square
            self.board[s1][s2] = piece

    def defaultBoard(self):
        colors = ['white', 'black']
        backRanks = [7, 0]
        pawnRanks = [6, 1]
        pieces = []
        for i in range(2):
            backRanks[i]
            pieces += [Rook(self.game, colors[i], (backRanks[i], 0)), Rook(self.game, colors[i], (backRanks[i], 7))]
            pieces += [Knight(self.game, colors[i], (backRanks[i], 1)), Knight(self.game, colors[i], (backRanks[i], 6))]
            pieces += [Bishop(self.game, colors[i], (backRanks[i], 2)), Bishop(self.game, colors[i], (backRanks[i], 5))]
            pieces += [Queen(self.game, colors[i], (backRanks[i], 3)), King(self.game, colors[i], (backRanks[i], 4))]
            self.game.kings[colors[i]] = pieces[-1]
            for col in range(8):
                pieces.append(Pawn(self.game, colors[i], (pawnRanks[i], col)))
        self.game.pieces = pieces