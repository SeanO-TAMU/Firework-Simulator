# open venv = venv\Scripts\Activate
# to leave venv = deactivate
# to generate requirements.txt = pip freeze > requirements.txt
import pygame
import particle
import firework
import grass
import math
import random
import numpy as np

FIREWORK_COLORS = [
    (255, 0, 0),       # bright red
    (255, 80, 0),      # orange
    (255, 150, 0),     # amber
    (255, 255, 0),     # yellow
    (200, 255, 0),     # lime
    (0, 255, 0),       # green
    (0, 255, 150),     # aqua green
    (0, 200, 255),     # cyan
    (0, 100, 255),     # bright blue
    (100, 0, 255),     # violet
    (200, 0, 255),     # magenta
    (255, 0, 150),     # pink
]

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
particle_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
clock = pygame.time.Clock()
running = True

def draw_gradient(surface, top_color, bottom_color):
    height = surface.get_height()
    
    for y in range(height):
        # Interpolate color
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))

dt = 0
wind = np.array([0, 0])
fireworks = []
particles = []
time = 0

blades = []
origin = 50

for i in range(10):
    blades.append(grass.Grass(np.array([origin, 720])))
    origin += 50

while running:

    # wipes away stuff from the last frame
    draw_gradient(screen, (0, 0, 0), (30, 0, 40))
    particle_surface.fill((0, 0, 0, 0))

    pygame.draw.circle(screen, (0, 40, 0), (600, 975), 400, width=0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # render firework here
            print(pos)
            pArray = [pos[0], pos[1]]
            fireworks.append(firework.firework(10, [640, 720], [0, -100], pArray, (255, 0, 0), FIREWORK_COLORS, 6))
            
    
    # WIND FORCE
    time += dt
    fx = 20.0 * math.cos(0.5 * time) + random.uniform(-0.5, 0.5)
    fy = 20.0 * math.sin(0.5 * time) + random.uniform(-0.5, 0.5)

    wind[0] = fx
    wind[1] = fy

    # RENDER YOUR GAME HERE
    i = 0
    while i < len(particles):
        if particles[i].timer <= 0:
            particles[i] = particles[-1]
            particles.pop()
            continue
        
        particles[i].step(dt, wind) # also need to pass in the wind force
        particles[i].draw(particle_surface)
        i += 1

    i = 0
    while i < len(fireworks):
        if fireworks[i].timer <= 0:

            fireworks[i].explode(particles) # spawn in the particles

            fireworks[i] = fireworks[-1]
            fireworks.pop()

            continue
            
        fireworks[i].step(dt, particles, wind)
        fireworks[i].draw(particle_surface)
        i += 1

    screen.blit(particle_surface, (0, 0))

    # draw green hills
    pygame.draw.circle(screen, (0, 60, 0), (1000, 1425), 900, width=0)
    pygame.draw.circle(screen, (0, 80, 0), (200, 1250), 700, width=0)

    for blade in blades:
        blade.draw(screen)
    

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(32) / 1000  # limits FPS to 32

pygame.quit()