from __future__ import annotations

import random
from typing import ClassVar

import pygame
from pygame.math import Vector2

from astropy.entities.physics_body import PhysicsBody
from astropy.logger import log_event
from astropy.rendering.asteroid_renderer_protocol import AsteroidRendererProtocol


class Asteroid(PhysicsBody):
    """
    Represents an asteroid entity with physics behavior and pluggable rendering.

    Asteroids can split into smaller fragments when destroyed unless they
    are already at the minimum size.
    """

    MIN_RADIUS: ClassVar[int] = 20
    KINDS: ClassVar[int] = 3
    MAX_RADIUS: ClassVar[int] = MIN_RADIUS * KINDS

    def __init__(
        self,
        x: float,
        y: float,
        radius: int,
        renderer: AsteroidRendererProtocol,
    ) -> None:
        """
        Create a new asteroid.

        Args:
            x: Initial X position.
            y: Initial Y position.
            radius: Collision radius of the asteroid.
            renderer: Rendering strategy responsible for drawing the asteroid.
        """
        super().__init__(x, y, radius)

        self.renderer: AsteroidRendererProtocol = renderer

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the asteroid using its renderer.

        Args:
            screen: Target pygame surface.
        """
        self.renderer.draw(screen, self.position)

    def split(self) -> None:
        """
        Destroy the asteroid and spawn smaller fragments if possible.

        Larger asteroids split into two fragments with slightly diverging
        velocities to simulate an explosion effect.
        """
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

    def _spawn_fragment(self, velocity: Vector2, radius: int) -> None:
        """
        Spawn a fragment asteroid after a split.

        Args:
            velocity: Velocity vector for the fragment.
            radius: Radius of the new asteroid.
        """
        renderer = self.renderer.clone()

        asteroid = Asteroid(
            self.position.x,
            self.position.y,
            radius,
            renderer,
        )

        asteroid.velocity = velocity * 1.2

    def update(self, dt: float) -> None:
        """
        Update asteroid physics and renderer animation.

        Args:
            dt: Delta time since the previous frame.
        """
        self.position += self.velocity * dt
        self.renderer.update(dt)
