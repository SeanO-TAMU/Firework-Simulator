# open venv = venv\Scripts\Activate
# to leave venv = deactivate
# to generate requirements.txt = pip freeze > requirements.txt
import pygame
import particle
import firework

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
clock = pygame.time.Clock()
running = True

dt = 0
fireworks = []
particles = []
while running:

    # wipes away stuff from the last frame
    screen.fill("black")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # render firework here
            print(pos)
            pArray = [pos[0], pos[1]]
            fireworks.append(firework.firework(10, [640, 720], [0, -100], pArray, (255, 0, 0), FIREWORK_COLORS, 10))
            
            
    # RENDER YOUR GAME HERE
    i = 0
    while i < len(particles):
        if particles[i].timer <= 0:
            particles[i] = particles[-1]
            particles.pop()
            continue
        
        particles[i].step(dt) # also need to pass in the wind force
        particles[i].draw(screen)
        i += 1

    i = 0
    while i < len(fireworks):
        if fireworks[i].timer <= 0:

            fireworks[i].explode(particles) # spawn in the particles

            fireworks[i] = fireworks[-1]
            fireworks.pop()

            continue
            
        fireworks[i].step(dt)
        fireworks[i].draw(screen)
        i += 1

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(32) / 1000  # limits FPS to 32

pygame.quit()