"""
MiniMax Algorithm for Game Playing - Complete standalone implementation
"""
import math
import random

class TicTacToe:
    """Tic-Tac-Toe game for MiniMax demonstration"""
    
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
    
    def print_board(self):
        """Print the current board state"""
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
    
    def available_moves(self):
        """Get all available moves"""
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def empty_squares(self):
        """Check if there are empty squares"""
        return ' ' in self.board
    
    def num_empty_squares(self):
        """Count empty squares"""
        return self.board.count(' ')
    
    def make_move(self, square, letter):
        """Make a move on the board"""
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square, letter):
        """Check if the current move wins the game"""
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        
        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # Top-left to bottom-right
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]  # Top-right to bottom-left
            if all([spot == letter for spot in diagonal2]):
                return True
        
        return False

class MiniMaxPlayer:
    """MiniMax algorithm implementation"""
    
    def __init__(self, letter):
        self.letter = letter
    
    def get_move(self, game):
        """Get the best move using MiniMax"""
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())  # Random first move
        else:
            square = self.minimax(game, self.letter)['position']
        return square
    
    def minimax(self, state, player):
        """MiniMax algorithm implementation"""
        max_player = self.letter  # Yourself
        other_player = 'O' if player == 'X' else 'X'
        
        # First check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None, 
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player 
                            else -1 * (state.num_empty_squares() + 1)}
        
        elif not state.empty_squares():  # No empty squares
            return {'position': None, 'score': 0}
        
        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # Each score should maximize
        else:
            best = {'position': None, 'score': math.inf}   # Each score should minimize
        
        for possible_move in state.available_moves():
            # Step 1: make a move, try that spot
            state.make_move(possible_move, player)
            
            # Step 2: recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player)  # Alternate players
            
            # Step 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # This represents the move optimal next move
            
            # Step 4: update the dictionaries if necessary
            if player == max_player:  # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:  # O is min player
                if sim_score['score'] < best['score']:
                    best = sim_score
        
        return best

def play_tic_tac_toe():
    """Play a game of Tic-Tac-Toe with MiniMax"""
    print("=== MiniMax Algorithm - Tic Tac Toe ===")
    
    # Create game and players
    game = TicTacToe()
    human_player = 'X'
    ai_player = MiniMaxPlayer('O')
    
    print("You are X, AI is O")
    game.print_board()
    
    while game.empty_squares():
        # Human move
        if human_player == 'X':
            try:
                square = int(input("Enter your move (0-8): "))
                if square not in game.available_moves():
                    print("Invalid move! Try again.")
                    continue
            except ValueError:
                print("Please enter a number!")
                continue
            
            game.make_move(square, human_player)
        
        # AI move
        else:
            print("AI is thinking...")
            square = ai_player.get_move(game)
            game.make_move(square, ai_player.letter)
            print(f"AI plays at position {square}")
        
        game.print_board()
        print()
        
        # Check for winner
        if game.current_winner:
            if game.current_winner == human_player:
                print("You win! 🎉")
            else:
                print("AI wins! 🤖")
            break
        
        # Switch players
        human_player, ai_player.letter = ai_player.letter, human_player
    
    if not game.current_winner:
        print("It's a tie! 😐")

def minimax_example():
    """Simple MiniMax example with game tree"""
    print("\n=== MiniMax Game Tree Example ===")
    
    # Simple game tree for demonstration
    game_tree = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F', 'G'],
        'D': [3, 5],
        'E': [6, 9],
        'F': [1, 2],
        'G': [7, 8]
    }
    
    def minimax(node, depth, is_maximizing):
        """Recursive MiniMax function"""
        if node in [3, 5, 6, 9, 1, 2, 7, 8]:  # Terminal nodes
            return node
        
        if is_maximizing:
            best_value = -math.inf
            for child in game_tree[node]:
                value = minimax(child, depth + 1, False)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = math.inf
            for child in game_tree[node]:
                value = minimax(child, depth + 1, True)
                best_value = min(best_value, value)
            return best_value
    
    # Calculate MiniMax value for root
    root_value = minimax('A', 0, True)
    print(f"MiniMax value for root node A: {root_value}")
    
    # Show the game tree
    print("\nGame Tree:")
    for node, children in game_tree.items():
        print(f"{node} -> {children}")

if __name__ == "_main_":
    minimax_example()
    print("\n" + "="*50)
    # Uncomment to play Tic-Tac-Toe
    # play_tic_tac_toe()