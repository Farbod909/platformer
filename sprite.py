import pygame
from helpers import adjust_scroll


class GroupWithCamera(pygame.sprite.Group):
    def draw(self, surface, camera_scroll):
        """draw all sprites onto the surface
        Group.draw(surface): return None
        Draws all of the member sprites onto the given surface.
        """
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(
                spr.image, spr.rect.move(adjust_scroll(camera_scroll))
            )
        self.lostsprites = []


class GroupSingleWithCamera(pygame.sprite.GroupSingle):
    def draw(self, surface, camera_scroll):
        """draw all sprites onto the surface
        Group.draw(surface): return None
        Draws all of the member sprites onto the given surface.
        """
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(
                spr.image, spr.rect.move(adjust_scroll(camera_scroll))
            )
        self.lostsprites = []
