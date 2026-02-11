from __future__ import annotations

from typing import Any, ClassVar

import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    """Base class for circular sprites with position, velocity, and radius."""

    LINE_WIDTH: int = 2
    position: pygame.Vector2
    velocity: pygame.Vector2
    radius: float
    containers: ClassVar[tuple[pygame.sprite.AbstractGroup[Any], ...]] = ()

    def __init__(self, x: float, y: float, radius: int) -> None:
        """Initialize sprite state for a circular game object."""
        super().__init__(*self.containers)

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the sprite to the given screen surface."""
        # must override
        pass

    def collides_with(self, other: CircleShape) -> bool:
        """Return whether this circle overlaps another circle."""
        return self.position.distance_to(other.position) < (self.radius + other.radius)

    def update(self, dt: float) -> None:
        """Update sprite state using the elapsed delta time."""
        # must override
        pass
