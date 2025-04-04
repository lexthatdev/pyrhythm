import pygame
import json
import time

# initialize pygame
pygame.init()

# screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# load song and chart
pygame.mixer.music.load("song.mp3")
with open("chart.json", "r") as f:
    chart_data = json.load(f)

# game variables
SPEED = 100  # pixels per second
HIT_WINDOW = 150  # ms
keys = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN}
colors = {"left": (255, 0, 0), "right": (0, 255, 0), "up": (0, 0, 255), "down": (255, 255, 0)}
x_positions = {"left": 200, "right": 400, "up": 300, "down": 500}
notes = [{"time": note["time"] * 1000, "type": note["type"], "y": -50} for note in chart_data]

time.sleep(2)
# start the song
pygame.mixer.music.play()
START_TIME = pygame.time.get_ticks()

# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    current_time = pygame.time.get_ticks() - START_TIME
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            for note in notes:
                if abs(note["time"] - current_time) < HIT_WINDOW and event.key == keys[note["type"]]:
                    print(f"Hit {note['type']}!")
                    notes.remove(note)
                    break
    
    for note in notes:
        note["y"] = 600 - ((note["time"] - current_time) / 1000 * SPEED)
        pygame.draw.rect(screen, colors[note["type"]], (x_positions[note["type"]], note["y"], 50, 50))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
