from typing import ClassVar

import pygame

from astropy.entities.physics_body import PhysicsBody


class Shot(PhysicsBody):
    """Create projectile objects for player to shoot with."""

    SHOT_RADIUS: ClassVar[int] = 5

    def __init__(self, x: float, y: float) -> None:
        """Initialize shot object."""
        super().__init__(x, y, self.SHOT_RADIUS)

    def draw(self, screen: pygame.Surface) -> None:
        if self.velocity.length() == 0:
            return

        direction = self.velocity.normalize()
        laser_length = 20
        start = self.position
        end = self.position + direction * laser_length
        pygame.draw.line(screen, "green", start, end, 3)

    def update(self, dt: float) -> None:
        """Advance shotd position according to velocity and delta time."""
        self.position += self.velocity * dt
