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

fireworkType = 0
NUM_FIREWORKS = 2

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

cx = [200, 1000]
cy = [1250, 1425]
r = [700, 900]
grassColor = [(0, 180, 0), (0, 140, 0)]
blades = []
def drawGrass():
    for x in range(1, screen.get_width(), 15):
        height = 721
        color = (0, 0, 0)

        if x >= cx[0] - r[0] and x <= cx[0] + r[0]:
            y = cy[0] - math.sqrt(r[0] * r[0] - (x - cx[0]) * (x - cx[0]))
            if y < height:
                height = y
                color = grassColor[0]

        if x >= cx[1] - r[1] and x <= cx[1] + r[1]:
            y = cy[1] - math.sqrt(r[1] * r[1] - (x - cx[1]) * (x - cx[1]))
            if y < height:
                if height < 720:
                    blades.append(grass.Grass(np.array([x, height]), color))
                height = y
                color = grassColor[1]
        
        blades.append(grass.Grass(np.array([x, height]), color))
                
drawGrass()

dt = 0
wind = np.array([0, 0])
fireworks = []
particles = []
time = 0

launch_angles = [[320, 670], [960, 670]]

while running:

    # wipes away stuff from the last frame
    draw_gradient(screen, (0, 0, 0), (30, 0, 40))
    particle_surface.fill((0, 0, 0, 0))

    pygame.draw.circle(screen, (0, 40, 0), (600, 975), 400, width=0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                fireworkType += 1
                fireworkType %= NUM_FIREWORKS
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # render firework here
            print(pos)
            pArray = [pos[0], pos[1]]
            
            if fireworkType == 0:
                # single color firework
                fireworks.append(firework.Firework(10, launch_angles[pos[0] // 640], [0, -100], pArray,  random.choice(FIREWORK_COLORS), 5))
            else:
                # multi-color firework
                fireworks.append(firework.multiColorFirework(10, launch_angles[pos[0] // 640], [0, -100], pArray,  random.choice(FIREWORK_COLORS), FIREWORK_COLORS, 5))
            
    
    # WIND FORCE
    time += dt
    fx = (6.0 * math.sin(0.3 * time) + 2.0 * math.sin(0.6 * time + 0.5))
    # fy = 20.0 * math.sin(0.5 * time) + random.uniform(-0.5, 0.5)

    wind[0] = fx
    wind[1] = 0.0

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

    # draw grass
    for blade in blades:
        blade.step(dt, wind)
        blade.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(32) / 1000  # limits FPS to 32

pygame.quit()