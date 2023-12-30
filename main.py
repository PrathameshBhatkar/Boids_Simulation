import random
import argparse
from typing import List

import pygame

from boids import Boid
from boid_tree import BoidNode
from tree import BinaryTree


# Colour
COLOR_LIGHT_GRAY = (200, 200, 200)
COLOR_DARK_GRAY = (50, 50, 50)
COLOR_WHITE = (255, 255, 255)


def setup_args() -> argparse.ArgumentParser:
    """
    sets up the argument parser for the flags

    returns the parser
    """
    parser = argparse.ArgumentParser(description='A boids simulation program')
    parser.add_argument('-r', '--repel', default=50, type=int, help='the strength of the force to repel')
    parser.add_argument('-d', '--direction', default=20, type=int, help='the strength of the force to align direction')
    parser.add_argument('-c', '--center', default=10, type=int, help='the strength of the force to move boids to the center of mass')
    parser.add_argument('-n', '--number_of_boids', default=100, type=int, help='the number of boids to simulate')
    parser.add_argument('-t', '--height', default=800, type=int, help='the height of the window in pixels')
    parser.add_argument('-w', '--width', default=1500, type=int, help='the width of the window in pixels')
    parser.add_argument('-f', '--fps', default=60, type=int, help='the nominal framerate to shoot for')
    parser.add_argument('-s', '--speed', default=10, type=int, help='the speed of the boids')
    return parser


def draw_window(settings, screen, boids: List[BoidNode]):
    """
    draws the window
    """
    screen.fill(COLOR_DARK_GRAY)
    # display Fps (frames per second)
    text = settings.font.render("FPS: " + str(int(clock.get_fps())), True, COLOR_WHITE)
    screen.blit(text, (settings.width - (text.get_width() + 10), 10))

    # draw fonts on top of each other on the with the values first, second and third
    text_repel = settings.font.render(f"Repel: {settings.can_repel}, {settings.repel}", True,
                             COLOR_WHITE if settings.selected == 0 else COLOR_LIGHT_GRAY)
    text_align = settings.font.render(f"Point on same direction: {settings.can_align}, {settings.direction}", True,
                              COLOR_WHITE if settings.selected == 1 else COLOR_LIGHT_GRAY)
    text_center = settings.font.render(f"move to center: {settings.can_center}, {settings.center}", True,
                             COLOR_WHITE if settings.selected == 2 else COLOR_LIGHT_GRAY)

    screen.blit(text_repel, (10, 10))
    screen.blit(text_align, (10, 50))
    screen.blit(text_center, (10, 90))

    # draw all boids
    for b in boids:
        b.boid.draw(screen)

    pygame.display.flip()


if __name__ == '__main__':
    parser = setup_args()
    settings = parser.parse_args()

    # initialize pygame
    pygame.init()

    # setup variables
    settings.simulate = False
    settings.can_repel = False
    settings.can_align = False
    settings.can_center = False
    settings.selected = 0
    settings.font = pygame.font.SysFont("comicsans", size=35)

    width = settings.width
    height = settings.height
    num = settings.number_of_boids

    # *****************-- SystemCore Variables --*************
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Boids algorithm')
    clock = pygame.time.Clock()

    # ********************************************************
    boids = [BoidNode(Boid(random.randint(0, width), random.randint(0, height))) for _ in range(num)]

    # generate binary tree
    btree = BinaryTree()
    for b in boids:
        btree.add_node(b)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s: settings.simulate = not settings.simulate

                if event.key == pygame.K_w: settings.can_repel = not settings.can_repel
                if event.key == pygame.K_e: settings.can_align = not settings.can_align
                if event.key == pygame.K_r: settings.can_center = not settings.can_center

                # press 1,2 or 3 to change the selected variable to the corresponding one
                if event.key == pygame.K_1: settings.selected = 0
                if event.key == pygame.K_2: settings.selected = 1
                if event.key == pygame.K_3: settings.selected = 2

        keys = pygame.key.get_pressed()

        # check if the up key is pressed
        if keys[pygame.K_UP]:
            # if the selected variable is 0, then change the value of repel which is first
            if settings.selected == 0: settings.repel += 1

            # if the selected variable is 1, then change the value of same_direction which is second
            if settings.selected == 1: settings.direction += 1

            # if the selected variable is 2, then change the value of move_to_center which is third
            if settings.selected == 2: settings.center += 1

        # check if the down key is pressed
        if keys[pygame.K_DOWN]:
            # Don't let the value of repel, same_direction, move_to_center to be less than 0

            # if the selected variable is 0, then change the value of repel which is first
            if settings.selected == 0:
                if settings.repel <= 0: settings.repel = 0
                settings.repel -= 1

            # if the selected variable is 1, then change the value of same_direction which is second
            if settings.selected == 1:
                if settings.direction <= 0: settings.direction = 0
                settings.direction -= 1

            # if the selected variable is 2, then change the value of move_to_center which is third
            if settings.selected == 2:
                if settings.center <= 0: settings.center = 0
                settings.center -= 1

        # update all the boids
        for b in boids:
            b.boid.update(settings)
            # if the variable can_simulate is true, then call the simulate function
            if settings.simulate:
                b.boid.simulate_boid_rules(boids, settings)
            # update the position in the boid into the tree
            btree.reinsert_node(b)

        draw_window(settings, screen, boids)
        clock.tick(settings.fps)
