import pygame
from camera import Camera
from colors import SKYBLUE
from pygame.locals import *


class Game:
    WINDOW_SIZE = (600, 400)
    CANVAS_SIZE = (300, 200)

    def __init__(self):
        pygame.init()
        Game.MONITOR_SIZE = [
            pygame.display.Info().current_w,
            pygame.display.Info().current_h,
        ]
        self.screen = pygame.display.set_mode(Game.WINDOW_SIZE)
        self.canvas = pygame.Surface(Game.CANVAS_SIZE)
        self.background = self.make_background()
        self.camera = Camera(self.canvas.get_size())
        pygame.display.set_caption("Platformer")
        self.spritegroups = {}

    def make_background(self):
        """Create a background surface.
        
        Return:
            Surface: The background.
        """
        background = pygame.Surface((self.canvas.get_width(), self.canvas.get_height()))
        background = background.convert()
        background.fill(SKYBLUE)
        return background

    def add_sprite(self, sprite):
        """Add a sprite to the game.
        
        This adds a `game` property to each sprite in the game
        so the sprite can access the game's functions and properties
        such as the state.

        Args:
            sprite (Sprite): The sprite to be added to the game.
        
        Returns:
            Sprite: the same sprite, slightly modified.
        """
        sprite.game = self
        return sprite

    def add_sprites(self, *sprites):
        """Adds several sprites to the game.
        
        This adds a `game` property to each sprite in the game
        so the sprite can access the game's functions and properties
        such as the state.
        """
        for sprite in sprites:
            self.add_sprite(sprite)

    def add_spritegroups(self, spritegroups_dict):
        """Adds references to Sprites and Game so they can access eachother.

        Creates a reference to this Game instance in all sprites and
        creates a reference to all spritegroups in this Game instance.

        Args:
            spritegroups_dict (Dict[str, Group]): A dictionary of the
                spritegroups in the game where the key is the name of each
                spritegroup and the value is a reference to the Group.
        """
        self.spritegroups.update(spritegroups_dict)
        for spritegroup in self.spritegroups.values():
            for sprite in spritegroup.sprites():
                self.add_sprite(sprite)

    def initial_frame(self):
        self.canvas.blit(self.background, (0, 0))

        self.screen.blit(pygame.transform.scale(self.canvas, Game.WINDOW_SIZE), (0, 0))
        pygame.display.update()

    def update_frame(self):
        """Clear sprites from screen and re-render them based on new values
        
        Blits the background onto all sprites in the game and then
        blits the sprites with new locations onto the screen again.
        """
        self.canvas.blit(self.background, (0, 0))
        for spritegroup in self.spritegroups.values():
            spritegroup.update()
            spritegroup.draw(self.canvas, self.camera.position)

        self.screen.blit(pygame.transform.scale(self.canvas, Game.WINDOW_SIZE), (0, 0))
        pygame.display.update()

    def startloop(self):
        player = self.spritegroups["playersprite"].sprite

        clock = pygame.time.Clock()
        self.camera.follow(player)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        player.moving_right = True
                    if event.key == K_LEFT:
                        player.moving_left = True
                    if event.key == K_UP:
                        player.jump()
                if event.type == KEYUP:
                    if event.key == K_RIGHT:
                        player.moving_right = False
                    if event.key == K_LEFT:
                        player.moving_left = False

            self.camera.update()
            self.update_frame()

            clock.tick(60)
