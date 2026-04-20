# open venv = venv\Scripts\Activate
# to leave venv = deactivate
# to generate requirements.txt = pip freeze > requirements.txt
import pygame
import particle

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
            particles.append(particle.particle(1, pArray, [10, 0], (255, 0, 0), 8))
            particles.append(particle.particle(1, pArray, [0, 10], (255, 255, 0), 8))
            particles.append(particle.particle(1, pArray, [5, 5], (255, 0, 255), 8))
            particles.append(particle.particle(1, pArray, [-10, 0], (0, 0, 255), 8))
            particles.append(particle.particle(1, pArray, [-10, 5], (0, 255, 0), 8))
            
            
    # RENDER YOUR GAME HERE
    i = 0
    while i < len(particles):
        if particles[i].timer <= 0:
            particles[i] = particles[-1]
            particles.pop()
            continue
        
        particles[i].step(dt)
        particles[i].draw(screen)
        i += 1

    for i in range(len(fireworks)):
        if fireworks[i].timer <= 0:

            fireworks[i].explode(particles) # spawn in the particles

            fireworks[i] = fireworks[-1]
            fireworks.pop()

            continue
            
        fireworks[i].step(dt)

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(32) / 1000  # limits FPS to 32

pygame.quit()