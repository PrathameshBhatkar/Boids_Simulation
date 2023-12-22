# Boids Simulation

In this project I attempted to simulate flocking of small entities called boids (birdoids) 🕊 🦅. Which exist in a 2D
space and move around in a way that is similar to the way birds move.

## Description

It can simulate the movement of a flock of boids (birds) by the help of the Boids algorithm.

The Boids algorithm is a simple algorithm which has 3 main rules:

* Separation: Boids try to keep a small distance between themselves.
* Alignment: Boids try to match velocity of other boids.
* Cohesion: Boids try to match position of other boids.

* These rules are applied to each boid in the flock.

## Getting Started

### Dependencies

* This project uses the [pygame](https://www.pygame.org/) library.
* [python](https://www.python.org/) 3.6 or higher.
* I only tested it on Windows 10 🙄

<p align="right">(<a href="#top">back to top</a>)</p>

### Installing

* Download the code from by cloning the GitHub repository
* Open a command prompt and type:
```
    pip install -r requirements.txt
```
* You Don't need to install any other dependencies.

<p align="right">(<a href="#top">back to top</a>)</p>

### Executing program

* From the commandline, cd into the repo directory and run the following command:
```
python main.py
```
* Controls:

  1. Press `s` to enable the simulation
  2. Press `w` to activate Repel force
  3. Press `e` to activate 'Point on same direction' / 'Align' force
  4. Press `r` to activate 'move to center' force
  5. Press `up` and `down` arrow keys to change the values of selected variable during simulation

<p align="right">(<a href="#top">back to top</a>)</p>

## Authors

Prathamesh Bhatkar aka 🐱‍👤 [Ninja Cat Cder](https://www.codegrepper.com/profile/prathamesh-bhatkar)

Aaron Jencks aka [aaron-jencks](https://github.com/aaron-jencks)

## License

This Boids Algorithm is placed in the Public Domain.

## Acknowledgments

Inspiration from:

* [Coding train video](https://www.youtube.com/watch?v=mhjuuHl6qHM&t=1564s)
* [Boids Algorithm](https://www.red3d.com/cwr/boids/)