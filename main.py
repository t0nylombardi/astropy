"""Main module for the Asteroids game.

This module initializes pygame, creates game objects (player, asteroids, and
fields), and runs the main loop that processes events, updates state, and
renders the game.
"""

import sys
from collections.abc import Iterable
from typing import Any

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player

VERSION: str = pygame.version.ver
FPS: int = 60


def process_events() -> bool:
    """Handle pygame input events and return `False` when the game should exit."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        return not (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)

    return True


def update(
    player: Player,
    updatable: pygame.sprite.AbstractGroup[Any],
    asteroids: Iterable[object],
    dt: float,
) -> None:
    """Advance game state and exit if the player collides with an asteroid."""
    updatable.update(dt)

    if any(
        isinstance(asteroid, Asteroid) and asteroid.collides_with(player) for asteroid in asteroids
    ):
        log_event("player_hit")
        print("Game over!")
        sys.exit()


def render(screen: pygame.Surface, drawable: Iterable[object]) -> None:
    """Clear the screen, draw all circle sprites, and present the frame."""
    screen.fill((0, 0, 0))

    for sprite in drawable:
        if isinstance(sprite, CircleShape):
            sprite.draw(screen)

    pygame.display.flip()


def main() -> None:
    """Initialize and run the Asteroids game loop."""
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    print(f"Starting Asteroids with pygame version: {VERSION}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    updatable: pygame.sprite.Group[Any] = pygame.sprite.Group()
    drawable: pygame.sprite.Group[Any] = pygame.sprite.Group()
    asteroids: pygame.sprite.Group[Any] = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)

    player = Player(
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT / 2,
    )

    AsteroidField()

    while process_events():
        dt = clock.tick(FPS) / 1000.0

        log_state()
        update(player, updatable, asteroids, dt)
        render(screen, drawable)

    pygame.quit()


if __name__ == "__main__":
    main()
