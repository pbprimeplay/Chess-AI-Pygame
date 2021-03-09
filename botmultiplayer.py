import chess
import pygame
from tkinter import *
import random
from tkinter import messagebox
from stockfish import Stockfish
stockfish = Stockfish(r'stockfish_13_win_x64_bmi2\stockfish_13_win_x64_bmi2.exe')

pygame.init()
FPS = 60
clock = pygame.time.Clock()

board = chess.Board()
checkmate = pygame.USEREVENT
draw = pygame.USEREVENT + 1

#Game Class
class Game():
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 800
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp','bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]

        self.RESTARTBOARD = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp','bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
            
         ]
         
        self.whiteToMove = True
        self.moveLog = []
        self.images = {}
        self.pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
        self.size = self.HEIGHT // 8
        self.WHITE = (255, 255, 255)
        self.BLACK = (235, 235, 208)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_icon(pygame.image.load("Images/icon.png"))
        pygame.display.set_caption("ChessPoint")

        self.sqSelected = ()
        self.playerClicks = []

        self.possible_moves = []

        self.ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
        self.rowsToRanks = {v: k for k, v in self.ranksToRows.items()}

        self.filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
        self.colsToFiles = {v: k for k, v in self.filesToCols.items()}

        self.move_opt = pygame.transform.scale(pygame.image.load('Images/move_opt.png'), (50,55))
        self.highlight_pos = []
        self.isWhite = random.choice([True, False])
        self.checkTo = False
        if self.isWhite!=True:
            self.flip()

        self.bestMoves = []

    def flip(self):
        # for x in self.board:
        #     x.reverse()
        # self.board.reverse()
        pass

    def pawnPromotion(self):
        piece_name = ""
        
        root = Tk()
        root.title("Promote Pawn")
        root.geometry("325x120")
        root.resizable(False, False)
        root.iconbitmap("Images/icon.ico")
        queen = PhotoImage(file = "Images/pieces/wQ.png")
        rook = PhotoImage(file = "Images/pieces/wR.png")
        bishop = PhotoImage(file = "Images/pieces/wB.png")
        knight = PhotoImage(file = "Images/pieces/wN.png")
        Button(root, image=queen, command=lambda: getPromotedPiece('Q')).place(x=10, y=10)
        Button(root, image=rook, command=lambda: getPromotedPiece('R')).place(x=90, y=10)
        Button(root, image=bishop, command=lambda: getPromotedPiece('B')).place(x=170, y=10)
        Button(root, image=knight, command=lambda: getPromotedPiece('N')).place(x=250, y=10)
        Label(root, text="Pick a piece to promote").place(x=100, y=90)

        def getPromotedPiece(name):
            name = piece_name

        root.mainloop()

        return piece_name

    def move(self, startSq, endSq):
        try:
            self.startRow = startSq[0]
            self.startCol = startSq[1]
            self.endRow = endSq[0]
            self.endCol = endSq[1]
            # print(self.startRow, self.startCol)
            self.cm = self.board[self.startRow][self.startCol]
            self.notation = self.convertToNotation(self.startRow, self.startCol) + self.convertToNotation(self.endRow, self.endCol)
            
            self.pm = self.board[self.startRow][self.startCol]

            if self.whiteToMove == True and self.pm[0] == 'w':
                board.push_san(self.notation)
                self.moveLog.append(self.notation)
                stockfish.set_position(self.moveLog)
                self.board[self.startRow][self.startCol] = '--'
                self.board[self.endRow][self.endCol] = self.pm
                    
                if 'e1g1' == self.notation:
                    self.board[7][7] = '--'
                    self.board[7][5] = 'wR'

                elif 'e1c1' == self.notation:
                    self.board[7][0] = '--'
                    self.board[7][3] = 'wR'
                
                self.whiteToMove = False

            if self.whiteToMove == False and self.cm[0] == 'b':
                board.push_san(self.notation)
                self.moveLog.append(self.notation)
                stockfish.set_position(self.moveLog)
                
                self.board[self.startRow][self.startCol] = '--'
                self.board[self.endRow][self.endCol] = self.cm

                if 'e8g8' == self.notation:
                    self.board[0][7] = '--'
                    self.board[0][5] = 'bR'

                elif 'e8c8' == self.notation:
                    self.board[0][0] = '--'
                    self.board[0][3] = 'bR'

                self.whiteToMove = True

            else:
                self.sqSelected = ()
                self.playerClicks = []

            if board.is_checkmate():
                pygame.event.post(pygame.event.Event(checkmate))

            if board.can_claim_draw():
                pygame.event.post(pygame.event.Event(draw))

            if board.is_check():
                if len(self.moveLog)%2 == 0:
                    self.checkTo = 'w'

                else:
                    self.checkTo = 'b'
                
            self.highlight_pos = []
            
        except:
            self.sqSelected = ()
            self.playerClicks = []
            self.highlight_pos = []
            print("Invalid Move")


    def convertToNotation(self, r, c):
        return str(self.colsToFiles[c]) + str(self.rowsToRanks[r])

    def convertToNums(self, f, r):
        return (self.filesToCols[f]), (self.ranksToRows[r])

    def getChessNotation(self):
        return self.colsToFiles[self.startCol] + self.rowsToRanks[self.startRow] + self.colsToFiles[self.endCol] + self.rowsToRanks[self.endRow]
        
    def loadimages(self):
      for piece in self.pieces:
          self.images[piece] = pygame.transform.scale(pygame.image.load("Images/pieces/" + piece + ".png").convert_alpha(), (self.size, self.size))

    def draw(self):
        boardLength = 8
        self.screen.fill(self.WHITE)

        cnt = 0
        for i in range(boardLength):
            for z in range(boardLength):
                #check if current loop value is even
                if cnt % 2 == 0:
                    pygame.draw.rect(self.screen, self.WHITE,[self.size*z,self.size*i,self.size,self.size])
                else:
                    pygame.draw.rect(self.screen, self.BLACK, [self.size*z,self.size*i,self.size,self.size])
                cnt +=1
            cnt-=1
        pygame.draw.rect(self.screen, self.BLACK, [self.size, self.size, z*self.size, z*self.size],1)

        for r in range(8):
            for c in range(8):
                self.chess_piece = self.board[r][c]

                if self.checkTo != False:
                    self.red_surface = pygame.Surface((self.size, self.size))
                    self.red_surface.set_alpha(180)
                    self.red_surface.fill(pygame.Color('red'))

                    if self.checkTo == 'w':
                        if self.chess_piece == 'wK':
                            self.screen.blit(self.red_surface, (c*self.size, r*self.size))

                    elif self.checkTo == 'b':
                        if self.chess_piece == 'bK':
                            self.screen.blit(self.red_surface, (c*self.size, r*self.size))
                            
                if self.chess_piece != '--':
                    self.screen.blit(self.images[self.chess_piece], pygame.Rect(c*self.size, r*self.size, self.size,self.size))

                for x in range(len(self.highlight_pos)):
                    if str(c) + str(r) == str(self.highlight_pos[x][0]) + str(self.highlight_pos[x][1]):
                        self.screen.blit(self.move_opt, pygame.Rect(c*self.size + 20, r*self.size + 25, self.size,self.size))


