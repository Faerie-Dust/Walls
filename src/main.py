import pygame, pathlib
from pygame.locals import *
from wall import Wall as Wall
from player import Player as Player

SCORE = 0
WALLS = []
WIDTH, HEIGHT = 854, 480
ASSETS_PATH = pathlib.Path(__file__).parent.parent.joinpath("assets")

def render_walls(screen: 'pygame.Surface'):
    global WALLS

    wall_exists = len(WALLS) > 0

    if (wall_exists and WALLS[-1].enough_space()) or not wall_exists:
        WALLS.append(Wall(WIDTH)) # create a new wall if there's enough space from the previous wall OR if there isn't a wall at all

    for wall in WALLS:
        if wall.is_off_screen(screen):
            WALLS.remove(wall)
            continue

        wall.blit(screen)

if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Player(screen)

    running = True
    lost = False
    final_render = False

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        Wall.set_speed(1 * (1 + SCORE)) # scales with score :D

        render_walls(screen)
        player.blit(screen)

        for wall in WALLS:
            if wall.has_player_collided(player):
                lost = True
            if wall.is_half_passed_gap(player):
                SCORE += 1

        font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
        text = font.render(f"Score: {SCORE}", True, (0, 0, 0))

        screen.blit(text, (0, screen.get_height() - text.get_height()))

        if lost:
            game_over_text = font.render(f"Game over! Your score was {SCORE}!", True, (0, 0, 0))
            screen.blit(game_over_text, ((screen.get_width() - game_over_text.get_width()) / 2, (screen.get_height() - game_over_text.get_height()) / 2))

            if not final_render:
                pygame.display.flip() # final flip, no more rendering past this point
                final_render = True

        if not lost: # prevent rendering after loss, we handle the last flip ourselves
            pygame.display.flip()

        clock.tick(60)
