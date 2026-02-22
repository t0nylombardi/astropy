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
        """Render the shot as a white outlined circle."""
        pygame.draw.circle(
            screen,
            "red",
            self.position,
            self.SHOT_RADIUS,
            self.LINE_WIDTH,
        )

    def update(self, dt: float) -> None:
        """Advance shotd position according to velocity and delta time."""
        self.position += self.velocity * dt
