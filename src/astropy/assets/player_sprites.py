import pygame


class PlayerSpriteSheet:
    """Loads and stores player ship sprites."""

    SHIP_RECT = pygame.Rect(0, 0, 95, 95)

    def __init__(self, path: str) -> None:  # noqa: D107
        self.sheet = pygame.image.load(path).convert_alpha()

    def get(self) -> pygame.Surface:
        """Get the player ship sprite."""
        surface = pygame.Surface(self.SHIP_RECT.size, pygame.SRCALPHA)

        surface.blit(self.sheet, (0, 0), self.SHIP_RECT)

        return surface
