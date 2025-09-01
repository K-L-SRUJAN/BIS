import random
import numpy as np


def fitness(x):

    return (x - 0.3) ** 2 + 0.1  


def pso(num_particles=10, w=0.5, c1=1.5, c2=1.5, max_iter=100):

    particles = []
    velocities = []
    pbest = []
    pbest_fitness = []

    for _ in range(num_particles):
        x_i = random.uniform(0.0001, 1)       
        v_i = random.uniform(-0.01, 0.01)      
        f_i = fitness(x_i)
        particles.append(x_i)
        velocities.append(v_i)
        pbest.append(x_i)
        pbest_fitness.append(f_i)

    gbest_index = np.argmin(pbest_fitness)
    gbest = pbest[gbest_index]
    gbest_fitness = pbest_fitness[gbest_index]


    for _ in range(max_iter):
        for i in range(num_particles):
            r1, r2 = random.random(), random.random()

            velocities[i] = (
                w * velocities[i]
                + c1 * r1 * (pbest[i] - particles[i])
                + c2 * r2 * (gbest - particles[i])
            )

            particles[i] += velocities[i]
            particles[i] = max(0.0001, min(1, particles[i]))  

    
            f_i = fitness(particles[i])
            if f_i < pbest_fitness[i]:
                pbest[i] = particles[i]
                pbest_fitness[i] = f_i

                if f_i < gbest_fitness:
                    gbest = particles[i]
                    gbest_fitness = f_i

    return gbest, gbest_fitness


 
best_x, best_fit = pso()
print("Best Learning Rate (gbest):", best_x)
print("Best Fitness:", best_fit)
