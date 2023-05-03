import pygame, pathlib
from pygame.locals import *

class Player:
    _ASSETS_PATH = pathlib.Path(__file__).parent.parent.joinpath("assets")

    def __init__(self, screen: 'pygame.Surface'):
        source = pygame.image.load(pathlib.Path(Player._ASSETS_PATH, "bunny.png"))
        self._player = pygame.transform.smoothscale(source, (source.get_width() / 10, source.get_height() / 10))
        self._pos_x = (screen.get_width() - self._player.get_width()) / 2
        self._pos_y = screen.get_height() - self._player.get_height()

        self._facing = "LEFT"

    def blit(self, screen: 'pygame.Surface'):
        keys_pressed = pygame.key.get_pressed()
        speed = 20 if keys_pressed[K_LSHIFT] else 4

        if keys_pressed[K_a]:
            self._pos_x -= speed
            if self._facing == "RIGHT":
                self._player = pygame.transform.flip(self._player, True, False)
                self._facing = "LEFT"
        if keys_pressed[K_d]:
            self._pos_x += speed
            if self._facing == "LEFT":
                self._player = pygame.transform.flip(self._player, True, False)
                self._facing = "RIGHT"
        if keys_pressed[K_w]:
            self._pos_y -= speed
        if keys_pressed[K_s]:
            self._pos_y += speed

        screen.blit(self._player, (self._pos_x, self._pos_y))

    def is_half_past_rect(self, rect: 'pygame.rect.Rect'):
        player_between_x = self._pos_x > rect.left and self._pos_x + self._player.get_width() < rect.right
        player_passed_mid_y = self._pos_y <= rect.centery

        return player_between_x and player_passed_mid_y

    def has_collided(self, rect: 'pygame.rect.Rect'):
        wall_collided_x = self._pos_x <= rect.left or self._pos_x + self._player.get_width() >= rect.right
        wall_collided_y = self._pos_y <= rect.bottom # dont need to check for other coord, since if head touches its collided thats enough

        return wall_collided_x and wall_collided_y
