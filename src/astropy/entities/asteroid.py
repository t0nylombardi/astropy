import pygame

from astropy.entities.physics_body import PhysicsBody


class Asteroid(PhysicsBody):
    """A moving asteroid represented as a circular game object."""

    def __init__(self, x: float, y: float, radius: int) -> None:
        """Initialize an asteroid at `(x, y)` with a given collision radius."""
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        """Render the asteroid as a white outlined circle."""
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            self.LINE_WIDTH,
        )

    def update(self, dt: float) -> None:
        """Advance asteroid position according to velocity and delta time."""
        self.position += self.velocity * dt
