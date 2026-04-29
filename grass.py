import pygame
import numpy as np


class Point:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.mass = 0.2
        self.velocity = np.array([0.0, 0.0], dtype=float)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, tuple(self.pos), 1, width=0)

class Grass:
    def __init__(self, pos, color):
        # from start position make four points
        self.points = []
        self.pos = pos
        self.color = color

        for i in range(4):
            self.points.append(Point(pos.copy(), self.color))
            pos[1] -= 10

    def step(self, dt, wind):
        if dt <= 0:
            return
        p = []

        # unconstrained step
        for i in range(len(self.points)):

            p.append(self.points[i].pos.copy())

            if i == 0:
                continue

            f = wind
            self.points[i].velocity += dt / self.points[i].mass * f
            self.points[i].pos += dt * self.points[i].velocity

        # apply constraint
        for i in range(1, len(self.points)):
            delta = self.points[i].pos - self.points[i - 1].pos
            length = np.linalg.norm(delta)
            
            constraint = length - 10

            w1 = 1.0 / self.points[i - 1].mass
            if i == 1:
                w1 = 0.0
            w2 = 1.0 / self.points[i].mass

            g1 = -1.0 * delta/length
            g2 = delta/length

            lamb = - constraint / (w1 * np.linalg.norm(g1) * np.linalg.norm(g1) + w2 * np.linalg.norm(g2) * np.linalg.norm(g2))

            self.points[i - 1].pos += lamb * w1 * g1
            self.points[i].pos += lamb * w2 * g2


        # project back using constraint
        for i in range(len(self.points)):
            if i == 0:
                continue
            
            self.points[i].velocity = (1.0 / dt) * (self.points[i].pos - p[i])

    def draw(self, surface):
        # draw lines between each point
        begin = self.points[0].pos
        for i in range(1, len(self.points)):

            pygame.draw.line(surface, self.color, begin, self.points[i].pos, 1)
            begin = self.points[i].pos
            self.points[i].draw(surface)