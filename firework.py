import numpy as np
import math
import pygame
import random
import particle

def vary_color(color, amount=40):
    return tuple(
        max(0, min(255, c + random.randint(-amount, amount)))
        for c in color
    )

def brighten(color, factor=1.2):
    return tuple(min(255, int(c * factor)) for c in color)

def darken(color, factor=0.8):
    return tuple(int(c * factor) for c in color)

class Firework:
    def __init__(self, mass, pos, velocity, target, color, timer):
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.target = np.array(target, dtype=float)
        self.color = color 
        self.timer = timer

    def step(self, dt, list, wind):
        force = np.array([0, 10])
        # pdcontrol = ks(dist) - kd(Vel)
        fPD = 5.0 * (self.target - self.pos) - 10.0 * self.velocity
        f = self.mass * force + wind + fPD
        self.velocity += dt / self.mass * f
        self.pos += dt * self.velocity
        self.timer -= dt

        # add some particles that are opposite of the velocity to create a trail behind firework
        numParticles = random.randint(1, 3)
        norm = np.linalg.norm(self.velocity)
        reverseVelo = -self.velocity
        for _ in range(numParticles):
            spread = np.array([random.uniform(-0.6, 0.6), random.uniform(-0.6, 0.6)])
            particle_velocity = reverseVelo + spread * 20
            list.append(particle.particle(1, self.pos + spread * 2, particle_velocity, self.color, 0.4))

    def explode(self, list):
        # spawn the light particles
        for _ in range(200):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 30)
            vx = math.cos(angle)
            vy = math.sin(angle)
            velocity = np.array([vx, vy]) * speed

            color = self.color
            if random.random() >= 0.5:
                 color = vary_color(color, 60)
            
            r = random.random()
            if r < 0.25:
                color = brighten(color)
            elif r > 0.75:
                color = darken(color)

            list.append(particle.particle(0.5, self.pos, velocity, color, 5))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, tuple(self.pos), 4, width=0)

class multiColorFirework(Firework):
    def __init__(self, mass, pos, velocity, target, color, colors, timer):
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.target = np.array(target, dtype=float)
        self.color = color 
        self.colors = colors
        self.timer = timer
    
    def explode(self, list):
        # spawn the light particles
        for _ in range(200):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 30)
            vx = math.cos(angle)
            vy = math.sin(angle)
            velocity = np.array([vx, vy]) * speed

            list.append(particle.particle(0.5, self.pos, velocity, self.colors[int(random.random() * len(self.colors))], 5))

class ringFirework(Firework):
    def __init__(self, mass, pos, velocity, target, color, colors, timer):
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.target = np.array(target, dtype=float)
        self.color = color 
        self.colors = colors
        self.timer = timer
    
    def explode(self, list):
        # spawn the light particles
        for _ in range(300):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 30)
            vx = math.cos(angle)
            vy = math.sin(angle)
            velocity = np.array([vx, vy]) * speed
            color = (0, 0, 0)
            if speed <= 8:
                color = self.colors[0]
            elif speed <= 16:
                color = self.colors[1]
            else:
                color = self.colors[2]

            list.append(particle.particle(0.5, self.pos, velocity, color, 5))

class multiStageFirework(Firework):
    def __init__(self, mass, pos, velocity, target, color, colors, timer, list):
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.target = np.array(target, dtype=float)
        self.color = color 
        self.colors = colors
        self.timer = timer
        self.list = list
    
    def explode(self, list):
        # spawn the light particles
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 20)
            vx = math.cos(angle)
            vy = math.sin(angle)
            velocity = np.array([vx, vy]) * speed

            color = self.color
            if random.random() >= 0.5:
                 color = vary_color(color, 60)
            
            r = random.random()
            if r < 0.25:
                color = brighten(color)
            elif r > 0.75:
                color = darken(color)

            self.list.append(particleFirework(10, self.pos, velocity, color, 2))

class particleFirework(Firework):
    def __init__(self, mass, pos, velocity, color, timer):
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.color = color 
        self.timer = timer
    
    def step(self, dt, list, wind):
        force = np.array([0, 10])
        # fPD = 5.0 * (self.target - self.pos) - 10.0 * self.velocity
        f = self.mass * force + wind
        self.velocity += dt / self.mass * f
        self.pos += dt * self.velocity
        self.timer -= dt

    def explode(self, list):
        # spawn the light particles
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 20)
            vx = math.cos(angle)
            vy = math.sin(angle)
            velocity = np.array([vx, vy]) * speed

            color = self.color
            if random.random() >= 0.5:
                 color = vary_color(color, 60)
            
            r = random.random()
            if r < 0.25:
                color = brighten(color)
            elif r > 0.75:
                color = darken(color)

            list.append(particle.particle(0.5, self.pos, velocity, color, 5))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, tuple(self.pos), 1, width=0)
