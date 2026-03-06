import random

import pygame


class AsteroidSpriteSheet:
    """Provides asteroid sprites from the sprite sheet."""

    ROW_HEIGHT = 48
    ROW_START_Y = 1
    ROW_COUNT = 12
    LARGE_RECT = pygame.Rect(29, 0, 80, 48)
    MEDIUM_RECT = pygame.Rect(145, 0, 24, 32)
    SMALL_RECT = pygame.Rect(221, 0, 16, 16)

    def __init__(self, path: str) -> None:
        """Load sprite sheet and build asteroid sprite rectangles per size bucket."""
        self.sheet = pygame.image.load(path).convert_alpha()

        row_offsets = [
            self.ROW_START_Y + self.ROW_HEIGHT * row_index
            for row_index in range(self.ROW_COUNT)
        ]

        self.sprites: dict[str, list[pygame.Rect]] = {
            "large": [self.LARGE_RECT.move(0, y) for y in row_offsets],
            "medium": [self.MEDIUM_RECT.move(0, y) for y in row_offsets],
            "small": [self.SMALL_RECT.move(0, y) for y in row_offsets],
        }

    def get_random(self, size: str) -> pygame.Surface:
        """Return a random sprite surface for the requested asteroid size."""
        rect = random.choice(self.sprites[size])

        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        surface.blit(self.sheet, (0, 0), rect)

        return surface
