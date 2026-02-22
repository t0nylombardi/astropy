from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

import pygame


# Base class for game objects
class PhysicsBody(pygame.sprite.Sprite, ABC):
    """Base class for circular sprites with position, velocity, and radius."""

    LINE_WIDTH: int = 2
    containers: ClassVar[tuple[pygame.sprite.AbstractGroup[Any], ...]] = ()

    def __init__(self, x: float, y: float, radius: int) -> None:  # noqa: D107
        super().__init__(*self.containers)

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.radius: float = radius

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the sprite to the given screen surface."""
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update sprite state using the elapsed delta time."""
        pass

    def collides_with(self, other: PhysicsBody) -> bool:
        """Return whether this circle overlaps another circle."""
        return self.position.distance_to(other.position) < (self.radius + other.radius)
