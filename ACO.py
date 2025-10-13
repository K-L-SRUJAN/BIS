import random
import math
import numpy as np

 
def initialize_aco(num_ants, num_cities, pheromone_init, alpha, beta, rho, Q):
    pheromone_matrix = np.full((num_cities, num_cities), pheromone_init)  
    best_solution = None
    best_cost = float('inf')
    return pheromone_matrix, best_solution, best_cost
 
def build_solution(pheromone_matrix, alpha, beta, num_cities, heuristic_matrix):
    visited = [False] * num_cities
    solution = []
    current_city = random.randint(0, num_cities - 1)  
    visited[current_city] = True
    solution.append(current_city)
    
    for _ in range(num_cities - 1):
        next_city = select_next_city(current_city, visited, pheromone_matrix, alpha, beta, heuristic_matrix, num_cities)
        solution.append(next_city)
        visited[next_city] = True
        current_city = next_city
    
    return solution
 
def select_next_city(current_city, visited, pheromone_matrix, alpha, beta, heuristic_matrix, num_cities):
    probabilities = []
    total_prob = 0.0
    
    for next_city in range(num_cities):
        if not visited[next_city]:
            pheromone = pheromone_matrix[current_city][next_city]
            heuristic = heuristic_matrix[current_city][next_city]
            prob = (pheromone ** alpha) * (heuristic ** beta)
            total_prob += prob
            probabilities.append(prob)
        else:
            probabilities.append(0)
    
 
    probabilities = [prob / total_prob for prob in probabilities]
 
    return roulette_wheel_selection(probabilities)
 
def roulette_wheel_selection(probabilities):
    rand = random.random()
    cumulative_prob = 0.0
    for i, prob in enumerate(probabilities):
        cumulative_prob += prob
        if cumulative_prob >= rand:
            return i
    return len(probabilities) - 1

 
def evaluate_solution(solution, distance_matrix):
    total_distance = 0
    for i in range(len(solution) - 1):
        total_distance += distance_matrix[solution[i]][solution[i + 1]]
    total_distance += distance_matrix[solution[-1]][solution[0]]  
    return total_distance

 
def update_pheromones(pheromone_matrix, solutions, distances, rho, Q):
 
    pheromone_matrix *= (1 - rho)
   
    for i, solution in enumerate(solutions):
        for j in range(len(solution) - 1):
            pheromone_matrix[solution[j]][solution[j + 1]] += Q / distances[i]
        pheromone_matrix[solution[-1]][solution[0]] += Q / distances[i]  

 
def ACO(num_ants, num_cities, distance_matrix, pheromone_init, alpha, beta, rho, Q, max_iterations):
    pheromone_matrix, best_solution, best_cost = initialize_aco(num_ants, num_cities, pheromone_init, alpha, beta, rho, Q)
    
    for iteration in range(max_iterations):
        solutions = []
        distances = []
        
         
        for _ in range(num_ants):
            solution = build_solution(pheromone_matrix, alpha, beta, num_cities, distance_matrix)
            solutions.append(solution)
            cost = evaluate_solution(solution, distance_matrix)
            distances.append(cost)
             
            if cost < best_cost:
                best_cost = cost
                best_solution = solution
         
        update_pheromones(pheromone_matrix, solutions, distances, rho, Q)

        print(f"Iteration {iteration + 1}, Best Cost: {best_cost}")
    
    return best_solution, best_cost


num_cities = 5
num_ants = 10
max_iterations = 100
pheromone_init = 0.1
alpha = 1.0   
beta = 2.0  
rho = 0.5   
Q = 100       

 
distance_matrix = [
    [0, 2, 9, 10, 1],
    [1, 0, 6, 4, 3],
    [15, 7, 0, 8, 6],
    [6, 3, 12, 0, 5],
    [10, 8, 4, 6, 0]
]

 
heuristic_matrix = np.array([[1 / distance_matrix[i][j] if distance_matrix[i][j] > 0 else 0 for j in range(num_cities)] for i in range(num_cities)])

 
best_solution, best_cost = ACO(num_ants, num_cities, distance_matrix, pheromone_init, alpha, beta, rho, Q, max_iterations)

print("Best Solution:", best_solution)
print("Best Cost:", best_cost)
