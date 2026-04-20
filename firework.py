import numpy as np

class firework:
    def __init__(self, mass, pos, velocity, target):
        self.mass = mass
        self.pos = np.array([pos])
        self.velocity = np.array([velocity])
        self.target = np.array([target])

    def step(self):
        pass

    def explode(self, list):
        # spawn the light particles
        pass