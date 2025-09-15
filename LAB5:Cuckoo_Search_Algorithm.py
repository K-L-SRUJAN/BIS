import numpy as np
import random
 
def total_distance(tour, dist_matrix):
    d = 0
    for i in range(len(tour)):
        d += dist_matrix[tour[i - 1]][tour[i]]
    return d

 
def levy_flight_solution(tour):
    new_tour = tour.copy()
 
    i, j = sorted(random.sample(range(len(tour)), 2))
 
    new_tour[i:j] = reversed(new_tour[i:j])
    return new_tour

 
def cuckoo_search_tsp(dist_matrix, n=20, Pa=0.25, MaxIt=500):
    num_cities = len(dist_matrix)
    
 
    nests = [random.sample(range(num_cities), num_cities) for _ in range(n)]
    fitness = [total_distance(tour, dist_matrix) for tour in nests]
    
    best_idx = np.argmin(fitness)
    best_tour = nests[best_idx]
    best_fitness = fitness[best_idx]
    
    for t in range(MaxIt):
        for i in range(n):
   
            new_tour = levy_flight_solution(nests[i])
            new_fit = total_distance(new_tour, dist_matrix)
            
           
            j = random.randint(0, n-1)
            if new_fit < fitness[j]:
                nests[j] = new_tour
                fitness[j] = new_fit
        
      
        num_abandon = int(Pa * n)
        worst_idx = np.argsort(fitness)[-num_abandon:]
        for idx in worst_idx:
            nests[idx] = random.sample(range(num_cities), num_cities)
            fitness[idx] = total_distance(nests[idx], dist_matrix)
        
 
        curr_best_idx = np.argmin(fitness)
        if fitness[curr_best_idx] < best_fitness:
            best_tour = nests[curr_best_idx]
            best_fitness = fitness[curr_best_idx]
    
    return best_tour, best_fitness

 
if __name__ == "__main__":
 
    dist_matrix = [
        [0, 2, 9, 10, 7],
        [1, 0, 6, 4, 3],
        [15, 7, 0, 8, 3],
        [6, 3, 12, 0, 11],
        [9, 7, 5, 6, 0]
    ]
    
    best_tour, best_dist = cuckoo_search_tsp(dist_matrix, n=20, Pa=0.25, MaxIt=500)
    print("Best Tour (order of cities):", best_tour)
    print("Best Distance:", best_dist)
