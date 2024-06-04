import pygame
import random
import math
import matplotlib.pyplot as plt
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulasi Kerumunan Mall")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 192, 203)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
BROWN = (139, 69, 19)
LIGHTBLUE = (173, 216, 230)
LIGHTGREEN = (144, 238, 144)
GRAY = (169, 169, 169)

font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 18)

entered_count = 0
exited_count = 0
current_inside_count = 0

start_time = pygame.time.get_ticks()
opening_time = 8 * 60
closing_time = 22 * 60
current_time = opening_time

day_of_week = 0
day_start_time = start_time

door_width = 10
entry_doors = [(WIDTH - door_width, HEIGHT // 3), (WIDTH - door_width, 2 * HEIGHT // 3)]
exit_doors = [(door_width, HEIGHT // 3), (door_width, 2 * HEIGHT // 3)]

class Store:
    def __init__(self, x, y, store_type):
        self.x = x
        self.y = y
        self.store_type = store_type
        self.color = (
            GREEN if store_type == "Videogame" else
            PINK if store_type == "Kosmetik" else
            YELLOW if store_type == "Barang Murah" else
            PURPLE if store_type == "Perhiasan" else
            ORANGE if store_type == "Pakaian" else
            CYAN if store_type == "Elektronik" else
            BROWN if store_type == "Perabotan" else
            LIGHTBLUE if store_type == "Toko Buku" else
            LIGHTGREEN
        )

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x - 20, self.y - 20, 40, 40))
        text = small_font.render(self.store_type, True, BLACK)
        screen.blit(text, (self.x - 20, self.y - 30))

stores = [
    Store(100, 100, "Videogame"),
    Store(WIDTH - 100, 100, "Kosmetik"),
    Store(100, HEIGHT - 100, "Barang Murah"),
    Store(WIDTH - 100, HEIGHT - 100, "Perhiasan"),
    Store(WIDTH // 2, 100, "Pakaian"),
    Store(WIDTH // 2, HEIGHT - 100, "Elektronik"),
    Store(100, HEIGHT // 2, "Perabotan"),
    Store(WIDTH - 100, HEIGHT // 2, "Toko Buku"),
    Store(WIDTH // 4, HEIGHT // 4, "Restoran"),
    Store(3 * WIDTH // 4, 3 * HEIGHT // 4, "Toko Sepatu"),
]

visitor_per_hour = [0] * 24
visitor_per_day = [0] * 7
daily_visitor_count = 0

class Agent:
    def __init__(self, gender, age, income):
        global entered_count, current_inside_count
        self.gender = gender
        self.age = age
        self.income = income
        self.x, self.y = random.choice(entry_doors)
        self.angle = random.uniform(math.pi, 2 * math.pi)
        self.floor = 0

        self.color = BLUE if gender == "male" else RED

        if age < 20:
            self.speed = 3
        elif age > 60:
            self.speed = 1
        else:
            self.speed = 2

        self.target_store = None
        self.time_in_store = 0
        self.exiting = False
        self.target_door = None
        entered_count += 1
        current_inside_count += 1

    def move(self, agents):
        if self.exiting:
            if self.target_door is None:
                self.target_door = random.choice(exit_doors)
            angle_to_door = math.atan2(self.target_door[1] - self.y, self.target_door[0] - self.x)
            self.angle = angle_to_door
            self.x += math.cos(self.angle) * self.speed
            self.y += math.sin(self.angle) * self.speed

            if self.x < door_width:
                global exited_count, current_inside_count
                exited_count += 1
                current_inside_count -= 1
                return False
        else:
            if self.target_store is None:
                self.select_store()

            if self.target_store:
                angle_to_store = math.atan2(self.target_store.y - self.y, self.target_store.x - self.x)
                self.angle = angle_to_store
                self.x += math.cos(self.angle) * self.speed
                self.y += math.sin(self.angle) * self.speed

                if self.distance_to(self.target_store) < 10:
                    self.time_in_store += 1
                    if self.time_in_store > 50:
                        self.select_store()

        self.avoid_collisions(agents)

        return True

    def select_store(self):
        self.time_in_store = 0
        if random.random() < 0.1 or current_time >= closing_time:
            self.exiting = True
            self.target_store = None
        else:
            self.target_store = random.choice(stores)

    def avoid_collisions(self, agents):
        for agent in agents:
            if agent is not self:
                distance = self.distance_to(agent)
                if distance < 10:
                    angle_to_agent = math.atan2(agent.y - self.y, agent.x - self.x)
                    self.x -= math.cos(angle_to_agent) * self.speed
                    self.y -= math.sin(angle_to_agent) * self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), (int(self.y))), 5)

    def distance_to(self, obj):
        return math.sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2)

    def distance_to_pos(self, pos):
        return math.sqrt((self.x - pos[0])**2 + (self.y - pos[1])**2)

agents = []

# Main
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    current_time = (opening_time + elapsed_time) % (24 * 60)

    if current_time >= closing_time or current_time < opening_time:
        for agent in agents:
            agent.exiting = True

    day_elapsed = (pygame.time.get_ticks() - day_start_time) // (24 * 60 * 1000)
    day_of_week = (day_of_week + day_elapsed) % 7
    if day_elapsed > 0:
        day_start_time = pygame.time.get_ticks()

    if opening_time <= current_time < closing_time:
        probability = 0.05 if day_of_week < 5 else 0.1
        if random.random() < probability:
            for _ in range(random.randint(1, 5)):
                if random.random() < 0.5:
                    agents.append(Agent("male", random.randint(10, 70), random.randint(20000, 100000)))
                else:
                    agents.append(Agent("female", random.randint(10, 70), random.randint(20000, 100000)))

    hour = current_time // 60
    visitor_per_hour[hour] = current_inside_count
    visitor_per_day[day_of_week] = daily_visitor_count

    agents = [agent for agent in agents if agent.move(agents)]

    screen.fill(WHITE)
    for store in stores:
        store.draw()
    for agent in agents:
        agent.draw()

    for door in entry_doors:
        pygame.draw.rect(screen, GREEN, (door[0] - door_width // 2, door[1] - 20, door_width, 40))
    for door in exit_doors:
        pygame.draw.rect(screen, RED, (door[0] - door_width // 2, door[1] - 20, door_width, 40))

    entered_text = small_font.render(f'Pengunjung Masuk: {entered_count}', True, BLACK)
    exited_text = small_font.render(f'Pengujung Keluar: {exited_count}', True, BLACK)
    current_inside_text = small_font.render(f'Jumlah Pengunjung: {current_inside_count}', True, BLACK)
    screen.blit(entered_text, (10, 10))
    screen.blit(exited_text, (160, 10))
    screen.blit(current_inside_text, (310, 10))

    hours = current_time // 60
    minutes = current_time % 60
    time_text = small_font.render(f'{hours:02}:{minutes:02}', True, BLACK)
    screen.blit(time_text, (WIDTH - 150, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

def plot_visitor_stats(visitor_per_hour, visitor_per_day):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.plot(range(24), visitor_per_hour, marker='o')
    ax1.set_title('Pengunjung Per Jam')
    ax1.set_xlabel('Jam')
    ax1.set_ylabel('Jumlah Pengunjung')

    days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    ax2.plot(days, visitor_per_day, marker='o', linestyle='--', color='r')
    ax2.set_title('Pengunjung Per Hari')
    ax2.set_xlabel('Hari')
    ax2.set_ylabel('Jumlah Pengunjung')

    plt.tight_layout()
    plt.show()

plot_visitor_stats(visitor_per_hour, visitor_per_day)