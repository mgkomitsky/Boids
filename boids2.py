import math
import funcs
import pygame
from operator import add
import random

pygame.init()

screen = pygame.display.set_mode([1000, 1000])


class Flock:
    def __init__(self):
        self.boids = []
        for x in range(25):
            self.boids.append(Boid())
            x += 1

    def getMeanPosition(self, boid, nextBoid):
        x = 0
        y = 0
        for boid in self.boids:
            if self.distance(boid, nextBoid) < 100:
                x += boid.position[0]
                y += boid.position[1]
        return (x/len(self.boids), y/len(self.boids))

    def getMousePosition(self):
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        return [x, y]

    def distance(self, boid, otherBoid):
        z = math.pow(otherBoid.position[0] - boid.position[0], 2) + \
            math.pow(otherBoid.position[1] - boid.position[1], 2)
        return math.sqrt(z)

    def distance2(self, a, b):
        z = math.pow(b[0] - a.position[0], 2) + \
            math.pow(b[1] - a.position[1], 2)
        return math.sqrt(z)

    def iterator(self):

        for boid in self.boids:
            for nextBoid in self.boids:
                if boid != nextBoid:

                    # Cohesion: Steer towards average position
                    if self.distance(boid, nextBoid) <= 200:
                        newVector = funcs.subtract(
                            self.getMeanPosition(boid, nextBoid), boid.position)  # Vector to next boid

                        newAcceleration = funcs.add(
                            boid.acceleration, newVector)  # New acceleration vector

                        boid.acceleration = funcs.limit(
                            newAcceleration, boid.maxAcceleration)  # Limit max acceleration

                    if self.distance2(boid, self.getMousePosition()) <= 30:
                        newVector = funcs.subtract(
                            boid.position, self.getMousePosition())  # Vector to next boid

                        newAcceleration = funcs.add(
                            boid.acceleration, newVector)  # New acceleration vector

                        boid.acceleration = funcs.limit(
                            newAcceleration, .01)  # Limit max acceleration

                    if self.distance(boid, nextBoid) <= 20:
                        newVector = funcs.subtract(
                            boid.position, nextBoid.position)  # Vector to next boid

                        newAcceleration = funcs.add(
                            boid.acceleration, newVector)  # New acceleration vector

                        boid.acceleration = funcs.limit(
                            newAcceleration, .01)  # Limit max acceleration

                    if self.distance(boid, nextBoid) <= 30:
                        newVector = funcs.subtract(
                            nextBoid.velocity, boid.velocity)  # Vector to next boid

                        newAcceleration = funcs.add(
                            boid.acceleration, newVector)  # New acceleration vector

                        boid.acceleration = funcs.limit(
                            newAcceleration, .005)  # Limit max acceleration

                    boid.calculatePhysics()
            boid.update()


class Boid:
    def __init__(self):
        self.acceleration = [0, 0]
        self.velocity = [random.randrange(
            0, 1), random.randrange(0, 1)]
        self.position = [random.randrange(
            200, 400), random.randrange(100, 400)]
        self.maxSpeed = .3
        self.maxForce = 1
        self.maxAcceleration = .001

    def update(self):
        x = round(self.position[0])
        y = round(self.position[1])

        if x >= 1000:
            pygame.draw.circle(screen, (0, 255, 200), (0, y), 5)
            self.position[0] = 0

        elif y >= 1000:
            pygame.draw.circle(screen, (0, 255, 200), (x, 0), 5)
            self.position[1] = 0

        elif x <= 0:
            pygame.draw.circle(screen, (0, 255, 200), (1000, y), 5)
            self.position[0] = 1000

        elif y <= 0:
            pygame.draw.circle(screen, (0, 255, 200), (x, 1000), 5)
            self.position[1] = 1000

        else:
            pygame.draw.circle(screen, (0, 255, 200),
                               (round(self.position[0]), round(self.position[1])), 5)

        self.acceleration[0] = 0
        self.acceleration[1] = 0

    def calculatePhysics(self):

        self.velocity = funcs.limit(
            list(map(add, self.velocity, self.acceleration)), self.maxSpeed)

        self.position = list(map(add, self.position, self.velocity))


running = True
flock = Flock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    flock.iterator()
    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()
