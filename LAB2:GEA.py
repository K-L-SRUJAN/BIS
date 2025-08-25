import random

# Parameters
population_size = 100
mutation_rate = 0.1
crossover_rate = 0.7
generations = 200

# Initialize population: Random traffic signal timings (e.g., seconds per intersection)
def random_solution():
    return [random.randint(30, 60) for _ in range(4)]  # Example: 4 intersections

# Fitness function: Evaluates the solution (total waiting time + fuel consumption)
def fitness(solution):
    total_waiting_time = calculate_waiting_time(solution)
    fuel_consumption = calculate_fuel_consumption(solution)
    return total_waiting_time + fuel_consumption

def calculate_waiting_time(solution):
    # Placeholder for actual waiting time calculation based on traffic flow (simplified here)
    return sum(solution)  # Just sum the signal times as a proxy for waiting time

def calculate_fuel_consumption(solution):
    # Placeholder for fuel consumption based on waiting time at red lights
    return sum(solution) * 0.05  # Assuming a constant fuel cost per second of waiting

# Roulette Wheel Selection (to select individuals based on fitness)
def roulette_wheel_selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    pick = random.uniform(0, total_fitness)
    current = 0
    for i, fitness_value in enumerate(fitness_values):
        current += fitness_value
        if current > pick:
            return population[i]

# Crossover function: Mix two solutions (parents) to produce offspring
def crossover(parent1, parent2):
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, len(parent1)-1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    return parent1, parent2

# Mutation function: Randomly adjust a solution
def mutate(solution):
    if random.random() < mutation_rate:
        mutate_point = random.randint(0, len(solution)-1)
        solution[mutate_point] = random.randint(30, 60)  # Example: Randomize signal times
    return solution

# Main GEA loop
population = [random_solution() for _ in range(population_size)]

for generation in range(generations):
    # Evaluate fitness for the current population
    fitness_values = [fitness(individual) for individual in population]

    # Select individuals using Roulette Wheel Selection
    selected_population = [roulette_wheel_selection(population, fitness_values) for _ in range(population_size)]

    # Create the next generation through crossover and mutation
    new_population = []
    for i in range(0, population_size, 2):
        parent1, parent2 = selected_population[i], selected_population[i+1]
        child1, child2 = crossover(parent1, parent2)
        new_population.append(mutate(child1))
        new_population.append(mutate(child2))

    # Replace the old population with the new one
    population = new_population

# Output the best solution after all generations
best_solution = min(population, key=fitness)
print("Optimized Traffic Signal Timings:", best_solution)
