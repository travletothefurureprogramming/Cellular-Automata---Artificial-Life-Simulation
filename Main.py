import pygame
import numpy as np
import random

GRID_SIZE = 100
NODE_SIZE = 8
pygame.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Artificial Life Simulator")
clock = pygame.time.Clock()

running = True
frame_count = 0
is_night = False

food_grid = np.zeros((GRID_SIZE, GRID_SIZE))
for i in range(400):
    food_grid[random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)] = 1

preys = [{"x": random.randint(0, GRID_SIZE-1), "y": random.randint(0, GRID_SIZE-1), 
          "energy": 150, "speed": random.randint(1,3), "vision": random.randint(5,25)} for _ in range(40)]

predators = [
    {"x": 10, "y": 10, "energy": 250},
    {"x": 90, "y": 10, "energy": 250},
    {"x": 10, "y": 90, "energy": 250},
    {"x": 90, "y": 90, "energy": 250}
]

prey_history = []
pred_history = []
MAX_HISTORY = 100 

pygame.font.init()
font = pygame.font.SysFont('Arial', 18)

def draw_stats(window, preys, predators, is_night):
    stats = [
        f"Preys: {len(preys)}",
        f"Predators: {len(predators)}",
        f"Time: {'Night' if is_night else 'Day'}",
        f"Avg Prey Speed: {sum(p['speed'] for p in preys)/len(preys):.1f}" if preys else "Preys: 0"
    ]
    
    for i, text in enumerate(stats):
        surface = font.render(text, True, (255, 255, 255))
        window.blit(surface, (10, 10 + i * 20))

def draw_graph(window, prey_hist, pred_hist):
    graph_rect = pygame.Rect(550, 50, 200, 100)
    pygame.draw.rect(window, (0, 0, 0), graph_rect) # Background γραφήματος
    
    # Σχεδίαση γραμμών
    for i in range(1, len(prey_hist)):
        # Πράσινη γραμμή για preys
        start_pos = (550 + (i-1)*2, 150 - prey_hist[i-1]//2)
        end_pos = (550 + i*2, 150 - prey_hist[i]//2)
        pygame.draw.line(window, (0, 255, 100), start_pos, end_pos)
        
        # Κόκκινη γραμμή για predators
        start_pos_p = (550 + (i-1)*2, 150 - pred_hist[i-1]*2)
        end_pos_p = (550 + i*2, 150 - pred_hist[i]*2)
        pygame.draw.line(window, (255, 50, 50), start_pos_p, end_pos_p)

while running:
    if is_night:
        window.fill((5, 5, 20))
        if random.random() < 0.30: food_grid[random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)] = 1
    else:
        window.fill((10, 30, 50))
        if random.random() < 0.20: food_grid[random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)] = 1

    food_positions = np.argwhere(food_grid == 1)
    for pos in food_positions:
        pygame.draw.rect(window, (255, 255, 0), (pos[0] * NODE_SIZE, pos[1] * NODE_SIZE, NODE_SIZE, NODE_SIZE))

    for prey in preys[:]:
        if is_night:
            current_speed, energy_drain = 0, 0.0
            if prey["energy"] < 250: prey["energy"] += 0.2
        else:
            if prey["energy"] < 75: current_speed, energy_drain = max(1, int(prey["speed"]/2)), 1.0
            elif prey["energy"] > 150: current_speed, energy_drain = 1, 0.5
            else: current_speed, energy_drain = prey["speed"], 1.0
            
            prey_pos = np.array([prey["x"], prey["y"]])
            closest_food = None
            min_dist = prey["vision"]
            for f in food_positions:
                dist = np.linalg.norm(prey_pos - np.array([f[0], f[1]]))
                if dist < min_dist: min_dist, closest_food = dist, f

            if closest_food is not None:
                dx, dy = np.sign(closest_food[0] - prey["x"]), np.sign(closest_food[1] - prey["y"])
                prey["x"] += int(dx * min(current_speed, abs(closest_food[0] - prey["x"])))
                prey["y"] += int(dy * min(current_speed, abs(closest_food[1] - prey["y"])))
            elif current_speed > 0:
                prey["x"] += random.choice([-current_speed, 0, current_speed])
                prey["y"] += random.choice([-current_speed, 0, current_speed])

        prey["x"], prey["y"] = max(0, min(GRID_SIZE-1, prey["x"])), max(0, min(GRID_SIZE-1, prey["y"]))
        prey["energy"] -= energy_drain
        if not is_night and food_grid[prey["x"], prey["y"]] == 1:
            prey["energy"] += 45
            food_grid[prey["x"], prey["y"]] = 0
            
        pygame.draw.rect(window, (0, 255, 100), (prey["x"] * NODE_SIZE, prey["y"] * NODE_SIZE, NODE_SIZE, NODE_SIZE))

        if not is_night and prey["energy"] >= 250:
            prey["energy"] -= 120
            preys.append({"x": prey["x"], "y": prey["y"], "energy": 100, "speed": prey["speed"], "vision": prey["vision"]})

    for p in predators[:]:
        p["energy"] -= 5 if is_night else 3
        min_dist = 2 if is_night else 15
        target = None
        for prey in preys:
            dist = np.linalg.norm(np.array([p["x"], p["y"]]) - np.array([prey["x"], prey["y"]]))
            if dist < min_dist: min_dist, target = dist, prey

        if target:
            p["x"] += np.sign(target["x"] - p["x"])
            p["y"] += np.sign(target["y"] - p["y"])
            if p["x"] == target["x"] and p["y"] == target["y"]:
                p["energy"] += 80
                target["energy"] = 0
        else:
            p["x"] += random.choice([-1, 0, 1])
            p["y"] += random.choice([-1, 0, 1])

        p["x"], p["y"] = max(0, min(GRID_SIZE-1, p["x"])), max(0, min(GRID_SIZE-1, p["y"]))
        pygame.draw.rect(window, (255, 50, 50), (p["x"] * NODE_SIZE, p["y"] * NODE_SIZE, NODE_SIZE, NODE_SIZE))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    preys = [p for p in preys if p["energy"] > 0]
    predators = [p for p in predators if p["energy"] > 0]
    
    if is_night and not (frame_count % 600 >= 300):
        for p in preys: p["energy"] = min(250, p["energy"] + 5)
    
    is_night = (frame_count % 600 >= 300)
    frame_count += 1
    draw_stats(window, preys, predators, is_night)
    draw_stats(window, preys, predators, is_night)
    draw_graph(window, prey_history, pred_history) 
    
    prey_history.append(len(preys))
    pred_history.append(len(predators))

    if len(prey_history) > MAX_HISTORY:
        prey_history.pop(0)
        pred_history.pop(0)
    pygame.display.flip()
    clock.tick(15)

pygame.quit()