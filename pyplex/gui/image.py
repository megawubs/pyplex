import pygame.image, pygame.display

class image:
    def __init__(self, picture):
        # pygame.init()
        self.picture = pygame.image.load(picture)
        self.picture = pygame.transform.scale(self.picture,(1280,1024))

    def set(self):
        # pygame.mouse.set_visible(False)
        pygame.display.set_mode(self.picture.get_size())
        main_surface = pygame.display.get_surface()
        main_surface.blit(self.picture, (0, 0))
        pygame.display.update()