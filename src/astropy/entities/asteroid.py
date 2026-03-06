import random
from typing import ClassVar

import pygame

from astropy.entities.physics_body import PhysicsBody
from astropy.logger import log_event


class Asteroid(PhysicsBody):
    """A moving asteroid represented as a circular game object."""

    MIN_RADIUS: ClassVar[int] = 20
    KINDS: ClassVar[int] = 3
    MAX_RADIUS: ClassVar[int] = MIN_RADIUS * KINDS

    def __init__(self, x: float, y: float, radius: int) -> None:
        """Initialize an asteroid at `(x, y)` with a given collision radius."""
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        """Render the asteroid as a white outlined circle."""
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            self.LINE_WIDTH,
        )

    def split(self) -> None:
        """Split asteroid into two smaller asteroids."""
        self.kill()

        if self.radius <= self.MIN_RADIUS:
            return

        log_event("asteroid_split")

        angle = random.uniform(20, 50)
        velocity1 = self.velocity.rotate(angle)
        velocity2 = self.velocity.rotate(-angle)
        new_radius = self.radius - self.MIN_RADIUS

        self._spawn_fragment(velocity1, new_radius)
        self._spawn_fragment(velocity2, new_radius)

    def _spawn_fragment(self, velocity: pygame.Vector2, radius: int) -> None:
        asteroid = Asteroid(self.position.x, self.position.y, radius)
        asteroid.velocity = velocity * 1.2

    def update(self, dt: float) -> None:
        """Advance asteroid position according to velocity and delta time."""
        self.position += self.velocity * dt
