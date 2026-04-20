import numpy as np
import pygame
import random

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

        pass

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, tuple(self.pos), 10, width=0)