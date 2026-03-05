import sys
from typing import Any

import pygame

from astropy.core.config import Config
from astropy.entities.asteroid import Asteroid
from astropy.entities.asteroid_field import AsteroidField
from astropy.entities.physics_body import PhysicsBody
from astropy.entities.player import Player
from astropy.entities.shot import Shot
from astropy.logger import log_event, log_state


class Game:
    """Manage the initialization, main loop, and shutdown of the Astropy game."""

    FPS = 60

    def __init__(self) -> None:
        """Initialize pygame, the display surface, and all entity groups."""
        pygame.init()

        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self._setup_groups()
        self._register_entity_containers()
        self._create_entities()

    def _setup_groups(self) -> None:
        self.updatable: pygame.sprite.Group[Any] = pygame.sprite.Group()
        self.drawable: pygame.sprite.Group[Any] = pygame.sprite.Group()
        self.asteroids: pygame.sprite.Group[Any] = pygame.sprite.Group()
        self.shots: pygame.sprite.Group[Any] = pygame.sprite.Group()

    def _register_entity_containers(self) -> None:
        Player.containers = (self.updatable, self.drawable)

        Asteroid.containers = (
            self.asteroids,
            self.updatable,
            self.drawable,
        )

        AsteroidField.containers = (self.updatable,)
        Shot.containers = (self.shots, self.drawable, self.updatable)

    def _create_entities(self) -> None:
        self.player = Player(
            Config.SCREEN_WIDTH / 2,
            Config.SCREEN_HEIGHT / 2,
        )

        AsteroidField(
            Config.SCREEN_WIDTH,
            Config.SCREEN_HEIGHT,
        )

    def run(self) -> None:
        """Run _process_events while the game is active."""
        while self._process_events():
            dt = self.clock.tick(self.FPS) / 1000.0

            # expose attributes as locals so log_state can see them
            updatable = self.updatable
            drawable = self.drawable
            asteroids = self.asteroids
            shots = self.shots
            screen = self.screen

            log_state()

            self._update(dt)
            self._render()

        pygame.quit()

    def _process_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

        return True

    def _update(self, dt: float) -> None:
        self.updatable.update(dt)

        if any(asteroid.collides_with(self.player) for asteroid in self.asteroids):
            log_event("player_hit")
            print("Game over!")
            sys.exit()

    def _render(self) -> None:
        self.screen.fill((0, 0, 0))

        for sprite in self.drawable:
            if isinstance(sprite, PhysicsBody):
                sprite.draw(self.screen)

        pygame.display.flip()
