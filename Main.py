import pygame
import numpy as np
import random

movements = [-1, 0, 1]
running = True

GRID_SIZE = 100
NODE_SIZE = 8

food_grid = np.zeros((GRID_SIZE, GRID_SIZE))

for i in range(200):
    x = random.randint(0, GRID_SIZE - 1)
    y = random.randint(0, GRID_SIZE - 1)
    food_grid[x, y] = 1

prey_x = 50  
prey_y = 50
prey_energy = 150 

pygame.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Artificial Life Simulator")
clock = pygame.time.Clock()

while running:
    window.fill((10, 30, 50))

    prey_x = prey_x + random.choice(movements)
    prey_y = prey_y + random.choice(movements)

    if prey_x < 0: prey_x = 0
    if prey_x >= GRID_SIZE: prey_x = GRID_SIZE - 1
    if prey_y < 0: prey_y = 0
    if prey_y >= GRID_SIZE: prey_y = GRID_SIZE - 1

    if food_grid[prey_x, prey_y] == 1:
        prey_energy += 50      
        food_grid[prey_x, prey_y] = 0 

    prey_energy -= 1 

    food_positions = np.argwhere(food_grid == 1)
    for pos in food_positions:
        fx, fy = pos[0], pos[1]
        pygame.draw.rect(window, (255, 255, 0), (fx * NODE_SIZE, fy * NODE_SIZE, NODE_SIZE, NODE_SIZE))

    pixel_x = prey_x * NODE_SIZE 
    pixel_y = prey_y * NODE_SIZE 
    pygame.draw.rect(window, (0, 255, 100), (pixel_x, pixel_y, NODE_SIZE, NODE_SIZE))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if prey_energy <= 0: 
        print("Το πλάσμα πέθανε από ασιτία!")
        running = False
             
    pygame.display.flip()
    print(prey_energy)
    clock.tick(10) 

pygame.quit()