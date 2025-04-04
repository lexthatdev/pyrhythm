import contextlib
with contextlib.redirect_stdout(None):
    import pygame

import json
import os
import time
from moviepy.editor import VideoFileClip
import configparser

# terminal print colors
TERMINAL_COLORS = {
    "perfect": "\033[95m",  # magenta
    "good": "\033[92m",     # green
    "meh": "\033[94m",      # blue
    "shit": "\033[93m",     # yellow
    "miss": "\033[91m",     # red
    "reset": "\033[0m"
}

# scoring windows (ms)
WINDOWS = {
    "perfect": 50,
    "good": 100,
    "meh": 150,
    "shit": 200,
    "miss": 500
}

pygame.init()
pygame.display.set_caption('pyrhythm')

# setup paths
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
dir_path = os.path.dirname(os.path.abspath(__file__))
misc_dir = os.path.join(dir_path, "misc")
charts_dir = os.path.join(dir_path, "charts")

pyrhythmlogo = pygame.image.load(os.path.join(misc_dir, 'logo.png'))
pygame.display.set_icon(pyrhythmlogo)

# load config
config = configparser.ConfigParser()
config.read(os.path.join(dir_path, "options.txt"))

username = config.get("GENERAL", "username", fallback="You")
show_musicvid = config.getboolean("GENERAL", "show_musicvid", fallback=True)
quit_oncomplete = config.getboolean("GENERAL", "quit_oncomplete", fallback=True)
sprite_notes = config.getboolean("GENERAL", "sprite_notes", fallback=False)
custom_colors = config.getboolean("GENERAL", "custom_colors", fallback=False)
autoplay = config.getboolean("GENERAL", "autoplay", fallback=False)

# load selected song
with open(os.path.join(misc_dir, "selectedsong.txt"), "r") as file:
    song_name = file.read().strip().replace(" ", "_")

real_song_name = song_name.replace("_",  "  ")
song_folder = os.path.join(charts_dir, song_name)
song_path = os.path.join(song_folder, "song.mp3")
chart_path = os.path.join(song_folder, "chart.json")
video_path = os.path.join(song_folder, "musicvid.mp4")

if not os.path.exists(song_path) or not os.path.exists(chart_path):
    print("Error: Song or chart not found!")
    exit()

video_clip = None
if show_musicvid and os.path.exists(video_path):
    video_clip = VideoFileClip(video_path)

# chart
with open(chart_path, "r") as f:
    chart_data = json.load(f)

# keybinds
keys = {}
if "KEYBINDS" in config:
    for action in config["KEYBINDS"]:
        key_name = config["KEYBINDS"][action]
        keys[action] = getattr(pygame, key_name, None)

# fallback keys
default_keys = {"left": pygame.K_LEFT, "down": pygame.K_DOWN, "up": pygame.K_UP, "right": pygame.K_RIGHT, "quit": pygame.K_ESCAPE}
for action in default_keys:
    if action not in keys or keys[action] is None:
        keys[action] = default_keys[action]

# colors
colors = {"left": (255, 0, 0), "down": (255, 255, 0), "up": (0, 0, 255), "right": (0, 255, 0)}
if custom_colors and "COLORS" in config:
    for direction in colors:
        try:
            colors[direction] = eval(config["COLORS"][direction])
        except:
            pass

# note sprites
note_sprites = {}
hitbox_sprites = {}
sprite_paths = config["SPRITES"] if "SPRITES" in config else {}
use_one_sprite = config.getboolean("SPRITES", "is_one_sprite", fallback=False)
if sprite_notes:
    if use_one_sprite:
        one_path = os.path.join(dir_path, config["SPRITES"].get("one_sprite", "").replace('"', ""))
        note_img = pygame.image.load(one_path)
        hitbox_img = pygame.image.load(one_path.replace(".png", "_hitbox.png"))
        for k in colors:
            note_sprites[k] = note_img
            hitbox_sprites[k] = hitbox_img
    else:
        for direction in colors:
            path = sprite_paths.get(direction, "")
            if path:
                full_path = os.path.join(dir_path, path)
                note_sprites[direction] = pygame.image.load(full_path)
                hitbox_sprites[direction] = pygame.image.load(full_path.replace(".png", "_hitbox.png"))

# game vars
SPEED = 300
HIT_WINDOW = 500
x_positions = {"left": 200, "down": 300, "up": 400, "right": 500}
notes = [{"time": note["time"] * 1000, "type": note["type"], "y": -50} for note in chart_data]

# scoring
combo = 0
max_combo = 0
results = {"perfect": 0, "good": 0, "meh": 0, "shit": 0, "miss": 0}
hit_flash = {}

