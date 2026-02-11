from typing import ClassVar, Self

import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: ClassVar[tuple[pygame.sprite.AbstractGroup, ...]] = ()

    def __init__(self, x: float, y: float, radius: int) -> None:
        super().__init__(*self.containers)

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        # must override
        pass

    def collides_with(self, other: Self) -> bool:
        return self.position.distance_to(other.position) < (self.radius + other.radius)

    def update(self, dt: float) -> None:
        # must override
        pass
