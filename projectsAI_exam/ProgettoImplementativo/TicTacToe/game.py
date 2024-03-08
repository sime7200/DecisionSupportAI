import math
import time
from player import HumanPlayer, AIPlayer

class TicTacToe():
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None


    @staticmethod
    def make_board():
        return [' ' for _ in range(9)]


    def printBoard(self):
        for row in [self.board[i*3:(i+1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')


    @staticmethod
    def boardNums():  
        print("Available cells")  
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |') # dentro row ho i numeri e aggiungo separatore


    # cell -> numero della cella [0..9]. symbol -> O,X
    # se possibile fa la mossa. False se non se cella occupata
    def makeMove(self, cell, symbol):
        if(self.board[cell] == ' '):
            self.board[cell] = symbol
            if self.winner(cell, symbol):
                self.current_winner = symbol
            return True
        return False
        

    def winner(self, cell, symbol):
        rowIndex = math.floor(cell/3)
        row = self.board[rowIndex*3:(rowIndex+1)*3] #row va dal primo valore della riga all'ultimo: 0->2, 3->5, 6->8
        # se nella riga ci sono tutti simboli uguali
        if all([s == symbol for s in row]):
            return True
        colIndex = cell % 3
        column = [self.board[colIndex+i*3] for i in range(3)]
        # o cosi forse column = self.board[colIndex:(3*2)+colIndex] ------------------------------------------
        if all([s == symbol for s in column]):
            return True
        #se la vincita si trova in una delle 2 diagonali
        if cell % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == symbol for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == symbol for s in diagonal2]):
                return True
        return False
    

    # restiturisce True se ci sono celle vuote 
    def emptyCells(self):
        return ' ' in self.board


    # restituisce una lista di indici i delle celle vuote
    def availableMoves(self):
        return [i for i, x in enumerate(self.board) if x == " "]
    

    def is_game_over(self, state):
        # Controlla se c'è un vincitore
        if state.current_winner is not None:
            return True
        # Controlla se non ci sono più mosse disponibili
        if not state.emptyCells():
            return True
        return False



def play(game, xPlayer, oPlayer, printGame=True):
    if printGame:
        game.boardNums()
    
    symbol = 'X'
    while game.emptyCells():
        if symbol == 'O':
            cell = oPlayer.moveHum(game)
        else:
            cell = xPlayer.moveAI(game)
        if game.makeMove(cell, symbol):
            if printGame:
                print(symbol + ' aggiunta nella cella {}'.format(cell))
                game.printBoard()
                print('')
            if game.current_winner:
                if printGame:
                    print(symbol + ' vince!')
                return symbol  # fine while
            symbol = 'O' if symbol == 'X' else 'X'  # cambio player
        time.sleep(1)
    if printGame:
        print('Pareggio!')




if __name__ == '__main__':
    xPlayer = AIPlayer('X')
    oPlayer = HumanPlayer('O')
    t = TicTacToe()
    play(t, xPlayer, oPlayer, printGame=True)