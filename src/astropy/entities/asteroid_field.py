import random
from collections.abc import Callable
from typing import Any, ClassVar

import pygame
from pygame.math import Vector2

from astropy.entities.asteroid import Asteroid

type EdgeFactory = Callable[[float], Vector2]
type Edge = tuple[Vector2, EdgeFactory]


class AsteroidField(pygame.sprite.Sprite):
    """Spawner that periodically creates asteroids at random screen edges."""

    # Domain constants (cohesive to this class)
    ASTEROID_KINDS: ClassVar[int] = 3
    ASTEROID_SPAWN_RATE_SECONDS: ClassVar[float] = 1.5

    containers: ClassVar[tuple[pygame.sprite.AbstractGroup[Any], ...]] = ()

    def __init__(self, screen_width: float, screen_height: float) -> None:
        """Create an Ateroid fieldn."""
        super().__init__(*self.containers)

        self._screen_width = screen_width
        self._screen_height = screen_height
        self._spawn_timer: float = 0.0

        self._edges: tuple[Edge, ...] = (
            (Vector2(1, 0), self._left_edge_spawn),
            (Vector2(-1, 0), self._right_edge_spawn),
            (Vector2(0, 1), self._top_edge_spawn),
            (Vector2(0, -1), self._bottom_edge_spawn),
        )

    def _left_edge_spawn(self, y: float) -> Vector2:
        return Vector2(-Asteroid.MAX_RADIUS, y * self._screen_height)

    def _right_edge_spawn(self, y: float) -> Vector2:
        return Vector2(self._screen_width + Asteroid.MAX_RADIUS, y * self._screen_height)

    def _top_edge_spawn(self, x: float) -> Vector2:
        return Vector2(x * self._screen_width, -Asteroid.MAX_RADIUS)

    def _bottom_edge_spawn(self, x: float) -> Vector2:
        return Vector2(x * self._screen_width, self._screen_height + Asteroid.MAX_RADIUS)

    def _spawn(self, radius: int, position: Vector2, velocity: Vector2) -> None:
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        """Spawn a new asteroids at a random."""
        self._spawn_timer += dt

        if self._spawn_timer < self.ASTEROID_SPAWN_RATE_SECONDS:
            return

        self._spawn_timer -= self.ASTEROID_SPAWN_RATE_SECONDS

        edge = random.choice(self._edges)
        speed = random.randint(40, 100)
        velocity = edge[0] * speed
        velocity = velocity.rotate(random.randint(-30, 30))
        position = edge[1](random.uniform(0, 1))
        kind = random.randint(1, Asteroid.KINDS)
        self._spawn(Asteroid.MIN_RADIUS * kind, position, velocity)
