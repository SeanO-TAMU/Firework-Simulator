import numpy as np
import math
import pygame
import random
import particle

class firework:
    def __init__(self, mass, pos, velocity, target, color, colors, timer):
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.target = np.array(target, dtype=float)
        self.color = color 
        self.colors = colors
        self.timer = timer

    def step(self, dt):
        force = np.array([0, 10])
        f = self.mass * force
        self.velocity += dt / self.mass * f
        self.pos += dt * self.velocity
        self.timer -= dt

    def explode(self, list):
        # spawn the light particles
        for _ in range(200):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 30)
            vx = math.cos(angle)
            vy = math.sin(angle)
            velocity = np.array([vx, vy]) * speed

            list.append(particle.particle(1, self.pos, velocity, self.colors[int(random.random() * len(self.colors))], 5))


        

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, tuple(self.pos), 5, width=0)