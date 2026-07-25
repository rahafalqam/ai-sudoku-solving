"""
CSP Backtracking Search with MRV, LCV, and Forward Checking
Complete standalone implementation
"""
import time
import random

class SudokuCSP:
    def __init__(self, size=9):
        self.size = size
        self.subgrid_size = int(size ** 0.5)
        self.grid = [[0] * size for _ in range(size)]
        self.nodes_explored = 0
        self.backtracks = 0
    
    def load_puzzle(self, puzzle):
        """Load a puzzle into the grid"""
        self.grid = [row[:] for row in puzzle]
    
    def is_valid_move(self, row, col, num):
        """Check if a number is valid in a cell"""
        # Check row
        if num in self.grid[row]:
            return False
        
        # Check column
        for i in range(self.size):
            if self.grid[i][col] == num:
                return False
        
        # Check subgrid
        start_row = self.subgrid_size * (row // self.subgrid_size)
        start_col = self.subgrid_size * (col // self.subgrid_size)
        
        for i in range(self.subgrid_size):
            for j in range(self.subgrid_size):
                if self.grid[start_row + i][start_col + j] == num:
                    return False
        return True
    
    def get_empty_cells(self):
        """Get all empty cell positions"""
        return [(i, j) for i in range(self.size) for j in range(self.size) 
                if self.grid[i][j] == 0]
    
    def get_legal_values(self, row, col):
        """Get all legal values for a cell"""
        return [num for num in range(1, self.size + 1) 
                if self.is_valid_move(row, col, num)]
    
    def select_variable_mrv(self, empty_cells):
        """MRV heuristic: select variable with fewest legal values"""
        min_legal_values = float('inf')
        best_cell = empty_cells[0]
        
        for cell in empty_cells:
            row, col = cell
            legal_values = self.get_legal_values(row, col)
            if len(legal_values) < min_legal_values:
                min_legal_values = len(legal_values)
                best_cell = cell
        
        return best_cell
    
    def order_values_lcv(self, row, col, empty_cells):
        """LCV heuristic: order values by least constraining first"""
        values = []
        legal_values = self.get_legal_values(row, col)
        
        for num in legal_values:
            # Count how many constraints this value imposes
            constraint_count = self.count_constraints(row, col, num, empty_cells)
            values.append((constraint_count, num))
        
        # Sort by least constraining first
        values.sort()
        return [num for _, num in values]
    
    def count_constraints(self, row, col, num, empty_cells):
        """Count how constraining a value is on neighbors"""
        count = 0
        
        # Temporarily assign the value
        original_value = self.grid[row][col]
        self.grid[row][col] = num
        
        # Count reduced legal values for empty neighbors
        for i, j in empty_cells:
            if (i, j) != (row, col) and self.affects_cell(row, col, i, j):
                original_legal = len(self.get_legal_values(i, j))
                # The value is already assigned, so we just check the current state
                count += (20 - original_legal)  # Heuristic measure
        
        # Restore original value
        self.grid[row][col] = original_value
        return count
    
    def affects_cell(self, row1, col1, row2, col2):
        """Check if cell1 affects cell2 (same row, column, or subgrid)"""
        return (row1 == row2 or col1 == col2 or 
                (row1 // self.subgrid_size == row2 // self.subgrid_size and 
                 col1 // self.subgrid_size == col2 // self.subgrid_size))
    
    def forward_checking(self, empty_cells):
        """Check if all empty cells have at least one legal value"""
        for row, col in empty_cells:
            if not self.get_legal_values(row, col):
                return False
        return True
    
    def solve_backtracking(self, use_mrv=True, use_lcv=True, use_forward_checking=True):
        """Main backtracking solver with heuristics"""
        self.nodes_explored = 0
        self.backtracks = 0
        empty_cells = self.get_empty_cells()
        
        start_time = time.time()
        success = self._backtrack(empty_cells, use_mrv, use_lcv, use_forward_checking)
        end_time = time.time()
        
        return {
            'success': success,
            'solution': self.grid if success else None,
            'runtime': end_time - start_time,
            'nodes_explored': self.nodes_explored,
            'backtracks': self.backtracks
        }
    
    def _backtrack(self, empty_cells, use_mrv, use_lcv, use_forward_checking):
        """Recursive backtracking function"""
        if not empty_cells:
            return True
        
        # Select variable
        if use_mrv and len(empty_cells) > 1:
            row, col = self.select_variable_mrv(empty_cells)
        else:
            row, col = empty_cells[0]
        
        empty_cells.remove((row, col))
        
        # Order values
        if use_lcv:
            values = self.order_values_lcv(row, col, empty_cells)
        else:
            values = self.get_legal_values(row, col)
            random.shuffle(values)
        
        for value in values:
            self.nodes_explored += 1
            
            if self.is_valid_move(row, col, value):
                original_value = self.grid[row][col]
                self.grid[row][col] = value
                
                # Forward checking
                if use_forward_checking:
                    if not self.forward_checking(empty_cells):
                        self.grid[row][col] = original_value
                        continue
                
                if self._backtrack(empty_cells, use_mrv, use_lcv, use_forward_checking):
                    return True
                
                # Backtrack
                self.grid[row][col] = original_value
                self.backtracks += 1
        
        empty_cells.append((row, col))
        return False
    
    def display(self):
        """Display the Sudoku grid"""
        for i in range(self.size):
            if i % self.subgrid_size == 0 and i != 0:
                print("-" * (self.size * 3 + self.subgrid_size))
            for j in range(self.size):
                if j % self.subgrid_size == 0 and j != 0:
                    print("|", end=" ")
                print(f"{self.grid[i][j]:2d}" if self.grid[i][j] != 0 else " .", end=" ")
            print()

# Example usage
def example_csp():
    """Example of using CSP Backtracking"""
    print("=== CSP Backtracking Search Example ===")
    
    # Sample Sudoku puzzle (0 represents empty cells)
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    # Create CSP solver
    csp = SudokuCSP()
    csp.load_puzzle(puzzle)
    
    print("Initial puzzle:")
    csp.display()
    
    # Solve with all heuristics
    print("\nSolving with MRV, LCV, and Forward Checking...")
    result = csp.solve_backtracking(use_mrv=True, use_lcv=True, use_forward_checking=True)
    
    if result['success']:
        print("\nSolution found!")
        csp.display()
    else:
        print("\nNo solution found!")
    
    print(f"\nPerformance metrics:")
    print(f"Runtime: {result['runtime']:.4f} seconds")
    print(f"Nodes explored: {result['nodes_explored']}")
    print(f"Backtracks: {result['backtracks']}")
"""
CSP Backtracking Search with MRV, LCV, and Forward Checking
Complete standalone implementation
"""
import time
import random

class SudokuCSP:
    def __init__(self, size=9):
        self.size = size
        self.subgrid_size = int(size ** 0.5)
        self.grid = [[0] * size for _ in range(size)]
        self.nodes_explored = 0
        self.backtracks = 0
    
    def load_puzzle(self, puzzle):
        """Load a puzzle into the grid"""
        self.grid = [row[:] for row in puzzle]
    
    def is_valid_move(self, row, col, num):
        """Check if a number is valid in a cell"""
        # Check row
        if num in self.grid[row]:
            return False
        
        # Check column
        for i in range(self.size):
            if self.grid[i][col] == num:
                return False
        
        # Check subgrid
        start_row = self.subgrid_size * (row // self.subgrid_size)
        start_col = self.subgrid_size * (col // self.subgrid_size)
        
        for i in range(self.subgrid_size):
            for j in range(self.subgrid_size):
                if self.grid[start_row + i][start_col + j] == num:
                    return False
        return True
    
    def get_empty_cells(self):
        """Get all empty cell positions"""
        return [(i, j) for i in range(self.size) for j in range(self.size) 
                if self.grid[i][j] == 0]
    
    def get_legal_values(self, row, col):
        """Get all legal values for a cell"""
        return [num for num in range(1, self.size + 1) 
                if self.is_valid_move(row, col, num)]
    
    def select_variable_mrv(self, empty_cells):
        """MRV heuristic: select variable with fewest legal values"""
        min_legal_values = float('inf')
        best_cell = empty_cells[0]
        
        for cell in empty_cells:
            row, col = cell
            legal_values = self.get_legal_values(row, col)
            if len(legal_values) < min_legal_values:
                min_legal_values = len(legal_values)
                best_cell = cell
        
        return best_cell
    
    def order_values_lcv(self, row, col, empty_cells):
        """LCV heuristic: order values by least constraining first"""
        values = []
        legal_values = self.get_legal_values(row, col)
        
        for num in legal_values:
            # Count how many constraints this value imposes
            constraint_count = self.count_constraints(row, col, num, empty_cells)
            values.append((constraint_count, num))
        
        # Sort by least constraining first
        values.sort()
        return [num for _, num in values]
    
    def count_constraints(self, row, col, num, empty_cells):
        """Count how constraining a value is on neighbors"""
        count = 0
        
        # Temporarily assign the value
        original_value = self.grid[row][col]
        self.grid[row][col] = num
        
        # Count reduced legal values for empty neighbors
        for i, j in empty_cells:
            if (i, j) != (row, col) and self.affects_cell(row, col, i, j):
                original_legal = len(self.get_legal_values(i, j))
                # The value is already assigned, so we just check the current state
                count += (20 - original_legal)  # Heuristic measure
        
        # Restore original value
        self.grid[row][col] = original_value
        return count
    
    def affects_cell(self, row1, col1, row2, col2):
        """Check if cell1 affects cell2 (same row, column, or subgrid)"""
        return (row1 == row2 or col1 == col2 or 
                (row1 // self.subgrid_size == row2 // self.subgrid_size and 
                 col1 // self.subgrid_size == col2 // self.subgrid_size))
    
    def forward_checking(self, empty_cells):
        """Check if all empty cells have at least one legal value"""
        for row, col in empty_cells:
            if not self.get_legal_values(row, col):
                return False
        return True
    
    def solve_backtracking(self, use_mrv=True, use_lcv=True, use_forward_checking=True):
        """Main backtracking solver with heuristics"""
        self.nodes_explored = 0
        self.backtracks = 0
        empty_cells = self.get_empty_cells()
        
        start_time = time.time()
        success = self._backtrack(empty_cells, use_mrv, use_lcv, use_forward_checking)
        end_time = time.time()
        
        return {
            'success': success,
            'solution': self.grid if success else None,
            'runtime': end_time - start_time,
            'nodes_explored': self.nodes_explored,
            'backtracks': self.backtracks
        }
    
    def _backtrack(self, empty_cells, use_mrv, use_lcv, use_forward_checking):
        """Recursive backtracking function"""
        if not empty_cells:
            return True
        
        # Select variable
        if use_mrv and len(empty_cells) > 1:
            row, col = self.select_variable_mrv(empty_cells)
        else:
            row, col = empty_cells[0]
        
        empty_cells.remove((row, col))
        
        # Order values
        if use_lcv:
            values = self.order_values_lcv(row, col, empty_cells)
        else:
            values = self.get_legal_values(row, col)
            random.shuffle(values)
        
        for value in values:
            self.nodes_explored += 1
            
            if self.is_valid_move(row, col, value):
                original_value = self.grid[row][col]
                self.grid[row][col] = value
                
                # Forward checking
                if use_forward_checking:
                    if not self.forward_checking(empty_cells):
                        self.grid[row][col] = original_value
                        continue
                
                if self._backtrack(empty_cells, use_mrv, use_lcv, use_forward_checking):
                    return True
                
                # Backtrack
                self.grid[row][col] = original_value
                self.backtracks += 1
        
        empty_cells.append((row, col))
        return False
    
    def display(self):
        """Display the Sudoku grid"""
        for i in range(self.size):
            if i % self.subgrid_size == 0 and i != 0:
                print("-" * (self.size * 3 + self.subgrid_size))
            for j in range(self.size):
                if j % self.subgrid_size == 0 and j != 0:
                    print("|", end=" ")
                print(f"{self.grid[i][j]:2d}" if self.grid[i][j] != 0 else " .", end=" ")
            print()

# Example usage
def example_csp():
    """Example of using CSP Backtracking"""
    print("=== CSP Backtracking Search Example ===")
    
    # Sample Sudoku puzzle (0 represents empty cells)
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    # Create CSP solver
    csp = SudokuCSP()
    csp.load_puzzle(puzzle)
    
    print("Initial puzzle:")
    csp.display()
    
    # Solve with all heuristics
    print("\nSolving with MRV, LCV, and Forward Checking...")
    result = csp.solve_backtracking(use_mrv=True, use_lcv=True, use_forward_checking=True)
    
    if result['success']:
        print("\nSolution found!")
        csp.display()
    else:
        print("\nNo solution found!")
    
    print(f"\nPerformance metrics:")
    print(f"Runtime: {result['runtime']:.4f} seconds")
    print(f"Nodes explored: {result['nodes_explored']}")
    print(f"Backtracks: {result['backtracks']}")

if __name__ == "_main_":
    example_csp()