font = pygame.font.SysFont("Comic Sans MS", 80, bold=True)
for i in range(3, 0, -1):
    screen.fill((0, 0, 0))
    text_surface = font.render(str(i), True, (255, 255, 255))
    screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, HEIGHT//2 - text_surface.get_height()//2))
    pygame.display.flip()
    time.sleep(1)

pygame.mixer.music.load(song_path)
pygame.mixer.music.play()
START_TIME = pygame.time.get_ticks()

running = True
while running:
    screen.fill((0, 0, 0))
    current_time = pygame.time.get_ticks() - START_TIME

    if quit_oncomplete and video_clip and current_time >= video_clip.duration * 1000:
        running = False

    if video_clip:
        video_frame = video_clip.get_frame(current_time / 1000)
        video_frame_surface = pygame.surfarray.make_surface(video_frame.swapaxes(0, 1))
        video_frame_surface = pygame.transform.scale(video_frame_surface, (WIDTH, HEIGHT))
        video_frame_surface.set_alpha(150)
        screen.blit(video_frame_surface, (0, 0))

    bar_width = 500
    bar_x = (WIDTH - bar_width) // 2
    bar_y = 0
    bar_height = HEIGHT
    bar_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
    bar_surface.fill((0, 0, 0, 150))
    screen.blit(bar_surface, (bar_x, bar_y))

    for key in x_positions:
        marker_x = bar_x + (bar_width - 50) // 2 + x_positions[key] - 344
        marker_y = bar_height - 80

        if key in hit_flash and pygame.time.get_ticks() - hit_flash[key] < 100:
            if sprite_notes and key in hitbox_sprites:
                img = pygame.transform.scale(hitbox_sprites[key], (50, 50))
                screen.blit(img, (marker_x, marker_y))
            else:
                color = colors[key] + (100,)
                surf = pygame.Surface((50, 50), pygame.SRCALPHA)
                surf.fill(color)
                screen.blit(surf, (marker_x, marker_y))
        pygame.draw.rect(screen, (255, 255, 255), (marker_x, marker_y, 50, 50), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == keys.get('quit'):
                running = False
            if not autoplay:
                for note in notes:
                    diff = abs(note["time"] - current_time)
                    if diff <= HIT_WINDOW and event.key == keys.get(note["type"]):
                        key = note["type"]
                        if diff <= WINDOWS["perfect"]:
                            results["perfect"] += 1
                            combo += 1
                        elif diff <= WINDOWS["good"]:
                            results["good"] += 1
                            combo += 1
                        elif diff <= WINDOWS["meh"]:
                            results["meh"] += 1
                            combo += 1
                        elif diff <= WINDOWS["shit"]:
                            results["shit"] += 1
                            combo = 0
                        else:
                            continue
                        if combo > max_combo:
                            max_combo = combo
                        hit_flash[key] = pygame.time.get_ticks()
                        notes.remove(note)
                        break

    if autoplay:
        for note in notes[:]:
            if abs(note["time"] - current_time) <= WINDOWS["perfect"]:
                key = note["type"]
                results["perfect"] += 1
                combo += 1
                if combo > max_combo:
                    max_combo = combo
                hit_flash[key] = pygame.time.get_ticks()
                notes.remove(note)

    for note in notes[:]:
        note["y"] = (note["time"] - current_time) / 1000 * SPEED
        if note["time"] < current_time - HIT_WINDOW:
            results["miss"] += 1
            notes.remove(note)
            combo = 0
            continue

        note_x = bar_x + (bar_width - 50) // 2 + x_positions[note["type"]] - 344
        note_y = bar_height - 80 - note["y"]

        if sprite_notes and note["type"] in note_sprites:
            screen.blit(pygame.transform.scale(note_sprites[note["type"]], (50, 50)), (note_x, note_y))
        else:
            pygame.draw.rect(screen, colors[note["type"]], (note_x, note_y, 50, 50))
            pygame.draw.rect(screen, (255, 255, 255), (note_x, note_y, 50, 50), 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# print results with color
total_hits = sum(results[k] for k in ["perfect", "good", "meh", "shit", "miss"])
score = results["perfect"] * 100 + results["good"] * 70 + results["meh"] * 50 + results["shit"] * 20
max_score = total_hits * 100
accuracy = (score / max_score) * 100 if max_score > 0 else 0

print(f"\n{TERMINAL_COLORS['good']} {username} completed the level '{real_song_name}' with a score of {score}!!!")

for category in ["perfect", "good", "meh", "shit", "miss"]:
    print(f"{TERMINAL_COLORS[category]}{category}: {results[category]}{TERMINAL_COLORS['reset']}")

print(f"\nhighest combo: {max_combo}")
print(f"accuracy: {accuracy:.2f}%")