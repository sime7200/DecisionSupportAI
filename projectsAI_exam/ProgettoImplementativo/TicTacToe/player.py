import random
import math

class Player():
    def __init__(self, symbol):
        self.symbol = symbol

    def getMove(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def moveHum(self, game):
        validCell = False
        val = None
        while not validCell:
            cell = input("Turno di " + self.symbol + ". Casella: ")
            try:
                val = int(cell)
                if val not in game.availableMoves():
                    raise ValueError
                validCell = True
            except ValueError:
                print("Non valid cell!")
        return val




class AIPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    # fa una mossa casuale se fa la prima mossa, altrimenti minimax
    def moveAI(self, game):
        if len(game.availableMoves()) == 9:
            cell = random.choice(game.availableMoves())
        else: 
            cell = self.minimax(game, self.symbol)['position']
        return cell
    
    def minimax(self, state, player):
        max_player = self.symbol  # io
        other_player = 'O' if player == 'X' else 'X'

        # caso base
        # controllo se la mossa precedente era la mossa vincente
        if state.current_winner == other_player:
            # calcolo del punteggio migliore a seconda del giocatore massimizzante o minimizzante
            return {'position': None, 'score': 1 * (state.numEmptyCells() + 1) if other_player == max_player else -1 * (
                        state.numEmptyCells() + 1)}
        elif not state.emptyCells():
            return {'position': None, 'score': 0}
        
        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # each score should maximize
        else:
            best = {'position': None, 'score': math.inf}  # each score should minimize
        
        for possibleMove in state.availableMoves():
            state.makeMove(possibleMove, player)
            simulatedScore = self.minimax(state, other_player)

            # portiamo il tabellone alla condizione iniziale dopo la simulazione
            state.board[possibleMove] = ' '
            state.current_winner = None
            simulatedScore['position'] = possibleMove  # this represents the move optimal next move 
            if player == max_player:  # X is max player
                if simulatedScore['score'] > best['score']:
                    best = simulatedScore
            else:
                if simulatedScore['score'] < best['score']:
                    best = simulatedScore
        return best