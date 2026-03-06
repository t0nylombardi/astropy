from __future__ import annotations

import random
from collections.abc import Callable
from typing import Any, ClassVar

import pygame
from pygame.math import Vector2

from astropy.assets.asteroid_sprites import AsteroidSpriteSheet
from astropy.entities.asteroid import Asteroid
from astropy.rendering.asteroid.asteroid_renderer import AsteroidRenderer

EdgeFactory = Callable[[float], Vector2]
Edge = tuple[Vector2, EdgeFactory]


class AsteroidField(pygame.sprite.Sprite):
    """
    Spawns asteroids periodically at random edges of the screen.

    The field acts as a system responsible for asteroid creation.
    It determines spawn location, direction, velocity, and visual renderer.
    """

    ASTEROID_SPAWN_RATE_SECONDS: ClassVar[float] = 1.5
    SPRITES: ClassVar[AsteroidSpriteSheet]

    containers: ClassVar[tuple[pygame.sprite.AbstractGroup[Any], ...]] = ()

    def __init__(self, screen_width: float, screen_height: float) -> None:
        """
        Initialize the asteroid spawning system.

        Args:
            screen_width: Width of the game screen.
            screen_height: Height of the game screen.
        """
        super().__init__(*self.containers)

        if not hasattr(self.__class__, "SPRITES"):
            self.__class__.SPRITES = AsteroidSpriteSheet("assets/asteroids.png")

        self._screen_width: float = screen_width
        self._screen_height: float = screen_height
        self._spawn_timer: float = 0.0

        self._edges: tuple[Edge, ...] = (
            (Vector2(1, 0), self._left_edge_spawn),
            (Vector2(-1, 0), self._right_edge_spawn),
            (Vector2(0, 1), self._top_edge_spawn),
            (Vector2(0, -1), self._bottom_edge_spawn),
        )

    def _left_edge_spawn(self, y: float) -> Vector2:
        """Return a spawn position on the left edge."""
        return Vector2(-Asteroid.MAX_RADIUS, y * self._screen_height)

    def _right_edge_spawn(self, y: float) -> Vector2:
        """Return a spawn position on the right edge."""
        return Vector2(self._screen_width + Asteroid.MAX_RADIUS, y * self._screen_height)

    def _top_edge_spawn(self, x: float) -> Vector2:
        """Return a spawn position on the top edge."""
        return Vector2(x * self._screen_width, -Asteroid.MAX_RADIUS)

    def _bottom_edge_spawn(self, x: float) -> Vector2:
        """Return a spawn position on the bottom edge."""
        return Vector2(x * self._screen_width, self._screen_height + Asteroid.MAX_RADIUS)

    def _size_from_radius(self, radius: int) -> str:
        """
        Map asteroid radius to sprite size.

        Args:
            radius: Collision radius of the asteroid.

        Returns:
            The sprite size category.
        """
        if radius >= Asteroid.MIN_RADIUS * 3:
            return "large"
        if radius >= Asteroid.MIN_RADIUS * 2:
            return "medium"
        return "small"

    def _renderer_for_radius(self, radius: int) -> AsteroidRenderer:
        """Build a renderer using a random sprite matching the asteroid radius."""
        size = self._size_from_radius(radius)
        sprite = self.SPRITES.get_random(size)
        return AsteroidRenderer(sprite, radius)

    def _spawn(self, radius: int, position: Vector2, velocity: Vector2) -> None:
        """
        Spawn a new asteroid entity.

        Args:
            radius: Collision radius of the asteroid.
            position: Spawn position.
            velocity: Initial movement vector.
        """
        renderer = self._renderer_for_radius(radius)
        asteroid = Asteroid(
            position.x,
            position.y,
            radius,
            renderer,
            self._renderer_for_radius,
        )
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        """
        Update the spawn timer and create new asteroids when necessary.

        Args:
            dt: Delta time since last frame.
        """
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
        radius = Asteroid.MIN_RADIUS * kind
        self._spawn(radius, position, velocity)
