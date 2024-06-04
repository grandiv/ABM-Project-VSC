import pygame
import random
import math
import matplotlib.pyplot as plt

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dunkirk Evacuation Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 18)

# Track soldiers and evacuations
total_soldiers = 0
evacuated_soldiers = 0

# Boat settings
boat_capacity = 10

# Entry and exit points for soldiers and boats
entry_points = [(WIDTH // 2, HEIGHT - 10)]
evacuation_points = [(WIDTH - 50, HEIGHT // 2), (50, HEIGHT // 2)]

class Boat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.capacity = boat_capacity

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x - 20, self.y - 10, 40, 20))

class Soldier:
    def __init__(self):
        global total_soldiers
        self.x, self.y = random.choice(entry_points)
        self.color = BLUE
        self.speed = 2
        self.evacuation_point = random.choice(evacuation_points)
        self.evacuation_time = 0
        self.evacuated = False
        total_soldiers += 1

    def move(self):
        if self.evacuated:
            return False

        angle_to_boat = math.atan2(self.evacuation_point[1] - self.y, self.evacuation_point[0] - self.x)
        self.x += math.cos(angle_to_boat) * self.speed
        self.y += math.sin(angle_to_boat) * self.speed

        if self.distance_to_pos(self.evacuation_point) < 10:
            self.evacuation_time += 1
            if self.evacuation_time > 50:
                self.evacuated = True
                global evacuated_soldiers
                evacuated_soldiers += 1
                return False
        return True

    def distance_to_pos(self, pos):
        return math.sqrt((self.x - pos[0])**2 + (self.y - pos[1])**2)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), (int(self.y))), 5)

# Main loop
running = True
clock = pygame.time.Clock()
boats = [Boat(*evacuation_points[0]), Boat(*evacuation_points[1])]
soldiers = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn new soldiers randomly
    if random.random() < 0.05:
        soldiers.append(Soldier())

    # Move and remove evacuated soldiers
    soldiers = [soldier for soldier in soldiers if soldier.move()]

    # Draw everything
    screen.fill(WHITE)
    for boat in boats:
        boat.draw()
    for soldier in soldiers:
        soldier.draw()

    # Display statistics
    total_text = small_font.render(f'Total Soldiers: {total_soldiers}', True, BLACK)
    evacuated_text = small_font.render(f'Evacuated Soldiers: {evacuated_soldiers}', True, BLACK)
    screen.blit(total_text, (10, 10))
    screen.blit(evacuated_text, (10, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
