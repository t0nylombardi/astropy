import random
from typing import Any, Callable, ClassVar, TypeAlias

import pygame

from asteroid import Asteroid
from constants import (
    ASTEROID_KINDS,
    ASTEROID_MAX_RADIUS,
    ASTEROID_MIN_RADIUS,
    ASTEROID_SPAWN_RATE_SECONDS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

EdgeFactory: TypeAlias = Callable[[float], pygame.Vector2]
Edge: TypeAlias = tuple[pygame.Vector2, EdgeFactory]


def left_edge_spawn(y: float) -> pygame.Vector2:
    """Return a spawn position just beyond the left screen edge."""
    return pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT)


def right_edge_spawn(y: float) -> pygame.Vector2:
    """Return a spawn position just beyond the right screen edge."""
    return pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT)


def top_edge_spawn(x: float) -> pygame.Vector2:
    """Return a spawn position just above the top screen edge."""
    return pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS)


def bottom_edge_spawn(x: float) -> pygame.Vector2:
    """Return a spawn position just below the bottom screen edge."""
    return pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS)


class AsteroidField(pygame.sprite.Sprite):
    """Spawner that periodically creates asteroids at random screen edges."""

    containers: ClassVar[tuple[pygame.sprite.AbstractGroup[Any], ...]] = ()
    edges: ClassVar[tuple[Edge, ...]] = (
        (
            pygame.Vector2(1, 0),
            left_edge_spawn,
        ),
        (
            pygame.Vector2(-1, 0),
            right_edge_spawn,
        ),
        (
            pygame.Vector2(0, 1),
            top_edge_spawn,
        ),
        (
            pygame.Vector2(0, -1),
            bottom_edge_spawn,
        ),
    )

    def __init__(self) -> None:
        """Initialize the spawner with a zeroed spawn timer."""
        pygame.sprite.Sprite.__init__(self, *self.containers)
        self.spawn_timer = 0.0

    def spawn(
        self,
        radius: int,
        position: pygame.Vector2,
        velocity: pygame.Vector2,
    ) -> None:
        """Create one asteroid with the provided radius, position, and velocity."""
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        """Spawn a new asteroid after each configured interval."""
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity: pygame.Vector2 = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position: pygame.Vector2 = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
