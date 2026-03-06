import random

import pygame


class AsteroidRenderer:
    """Handles visual representation of an asteroid."""

    def __init__(self, sprite: pygame.Surface, radius: int) -> None:
        """Store a scaled asteroid sprite and initialize random rotation and spin."""
        diameter = radius * 2
        self.image = pygame.transform.smoothscale(sprite, (diameter, diameter))
        self.rotation = random.uniform(0, 360)
        self.spin = random.uniform(-50, 50)

    def update(self, dt: float) -> None:
        """Advance the renderer rotation by elapsed time."""
        self.rotation += self.spin * dt

    def draw(self, screen: pygame.Surface, position: pygame.Vector2) -> None:
        """Draw the rotated sprite centered at the given world position."""
        rotated = pygame.transform.rotate(self.image, self.rotation)
        rect = rotated.get_rect(center=position)
        screen.blit(rotated, rect)

    def clone(self) -> "AsteroidRenderer":
        """Create a renderer copy sharing the same sprite surface."""
        clone = object.__new__(AsteroidRenderer)
        clone.image = self.image
        clone.rotation = random.uniform(0, 360)
        clone.spin = random.uniform(-50, 50)
        return clone
