import random

import pygame


class AsteroidRenderer:
    """Handles visual representation of an asteroid."""

    def __init__(self, sprite: pygame.Surface) -> None:
        """Store the base sprite and initialize random rotation and spin."""
        self.image = sprite
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
        return AsteroidRenderer(self.image)
