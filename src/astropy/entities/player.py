from collections.abc import Callable
from typing import ClassVar

import pygame

from astropy.assets.player_sprites import PlayerSpriteSheet
from astropy.entities.physics_body import PhysicsBody
from astropy.entities.shot import Shot
from astropy.rendering.player.player_renderer import PlayerRenderer
from astropy.rendering.player.player_renderer_protocol import PlayerRendererProtocol

RendererFactory = Callable[[int], PlayerRendererProtocol]


class Player(PhysicsBody):
    """Player-controlled ship represented as a rotating sprite."""

    PLAYER_RADIUS: ClassVar[int] = 20
    PLAYER_TURN_SPEED: ClassVar[int] = 300
    PLAYER_SPEED: ClassVar[int] = 200
    PLAYER_SHOOT_SPEED: ClassVar[int] = 500
    PLAYER_SHOOT_COOLDOWN_SECONDS: ClassVar[float] = 0.3
    SPRITES: ClassVar[PlayerSpriteSheet]

    def __init__(
        self,
        x: float,
        y: float,
    ) -> None:
        """Create a player ship at `(x, y)` with the default facing direction."""
        super().__init__(x, y, self.PLAYER_RADIUS)

        if not hasattr(self.__class__, "SPRITES"):
            self.__class__.SPRITES = PlayerSpriteSheet("assets/spaceship-sprite.png")

        sprite = self.SPRITES.get()
        self.renderer = PlayerRenderer(sprite, self.PLAYER_RADIUS)
        self.rotation: float = 180
        self.shot_cooldown_timer: float = 0

    def draw(self, screen: pygame.Surface):
        """
        Draw the player using its renderer.

        Args:
            screen: Target pygame surface.
        """
        self.renderer.draw(screen, self.position, self.rotation)

    def rotate(self, dt: float):
        """Rotate the ship based on elapsed time and turn speed."""
        self.rotation += int(self.PLAYER_TURN_SPEED * dt)

    def move(self, dt: float) -> None:
        """Move the ship forward or backward along its current heading."""
        unit_vector = pygame.Vector2(0, 1)

        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * self.PLAYER_SPEED * dt

        self.position += rotated_with_speed_vector

    def shoot(self) -> None:
        """Create a shot moving in the direction the player is facing."""
        if self.shot_cooldown_timer > 0:
            return
        self.shot_cooldown_timer = self.PLAYER_SHOOT_COOLDOWN_SECONDS

        shot = Shot(self.position.x, self.position.y)
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = direction * self.PLAYER_SHOOT_SPEED

    def update(self, dt: float) -> None:
        """Read movement keys and apply rotation and translation updates."""
        self.shot_cooldown_timer -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        # self.renderer.update(dt)
