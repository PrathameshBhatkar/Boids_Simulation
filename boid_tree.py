from boids import Boid
from tree import Node


class BoidNode(Node):
    def __init__(self, b: Boid):
        super().__init__()
        self.boid = b

    def value(self) -> float:
        return self.boid.pos.length_squared()
