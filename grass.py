import pygame
import numpy as np


class Point:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

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

    def step(self):
        pass

    def draw(self, surface):
        # draw lines between each point
        begin = self.points[0].pos
        for i in range(1, len(self.points)):

            pygame.draw.line(surface, self.color, begin, self.points[i].pos, 1)
            begin = self.points[i].pos
            self.points[i].draw(surface)