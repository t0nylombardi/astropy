import random

import pygame


class AsteroidSpriteSheet:
    """Provides asteroid sprites from the sprite sheet."""

    def __init__(self, path: str) -> None:
        """Load the sprite sheet and define sprite rectangles by asteroid size."""
        self.sheet = pygame.image.load(path).convert_alpha()

        self.sprites: dict[str, list[pygame.Rect]] = {
            "large": [
                pygame.Rect(0, 0, 96, 96),
                pygame.Rect(96, 0, 96, 96),
                pygame.Rect(192, 0, 96, 96),
            ],
            "medium": [
                pygame.Rect(0, 96, 64, 64),
                pygame.Rect(64, 96, 64, 64),
                pygame.Rect(128, 96, 64, 64),
            ],
            "small": [
                pygame.Rect(0, 160, 32, 32),
                pygame.Rect(32, 160, 32, 32),
                pygame.Rect(64, 160, 32, 32),
            ],
        }

    def get_random(self, size: str) -> pygame.Surface:
        """Return a random sprite surface for the requested asteroid size."""
        rect = random.choice(self.sprites[size])

        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        surface.blit(self.sheet, (0, 0), rect)

        return surface
