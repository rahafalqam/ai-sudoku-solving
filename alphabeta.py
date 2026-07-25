"""
Alpha-Beta Pruning Algorithm - Complete standalone implementation
"""
import math

class AlphaBetaPruning:
    """Alpha-Beta Pruning implementation"""
    
    def __init__(self):
        self.nodes_evaluated = 0
    
    def alphabeta(self, node, depth, alpha, beta, maximizing_player, game_tree):
        """Alpha-Beta pruning algorithm"""
        self.nodes_evaluated += 1
        
        # Check if node is terminal or depth limit reached
        if depth == 0 or node not in game_tree:
            return self.evaluate(node)
        
        if maximizing_player:
            value = -math.inf
            for child in game_tree[node]:
                value = max(value, self.alphabeta(child, depth - 1, alpha, beta, False, game_tree))
                alpha = max(alpha, value)
                if alpha >= beta:
                    print(f"Beta cutoff at node {node} -> alpha={alpha}, beta={beta}")
                    break  # Beta cutoff
            return value
        else:
            value = math.inf
            for child in game_tree[node]:
                value = min(value, self.alphabeta(child, depth - 1, alpha, beta, True, game_tree))
                beta = min(beta, value)
                if alpha >= beta:
                    print(f"Alpha cutoff at node {node} -> alpha={alpha}, beta={beta}")
                    break  # Alpha cutoff
            return value
    
    def evaluate(self, node):
        """Evaluation function for terminal nodes"""
        # In a real game, this would be a proper evaluation function
        # For this example, we'll use predefined values
        values = {
            'D1': 3, 'D2': 5, 'D3': 6, 'D4': 9, 'D5': 1, 'D6': 2, 'D7': 0, 'D8': -1,
            'E1': 3, 'E2': 5, 'E3': 6, 'E4': 9, 'E5': 1, 'E6': 2, 'E7': 0, 'E8': -1,
            'F1': 3, 'F2': 5, 'F3': 6, 'F4': 9, 'F5': 1, 'F6': 2, 'F7': 0, 'F8': -1,
            'G1': 3, 'G2': 5, 'G3': 6, 'G4': 9, 'G5': 1, 'G6': 2, 'G7': 0, 'G8': -1
        }
        return values.get(node, 0)
    
    def print_game_tree(self, game_tree):
        """Print the game tree structure"""
        print("Game Tree Structure:")
        for node, children in game_tree.items():
            print(f"{node} -> {children}")

def alpha_beta_example():
    """Alpha-Beta Pruning example with detailed explanation"""
    print("=== Alpha-Beta Pruning Algorithm ===")
    
    # Create a more complex game tree for demonstration
    game_tree = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F', 'G'],
        'D': ['D1', 'D2', 'D3', 'D4'],
        'E': ['E1', 'E2', 'E3', 'E4'],
        'F': ['F1', 'F2', 'F3', 'F4'],
        'G': ['G1', 'G2', 'G3', 'G4']
    }
    
    # Terminal node values
    terminal_values = {
        'D1': 3, 'D2': 12, 'D3': 8, 'D4': 2,
        'E1': 4, 'E2': 6, 'E3': 14, 'E4': 5,
        'F1': 2, 'F2': 1, 'F3': 5, 'F4': 4,
        'G1': 9, 'G2': 3, 'G3': 2, 'G4': 7
    }
    
    ab = AlphaBetaPruning()
    
    # Override evaluate function for this example
    original_evaluate = ab.evaluate
    ab.evaluate = lambda node: terminal_values.get(node, 0)
    
    print("Game Tree with terminal values:")
    for node, children in game_tree.items():
        if node in ['D', 'E', 'F', 'G']:
            child_values = [f"{child}({terminal_values[child]})" for child in children]
            print(f"{node} -> {child_values}")
        else:
            print(f"{node} -> {children}")
    
    print("\nRunning Alpha-Beta Pruning...")
    
    # Run Alpha-Beta pruning
    result = ab.alphabeta('A', 3, -math.inf, math.inf, True, game_tree)
    
    print(f"\nAlpha-Beta Result: {result}")
    print(f"Nodes evaluated: {ab.nodes_evaluated}")
    
    # Compare with MiniMax
    print("\n" + "="*50)
    print("Comparison with MiniMax:")
    
    class MiniMaxComparison:
        def __init__(self):
            self.nodes_evaluated = 0
        
        def minimax(self, node, depth, maximizing_player, game_tree):
            self.nodes_evaluated += 1
            
            if depth == 0 or node not in game_tree:
                return terminal_values.get(node, 0)
            
            if maximizing_player:
                value = -math.inf
                for child in game_tree[node]:
                    value = max(value, self.minimax(child, depth - 1, False, game_tree))
                return value
            else:
                value = math.inf
                for child in game_tree[node]:
                    value = min(value, self.minimax(child, depth - 1, True, game_tree))
                return value
    
    mm = MiniMaxComparison()
    mm_result = mm.minimax('A', 3, True, game_tree)
    
    print(f"MiniMax Result: {mm_result}")
    print(f"MiniMax nodes evaluated: {mm.nodes_evaluated}")
    print(f"Alpha-Beta pruning efficiency: {mm.nodes_evaluated - ab.nodes_evaluated} nodes saved")

def alpha_beta_visualization():
    """Visualize Alpha-Beta pruning with a simpler example"""
    print("\n" + "="*50)
    print("Alpha-Beta Pruning Visualization")
    
    # Simple game tree for visualization
    simple_tree = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F', 'G'],
        'D': [3, 12],
        'E': [8, 2],
        'F': [4, 6],
        'G': [14, 5]
    }
    
    ab = AlphaBetaPruning()
    
    print("\nSimple Game Tree:")
    for node, children in simple_tree.items():
        if node in ['D', 'E', 'F', 'G']:
            print(f"{node} -> {children}")
        else:
            print(f"{node} -> {children}")
    
    print("\nAlpha-Beta execution trace:")
    result = ab.alphabeta('A', 3, -math.inf, math.inf, True, simple_tree)
    
    print(f"\nFinal result: {result}")
    print(f"Total nodes evaluated: {ab.nodes_evaluated}")

if __name__ == "_main_":
    alpha_beta_example()
    alpha_beta_visualization()