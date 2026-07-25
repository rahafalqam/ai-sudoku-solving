"""
Simulated Annealing for Sudoku - Complete standalone implementation
"""
import time
import math
import random

class SudokuSA:
    def __init__(self, size=9):
        self.size = size
        self.subgrid_size = int(size ** 0.5)
        self.grid = [[0] * size for _ in range(size)]
        self.original_puzzle = None
    
    def load_puzzle(self, puzzle):
        """Load a puzzle into the grid"""
        self.grid = [row[:] for row in puzzle]
        self.original_puzzle = [row[:] for row in puzzle]
    
    def count_violations(self):
        """Count total constraint violations in the grid"""
        violations = 0
        
        # Check rows
        for i in range(self.size):
            row = [x for x in self.grid[i] if x != 0]
            violations += len(row) - len(set(row))
        
        # Check columns
        for j in range(self.size):
            col = [self.grid[i][j] for i in range(self.size) if self.grid[i][j] != 0]
            violations += len(col) - len(set(col))
        
        # Check subgrids
        for box_i in range(0, self.size, self.subgrid_size):
            for box_j in range(0, self.size, self.subgrid_size):
                subgrid = []
                for i in range(self.subgrid_size):
                    for j in range(self.subgrid_size):
                        val = self.grid[box_i + i][box_j + j]
                        if val != 0:
                            subgrid.append(val)
                violations += len(subgrid) - len(set(subgrid))
        
        return violations
    
    def create_initial_solution(self):
        """Create initial solution by filling subgrids with random permutations"""
        solution = [row[:] for row in self.grid]
        
        # Fill each subgrid
        for box_i in range(0, self.size, self.subgrid_size):
            for box_j in range(0, self.size, self.subgrid_size):
                # Find existing numbers and empty positions
                existing_numbers = []
                empty_positions = []
                
                for i in range(self.subgrid_size):
                    for j in range(self.subgrid_size):
                        row = box_i + i
                        col = box_j + j
                        if self.original_puzzle[row][col] != 0:
                            existing_numbers.append(self.original_puzzle[row][col])
                        else:
                            empty_positions.append((row, col))
                
                # Find missing numbers
                all_numbers = set(range(1, self.size + 1))
                missing_numbers = list(all_numbers - set(existing_numbers))
                random.shuffle(missing_numbers)
                
                # Fill empty positions
                for idx, (row, col) in enumerate(empty_positions):
                    solution[row][col] = missing_numbers[idx]
        
        return solution
    
    def generate_neighbor(self, current_solution):
        """Generate a neighbor by swapping two values in the same subgrid"""
        neighbor = [row[:] for row in current_solution]
        
        # Find a subgrid with at least 2 non-fixed cells
        attempts = 0
        while attempts < 100:
            # Random subgrid
            box_i = random.randint(0, self.subgrid_size - 1) * self.subgrid_size
            box_j = random.randint(0, self.subgrid_size - 1) * self.subgrid_size
            
            # Find swappable positions (non-fixed cells)
            swappable = []
            for i in range(self.subgrid_size):
                for j in range(self.subgrid_size):
                    row = box_i + i
                    col = box_j + j
                    if self.original_puzzle[row][col] == 0:  # Non-fixed cell
                        swappable.append((row, col))
            
            if len(swappable) >= 2:
                # Select two different positions to swap
                pos1, pos2 = random.sample(swappable, 2)
                row1, col1 = pos1
                row2, col2 = pos2
                
                # Swap values
                neighbor[row1][col1], neighbor[row2][col2] = \
                    neighbor[row2][col2], neighbor[row1][col1]
                break
            
            attempts += 1
        
        return neighbor
    
    def solve_simulated_annealing(self, initial_temp=1000, cooling_rate=0.99, 
                                 max_iterations=50000, min_temp=0.01):
        """Main simulated annealing solver"""
        start_time = time.time()
        
        # Create initial solution
        current_solution = self.create_initial_solution()
        current_energy = self.calculate_energy(current_solution)
        
        best_solution = [row[:] for row in current_solution]
        best_energy = current_energy
        
        temperature = initial_temp
        iteration = 0
        energy_history = [current_energy]
        
        print(f"Starting SA: Initial energy = {current_energy}")
        
        while (temperature > min_temp and 
               iteration < max_iterations and 
               best_energy > 0):
            
            # Generate neighbor
            neighbor = self.generate_neighbor(current_solution)
            neighbor_energy = self.calculate_energy(neighbor)
            
            # Calculate energy difference
            energy_diff = neighbor_energy - current_energy
            
            # Metropolis acceptance criterion
            if energy_diff < 0:
                # Always accept better solutions
                current_solution = neighbor
                current_energy = neighbor_energy
            else:
                # Accept worse solutions with probability
                acceptance_prob = math.exp(-energy_diff / (temperature + 1e-10))
                if random.random() < acceptance_prob:
                    current_solution = neighbor
                    current_energy = neighbor_energy
            
            # Update best solution
            if current_energy < best_energy:
                best_solution = [row[:] for row in current_solution]
                best_energy = current_energy
            
            # Cooling
            temperature *= cooling_rate
            iteration += 1
            energy_history.append(current_energy)
            
            # Progress reporting
            if iteration % 1000 == 0:
                print(f"Iteration {iteration}: Energy = {current_energy}, Temp = {temperature:.2f}")
        
        end_time = time.time()
        
        # Update final grid
        self.grid = best_solution
        
        return {
            'success': best_energy == 0,
            'solution': best_solution,
            'energy': best_energy,
            'runtime': end_time - start_time,
            'iterations': iteration,
            'final_temperature': temperature,
            'energy_history': energy_history
        }
    
    def calculate_energy(self, solution):
        """Calculate energy (constraint violations) for a solution"""
        # Simplified energy calculation for performance
        energy = 0
        
        # Check rows
        for i in range(self.size):
            row = solution[i]
            energy += len(row) - len(set(row))
        
        # Check columns
        for j in range(self.size):
            col = [solution[i][j] for i in range(self.size)]
            energy += len(col) - len(set(col))
        
        return energy
    
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
def example_simulated_annealing():
    """Example of using Simulated Annealing"""
    print("=== Simulated Annealing Example ===")
    
    # Sample Sudoku puzzle
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
    
    # Create SA solver
    sa = SudokuSA()
    sa.load_puzzle(puzzle)
    
    print("Initial puzzle:")
    sa.display()
    print(f"Initial violations: {sa.count_violations()}")
    
    # Solve with Simulated Annealing
    print("\nRunning Simulated Annealing...")
    result = sa.solve_simulated_annealing(
        initial_temp=1000,
        cooling_rate=0.995,
        max_iterations=30000
    )
    
    print(f"\nFinal energy: {result['energy']}")
    if result['success']:
        print("Perfect solution found!")
    else:
        print("Approximate solution found")
    
    sa.display()
    
    print(f"\nPerformance metrics:")
    print(f"Runtime: {result['runtime']:.4f} seconds")
    print(f"Iterations: {result['iterations']}")
    print(f"Final temperature: {result['final_temperature']:.4f}")

if __name__ == "_main_":
    example_simulated_annealing()

