from __future__ import annotations

from typing import Protocol

import pygame
from pygame.math import Vector2


class AsteroidRendererProtocol(Protocol):
    """
    Interface for asteroid rendering strategies.

    Implementations are responsible for drawing the asteroid and
    updating any visual animation state such as rotation.
    """

    def draw(self, screen: pygame.Surface, position: Vector2) -> None:
        """Render the asteroid at the given position."""
        ...

    def update(self, dt: float) -> None:
        """Update animation state."""
        ...

    def clone(self) -> AsteroidRendererProtocol:
        """
        Return a new renderer instance for asteroid fragments.

        Splitting asteroids must not share renderer state.
        """
        ...
