import random

import pygame
from pygame.math import Vector2

from tree import BinaryTree


COLOR_LITTLE_LIGHT_BLUE = (0, 150, 255)
COLOR_PINK = (255, 0, 255)

ZERO_VECTOR = Vector2(0, 0)


class Boid:
    """
    This is a Boid class
    Which represents individual boid
    It takes in the position as x, y

    Attributes:
    pos is the current position of the boid
    view_distance is the distance from which the boid can see
    dir is the direction in which the boid will move
    speed is the speed of the boid
    """
    speed = 10

    def __init__(self, x: int, y: int):
        self.pos = Vector2(x, y)
        self.view_distance = 25
        # generate a random direction vector
        self.dir = Vector2(random.randint(-40, 40) / 30, random.randint(-40, 40) / 30).normalize()

    def draw(self, screen):
        pygame.draw.line(screen, COLOR_LITTLE_LIGHT_BLUE, self.pos, self.pos + (self.dir * 10))

        pygame.draw.circle(screen, COLOR_PINK, self.pos, 2)

    def update(self, settings):
        # adding the direction to the position
        self.pos = self.pos + (self.dir * self.speed)
        # screen wrapping if the pos is outside the screen
        if self.pos.x > settings.width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = settings.width
        if self.pos.y > settings.height:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = settings.height

    @staticmethod
    def dist_not_squared(p1: Vector2, p2: Vector2):
        return (abs(p1.x - p2.x) ** 2) + (abs(p1.y - p2.y) ** 2)

    def simulate_boid_rules(self, boids: BinaryTree, settings):
        # make a list of nearby boids
        edist = self.pos.length_squared()
        nearby_boids = boids.find_interval(edist - self.view_distance, edist + self.view_distance)
        for b in nearby_boids:
            if settings.can_align:
                self.dir += b.boid.dir / settings.direction
            if settings.can_repel:
                dir = (self.pos - b.boid.pos)
                if dir != ZERO_VECTOR:
                    dir = dir.normalize() / settings.repel
                    self.dir += dir

            self.dir = self.dir.normalize()

        # loop over nearby_boids
        # find average of the positions of the nearby_boids
        if settings.can_center:
            try:
                average_pos = Vector2(0, 0)
                # add all the positions of the nearby_boids to the average_pos
                for b in nearby_boids: average_pos += b.boid.pos
                average_pos /= len(nearby_boids)
                # find the direction of the average_pos
                dir = average_pos - self.pos
                if dir != ZERO_VECTOR:
                    # normalize the vector
                    dir = dir.normalize()
                    dir = dir / settings.center
                    # add it to the direction
                    self.dir += dir
                    # normalize the vector
                    self.dir = self.dir.normalize()
            except ZeroDivisionError:
                pass