import pygame, player
from pygame.locals import *

class Wall:
    _GAP = 180
    _HEIGHT = 60
    _COLOUR = ((101, 67, 33))
    _SPEED = 0

    def __init__(self, width: int):
        import random

        self._surface = pygame.Surface((width, Wall._HEIGHT))
        self._surface.fill(Wall._COLOUR)

        self._pos_x = random.randint(Wall._GAP, width - Wall._GAP) # important that even at the edges the gap is consistent
        self._pos_y = 0 # shifted down per tick as necessary

        self._gap_rect = None # the gap coords
        self._scored = False # if the wall has been scored on, or passed once by the player

    def blit(self, screen: 'pygame.Surface'):
        self._pos_y += Wall._SPEED

        left_rect = screen.blit(self._surface, (-screen.get_width() + self._pos_x, self._pos_y))
        right_rect = screen.blit(self._surface, (left_rect.right + Wall._GAP, self._pos_y))

        self._gap_rect = pygame.rect.Rect(left_rect.right, left_rect.top, Wall._GAP, Wall._HEIGHT)

    def enough_space(self):
        return self._pos_y > Wall._HEIGHT * 4 # space between each wall

    def is_off_screen(self, screen: 'pygame.Surface'):
        return self._pos_y > screen.get_height()

    def is_half_passed_gap(self, player: 'player.Player'):
        if not self._scored:
            self._scored = player.is_half_past_rect(self._gap_rect)
            if self._scored:
                return True
        else:
            return False # return false after the first score check

    def has_player_collided(self, player: 'player.Player'):
        if self._scored: # prevent collision checks if we already passed it, intended to be forgiving because the spacing is tight
            return False

        return player.has_collided(self._gap_rect) # use gap_rect to know the outer bounds where the rect exists

    @staticmethod
    def set_speed(speed: int):
        Wall._SPEED = speed
