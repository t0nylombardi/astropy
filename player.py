import pygame

from circleshape import CircleShape
from constants import LINE_WIDTH, PLAYER_RADIUS, PLAYER_SPEED, PLAYER_TURN_SPEED


class Player(CircleShape):
    """Player-controlled ship represented as a rotating triangle."""

    def __init__(self, x: float, y: float) -> None:
        """Create a player ship at `(x, y)` with the default facing direction."""
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation: float = 180

    def triangle(self):
        """Return the three vertices that define the ship polygon."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5

        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface):
        """Draw the ship as an outlined triangle."""
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt: float):
        """Rotate the ship based on elapsed time and turn speed."""
        self.rotation += int(PLAYER_TURN_SPEED * dt)

    def move(self, dt: float) -> None:
        """Move the ship forward or backward along its current heading."""
        unit_vector = pygame.Vector2(0, 1)

        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt

        self.position += rotated_with_speed_vector

    def update(self, dt: float) -> None:
        """Read movement keys and apply rotation and translation updates."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
