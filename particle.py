import numpy as np
import pygame

class particle:
    # have a mass, pos, velocity, color
    def __init__(self, mass, pos, velocity, color, timer):
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.color = color
        self.timer = timer # fade away the particle
        self.alpha = 255
    
    def step(self, dt):
        # just do gravity for now
        force = np.array([0, 10])
        f = self.mass * force
        self.velocity += dt / self.mass * f
        self.pos += dt * self.velocity
        self.timer -= dt
        self.alpha = max(int(min(255, 255 * self.timer)), 0)
    
    def draw(self, surface):
        pygame.draw.circle(surface, (*self.color, self.alpha), tuple(self.pos), 1, width=0)
