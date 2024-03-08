import random
import math

class Player():
    def __init__(self, symbol):
        self.symbol = symbol


class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def moveHum(self, game):
        validCell = False
        val = None
        while not validCell:
            cell = input("Turno di " + self.symbol + ". Inserire numero cella: ")
            try:
                val = int(cell)
                if val not in game.availableMoves():
                    raise ValueError
                validCell = True
            except ValueError:
                print("Cella non valida! Selezionare un'altra cella.")
        return val




class AIPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)


    # fa una mossa casuale se fa la prima mossa, altrimenti minimax
    def moveAI(self, game):
        if len(game.availableMoves()) == 9:
            cell = random.choice(game.availableMoves())
        else: 
            cell = self.minimax(game, self.symbol, 2)['position']
        return cell
    

    def minimax(self, state, player, depth):
        max_player = self.symbol
        other_player = 'O' if player == 'X' else 'X'
        # Caso base
        if depth == 0 or state.is_game_over(state):
            return {'position': None, 'score': self.evaluate(state)}
        if player == max_player:
            best = {'position': None, 'score': -math.inf}  
        else:
            best = {'position': None, 'score': math.inf} 
        for possibleMove in state.availableMoves():
            state.makeMove(possibleMove, player)
            simulatedScore = self.minimax(state, other_player, depth-1)
            # Ripristina lo stato del tabellone
            state.board[possibleMove] = ' '
            state.current_winner = None
            simulatedScore['position'] = possibleMove  # mossa ottimale successiva 
            if player == max_player:  
                if simulatedScore['score'] > best['score']:
                    best = simulatedScore
            else:
                if simulatedScore['score'] < best['score']:
                    best = simulatedScore
        
        return best

    


    def evaluate(self, state):
        max_player = self.symbol
        other_player = 'O' if max_player == 'X' else 'X'
        score = 0
        # Controllo delle linee orizzontali, verticali e diagonali
        lines = state.board[:]
        for i in range(3):
            # Orizzontali
            lines.append(''.join(state.board[i*3:i*3+3]))
            # Verticali
            lines.append(''.join(state.board[i::3]))
        # Diagonali
        lines.append(''.join(state.board[0::4]))
        lines.append(''.join(state.board[2:8:2]))
        # Funzione euristica di valutazione
        for line in lines:
            if line.count(max_player) == 3:
                score += 100
            elif line.count(max_player) == 2 and line.count(' ') == 1:
                score += 10
            elif line.count(max_player) == 1 and line.count(' ') == 2:
                score += 1
            elif line.count(other_player) == 3:
                score -= 100
            elif line.count(other_player) == 2 and line.count(' ') == 1:
                score -= 10
            elif line.count(other_player) == 1 and line.count(' ') == 2:
                score -= 1

        return score
