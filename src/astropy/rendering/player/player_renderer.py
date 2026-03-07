import random

import pygame


class PlayerRenderer:
    """Handles visual representation of an player."""

    SPRITE_ROTATION_OFFSET = 90

    def __init__(self, sprite: pygame.Surface, radius: int) -> None:
        """Store a scaled player sprite and initialize random rotation and spin."""
        diameter = radius * 2
        self.image = pygame.transform.smoothscale(sprite, (diameter, diameter))
        self.rotation = random.uniform(0, 360)
        self.spin = random.uniform(-50, 50)

    def update(self, dt: float) -> None:
        """Advance the renderer rotation by elapsed time."""
        pass

    def draw(
        self,
        screen: pygame.Surface,
        position: pygame.Vector2,
        rotation: float,
    ) -> None:
        """Rotate the cached sprite and draw it centered on `position`."""
        rotated = pygame.transform.rotate(self.image, -(rotation + 180))
        rect = rotated.get_rect(center=position)
        screen.blit(rotated, rect)
