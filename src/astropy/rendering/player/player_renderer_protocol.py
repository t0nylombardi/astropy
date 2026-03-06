from __future__ import annotations

from typing import Protocol

import pygame


class PlayerRendererProtocol(Protocol):
    """
    Interface for player rendering strategies.

    Implementations are responsible for drawing the player and
    updating any visual animation state such as rotation.
    """

    def draw(self, screen: pygame.Surface, position: pygame.Vector2, rotation: float) -> None:
        """Render the player at the given position."""
        ...

    def update(self, dt: float) -> None:
        """Update animation state."""
        ...

    def clone(self) -> PlayerRendererProtocol:
        """
        Return a new renderer instance for player fragments.

        Splitting players must not share renderer state.
        """
        ...
