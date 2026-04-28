import pygame
import numpy as np


class Point:
    def __init__(self, pos):
        self.pos = pos

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 255, 0), tuple(self.pos), 1, width=0)

class Grass:
    def __init__(self, pos):
        # from start position make four points
        self.points = []
        self.pos = pos
        for i in range(4):
            self.points.append(Point(pos.copy()))
            pos[1] -= 10

    def step(self):
        pass

    def draw(self, surface):
        # draw lines between each point
        begin = self.points[0].pos
        for i in range(1, len(self.points)):

            pygame.draw.line(surface, (0, 255, 0), begin, self.points[i].pos, 1)
            begin = self.points[i].pos
            self.points[i].draw(surface)