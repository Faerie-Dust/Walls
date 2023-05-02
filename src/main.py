import pygame, pathlib
from pygame.locals import *

ASSETS_PATH = pathlib.Path(__file__).parent.parent.joinpath("assets")

def create_wall(screen: 'pygame.Surface'):
    pass


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((854, 480))
    playerSource = pygame.image.load(pathlib.Path(ASSETS_PATH, "bunny.png"))
    clock = pygame.time.Clock()
    running = True
    
    player = pygame.transform.smoothscale(playerSource, (playerSource.get_width() / 10, playerSource.get_height() / 10))
    playerX = screen.get_width() / 2
    playerY = screen.get_height() - player.get_width()
    i = "left"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        playerKeys = pygame.key.get_pressed()
        speed = 4
        
        if playerKeys[pygame.K_LSHIFT]:
            speed = 8
        if playerKeys[pygame.K_a]:
            playerX -= speed
            if i == "right":
                player = pygame.transform.flip(player, True, False)
                i = "left"
        if playerKeys[pygame.K_d]:
            playerX += speed
            if i == "left":
                player = pygame.transform.flip(player, True, False)
                i = "right"
        if playerKeys[pygame.K_w]:
            playerY -= speed
        if playerKeys[pygame.K_s]:
            playerY += speed
        
        
        screen.fill((0, 0, 0))
        screen.blit(player, (playerX, playerY))
        pygame.display.flip()
        
        clock.tick(60)
                
    pygame.quit()