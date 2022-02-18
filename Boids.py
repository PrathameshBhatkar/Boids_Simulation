"""
This is a Boids algorithm simulater
Instructions:
    1. Press 's' to enable the simulation
    2. Press 'w' to activate Repel force
    3. Press 'e' to activate 'Point on same direction' / 'Align' force
    4. Press 'r' to activate 'move to center' force

    5. Press up and down arrow keys to change the values of selected variable during simulation

"""

# import all the libraries
import random

import pygame
import sys
from pygame.math import Vector2

# repel (Keep distance), same_direction (Align), move_to_center (Move to center of the visible boids)
# NOTE: all the values are divided so the smaller the value the stronger the force
repel = 50
same_direction = 20
move_to_center = 10

number_of_boids = 100

class Boid:
    """
    This is a Boid class
    Which represents individual boid
    It takes in the position as x, y

    Attributes:
    view_distance is the distance from which the boid can see
    dir is the direction in which the boid will move
    speed is the speed of the boid
    """
    speed = 10

    def __init__(self, x, y):
        self.pos = Vector2(x, y)
        self.view_distance = 25
        # generate a random vector
        self.dir = Vector2(random.randint(-40, 40) / 30, random.randint(-40, 40) / 30).normalize()

    def draw(self):
        pygame.draw.line(screen, COLOR_LITTLE_LIGHT_BLUE, self.pos, self.pos + (self.dir * 10))

        pygame.draw.circle(screen, COLOR_PINK, self.pos, 2)

    def update(self):
        # adding the direction to the position
        self.pos = self.pos + (self.dir * self.speed)
        # screen wrapping if the pos is outside the screen
        if self.pos.x > screenWidth:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = screenWidth
        if self.pos.y > screenHeight:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = screenHeight

    @staticmethod
    def dist_not_squared(p1: Vector2, p2: Vector2):
        return (abs(p1.x - p2.x) ** 2) + (abs(p1.y - p2.y) ** 2)

    def simulate_boid_rules(self):
        # make a list of nearby boids
        nearby_boids = []
        for b in boids:
            if b != self:
                d = self.dist_not_squared(b.pos, self.pos) ** .5
                if d < self.view_distance:
                    # if the boid is in the view distance add the boid to the nearby_boids list
                    nearby_boids.append(b)

                    if second:
                        self.dir += b.dir / same_direction
                    if first:
                        dir = (self.pos - b.pos)
                        dir = dir.normalize() / repel
                        self.dir += dir

                    self.dir = self.dir.normalize()

        # loop over nearby_boids
        # find average of the positions of the nearby_boids
        if third:
            try:
                average_pos = Vector2(0, 0)
                # add all the positions of the nearby_boids to the average_pos
                for b in nearby_boids: average_pos += b.pos
                average_pos /= len(nearby_boids)
                # find the direction of the average_pos
                dir = (average_pos - self.pos).normalize()
                # normalize the vector
                dir = dir.normalize() / move_to_center
                # add it to the direction
                self.dir += dir
                # normalize the vector
                self.dir = self.dir.normalize()
            except ZeroDivisionError:
                pass


pygame.init()
# *****************-- Normal Variables --*****************
screenHeight = 800
screenWidth = 1500
FPS = 60

# Colour
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_LITTLE_LIGHT_BLUE = (0, 150, 255)
COLOR_LIGHT_BLUE = (0, 255, 255)

COLOR_GRAY = (100, 100, 100)
COLOR_LIGHT_GRAY = (200, 200, 200)
COLOR_DARK_GRAY = (50, 50, 50)

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

COLOR_YELLOW = (255, 255, 0)
COLOR_PINK = (255, 0, 255)

# *****************-- SystemCore Variables --*************
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Boids algorithm')
clock = pygame.time.Clock()

# ********************************************************
boids = [Boid(random.randint(0, screenWidth), random.randint(0, screenHeight)) for i in range(number_of_boids)]

FONT = pygame.font.SysFont("comicsans", size=35)

selected = 0


# ********************************************************


def draw_window():
    screen.fill(COLOR_DARK_GRAY)
    # display Fps (frames per second)
    text = FONT.render("FPS: " + str(int(clock.get_fps())), True, COLOR_WHITE)
    screen.blit(text, (screenWidth - (text.get_width() + 10), 10))

    # draw fonts on top of each other on the with the values first, second and third
    text_first = FONT.render("Repel: " + str(first) + ", " + str(repel), True,
                             COLOR_WHITE if selected == 0 else COLOR_LIGHT_GRAY)
    text_second = FONT.render("Point on same direction: " + str(second) + ", " + str(same_direction), True,
                              COLOR_WHITE if selected == 1 else COLOR_LIGHT_GRAY)
    text_third = FONT.render("move to center: " + str(third) + ", " + str(move_to_center), True,
                             COLOR_WHITE if selected == 2 else COLOR_LIGHT_GRAY)

    screen.blit(text_first, (10, 10))
    screen.blit(text_second, (10, 50))
    screen.blit(text_third, (10, 90))

    # draw all boids
    for b in boids:
        b.draw()

    pygame.display.flip()


can_simulate = False
first = False
second = False
third = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: can_simulate = not can_simulate

            if event.key == pygame.K_w: first = not first
            if event.key == pygame.K_e: second = not second
            if event.key == pygame.K_r: third = not third

            # press 1,2 or 3 to change the selected variable to the corresponding one
            if event.key == pygame.K_1: selected = 0
            if event.key == pygame.K_2: selected = 1
            if event.key == pygame.K_3: selected = 2
    keys = pygame.key.get_pressed()

    # check if the up key is pressed
    if keys[pygame.K_UP]:
        # if the selected variable is 0, then change the value of repel which is first
        if selected == 0: repel += 1

        # if the selected variable is 1, then change the value of same_direction which is second
        if selected == 1: same_direction += 1

        # if the selected variable is 2, then change the value of move_to_center which is third
        if selected == 2: move_to_center += 1

    # check if the down key is pressed
    if keys[pygame.K_DOWN]:
        # Don't let the value of repel, same_direction, move_to_center to be less than 0

        # if the selected variable is 0, then change the value of repel which is first
        if selected == 0:
            if repel <= 0: repel = 0
            repel -= 1

        # if the selected variable is 1, then change the value of same_direction which is second
        if selected == 1:
            if same_direction <= 0: same_direction = 0
            same_direction -= 1

        # if the selected variable is 2, then change the value of move_to_center which is third
        if selected == 2:
            if move_to_center <= 0: move_to_center = 0
            move_to_center -= 1

    # update all the boids
    for b in boids:
        b.update()
        # if the variable can_simulate is true, then call the simulate function
        if can_simulate:
            b.simulate_boid_rules()

    draw_window()
    clock.tick(FPS)
