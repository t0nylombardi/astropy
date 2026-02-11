import sys

import pygame
from pygame.sprite import Group

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player

VERSION: str = pygame.version.ver
FPS: int = 60


def process_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

    return True


def update(
    player: Player,
    updatable: Group,
    asteroids: Group,
    dt: float,
) -> None:
    updatable.update(dt)

    if any(asteroid.collides_with(player) for asteroid in asteroids):
        log_event("player_hit")
        print("Game over!")
        sys.exit()


def render(screen: pygame.Surface, drawable: Group) -> None:
    screen.fill((0, 0, 0))

    for sprite in drawable:
        sprite.draw(screen)

    pygame.display.flip()


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    print(f"Starting Asteroids with pygame version: {VERSION}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

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