game = Game()
game.loadimages()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            col = pos[0]//game.size
            row = pos[1]//game.size
            if game.sqSelected == (row, col):
                game.sqSelected = ()
                game.playerClicks = []
                game.highlight_pos = []

            else:
                game.sqSelected = (row, col)
                game.playerClicks.append(game.sqSelected)
                position = game.convertToNotation(game.playerClicks[0][0], game.playerClicks[0][1])

                game.possible_moves = []
                for i in list(board.legal_moves):
                    if str(i)[0] + str(i)[1] == position:
                        game.possible_moves.append(str(i)[2] + str(i)[3])

            if len(game.playerClicks) == 1:
                if game.whiteToMove:
                    for i in game.possible_moves:
                        if str(game.convertToNums(i[0], i[1]) == str(game.playerClicks[0][0]) + str(game.playerClicks[0][1])):
                            posit = game.convertToNums(i[0], i[1])
                            game.highlight_pos.append(posit)

            if len(game.playerClicks) == 2:
                if game.checkTo != False:
                    game.checkTo = False

                game.move(game.playerClicks[0], game.playerClicks[1])

                game.sqSelected = ()
                game.playerClicks = []
                if not(game.whiteToMove):
                    game.compMove = game.convertToNums(str(stockfish.get_best_move())[0], str(stockfish.get_best_move())[1]) + game.convertToNums(str(stockfish.get_best_move())[2], str(stockfish.get_best_move())[3])
                    game.bestMoves.append(((game.compMove[1], game.compMove[0]), (game.compMove[3], game.compMove[2])))
                    if len(game.bestMoves) == 1:
                        game.move((game.compMove[1], game.compMove[0]), (game.compMove[3], game.compMove[2]))
                        game.bestMoves = []

        elif event.type == checkmate:
            root = Tk()
            root.withdraw()
            mess = ""
            if game.whiteToMove:
                mess = "It's a checkmate! Black wins! Want to play again?"

            else:
                mess = "It's a checkmate! White wins! Want to play again?"

            game_over = messagebox.askyesno("Checkmate!", mess, icon='info')
            if game_over == 0:
                quit()

            else:
                game.board = game.RESTARTBOARD
                game.whiteToMove = True
                board.reset_board()
                game.checkTo = False

        elif event.type == draw:
            root = Tk()
            root.withdraw()
            game_over = messagebox.askyesno("Checkmate!", "Good game! It's a draw! Want to play again?", icon='info')
            if game_over == 0:
                quit()

            else:
                game.board = game.RESTARTBOARD
                game.whiteToMove = True
                board.reset_board()
                game.checkTo = False

           
    game.draw()
    clock.tick(FPS)
    pygame.display.flip()
