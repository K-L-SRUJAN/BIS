import random
import math
import copy

# ---------- Helper Functions ----------
def tour_cost(tour, dist_matrix):
    cost = 0
    for i in range(len(tour)):
        cost += dist_matrix[tour[i]][tour[(i + 1) % len(tour)]]
    return cost

def two_opt_swap(tour):
    a, b = sorted(random.sample(range(len(tour)), 2))
    tour[a:b] = reversed(tour[a:b])
    return tour

def random_tour(n):
    tour = list(range(n))
    random.shuffle(tour)
    return tour

# ---------- PCA for TSP ----------
def pca_tsp(dist_matrix, num_cells=10, iterations=100):
    n = len(dist_matrix)
    cells = [{'tour': random_tour(n)} for _ in range(num_cells)]
    for cell in cells:
        cell['cost'] = tour_cost(cell['tour'], dist_matrix)

    for _ in range(iterations):
        new_cells = []
        for i in range(num_cells):
            neighbor = cells[(i + random.choice([-1, 1])) % num_cells]
            best_tour = neighbor['tour'] if neighbor['cost'] < cells[i]['cost'] else cells[i]['tour']
            new_tour = two_opt_swap(copy.deepcopy(best_tour))
            new_cost = tour_cost(new_tour, dist_matrix)
            if new_cost < cells[i]['cost']:
                new_cells.append({'tour': new_tour, 'cost': new_cost})
            else:
                new_cells.append(cells[i])
        cells = new_cells

    best = min(cells, key=lambda c: c['cost'])
    return best['tour'], best['cost']

# ---------- Example ----------
if __name__ == "__main__":
    # Example distance matrix (5 cities)
    dist_matrix = [
        [0, 2, 9, 10, 7],
        [2, 0, 6, 4, 3],
        [9, 6, 0, 8, 5],
        [10, 4, 8, 0, 6],
        [7, 3, 5, 6, 0]
    ]
    
    best_tour, best_cost = pca_tsp(dist_matrix, num_cells=10, iterations=200)
    print("Best Tour:", best_tour)
    print("Best Cost:", best_cost)
