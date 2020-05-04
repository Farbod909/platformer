import math
import os
import physics
import pygame
from animations import list_from_OrderedDict
from collections import OrderedDict
from resources import load_image, load_animation_image
from saved_images import saved_images


class Tile(pygame.sprite.Sprite):
    SIZE = (16, 16)

    def __init__(self, type, grid_position):
        pygame.sprite.Sprite.__init__(self)
        if not type in saved_images:
            image = load_image(type + ".png")
            if image.get_size() != Tile.SIZE:
                print("Cannot load tile:", type)
                raise SystemExit
            saved_images[type] = image
        self.image = saved_images[type]
        self.rect = self.image.get_rect()
        self.rect.x = grid_position[0] * Tile.SIZE[0]
        self.rect.y = grid_position[1] * Tile.SIZE[1]

    def update(self):
        pass


class Player(pygame.sprite.Sprite):
    MOVEMENT_SPEED = 2
    JUMP_SPEED = 6
    ACTIONS = ["idle", "run"]

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("player.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.velocity = {"x": 0, "y": 0}
        self.moving_left = False
        self.moving_right = False
        self.air_timer = 0
        self._current_action = Player.ACTIONS[0]

        self.flip = False
        animations_path = os.path.join("assets", "animations", "player")
        self.animations = {}
        for action in Player.ACTIONS:
            action_animations_path = os.path.join(animations_path, action)
            self.animations[action] = {
                os.path.splitext(item)[0]: load_animation_image(
                    "player", action, item, -1
                )
                for item in os.listdir(action_animations_path)
                if os.path.isfile(os.path.join(action_animations_path, item))
            }
        animation_sequence_setup = {
            "idle": OrderedDict([("idle_0", 7), ("idle_1", 7), ("idle_2", 40)]),
            "run": OrderedDict([("run_0", 7), ("run_1", 7)]),
        }
        self.animation_sequence = {
            key: list_from_OrderedDict(value)
            for key, value in animation_sequence_setup.items()
        }
        self.current_animation_frame = 0
        self.image = self.animations[self.current_action][
            self.animation_sequence[self.current_action][self.current_animation_frame]
        ]

    @property
    def current_action(self):
        return self._current_action

    @current_action.setter
    def current_action(self, value):
        if self._current_action != value:
            if value in Player.ACTIONS:
                self._current_action = value
                self.current_animation_frame = 0
            else:
                raise ValueError(
                    "%s is not a valid action for %s" % (value, self.__class__.__name__)
                )

    def update_velocity(self):
        self.velocity["x"] = 0
        if self.moving_left:
            self.velocity["x"] += -Player.MOVEMENT_SPEED
        if self.moving_right:
            self.velocity["x"] += Player.MOVEMENT_SPEED
        self.velocity["y"] += physics.GRAVITY_ACCELERATION
        if self.velocity["y"] >= 3:
            self.velocity["y"] = 3

    def move(self, tilesprites):
        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        self.rect.x += int(math.ceil(self.velocity["x"]))
        colliding_tiles = pygame.sprite.spritecollide(self, tilesprites, False)
        for tile in colliding_tiles:
            if self.velocity["x"] > 0:
                self.rect.right = tile.rect.left
                collision_types["right"] = True
            elif self.velocity["x"] < 0:
                self.rect.left = tile.rect.right
                collision_types["left"] = True
        self.rect.y += int(math.ceil(self.velocity["y"]))
        colliding_tiles = pygame.sprite.spritecollide(self, tilesprites, False)
        for tile in colliding_tiles:
            if self.velocity["y"] > 0:
                self.rect.bottom = tile.rect.top
                collision_types["bottom"] = True
            elif self.velocity["y"] < 0:
                self.rect.top = tile.rect.bottom
                collision_types["top"] = True
        return collision_types

    def update(self):
        tilesprites = self.game.spritegroups["tilesprites"]
        self.update_velocity()
        collisions = self.move(tilesprites)

        if collisions["bottom"] == True:
            self.hit_ground()
        else:
            self.in_air()

        if collisions["top"] == True:
            self.hit_ceiling()

        if self.velocity["x"] > 0:
            self.current_action = "run"
            self.flip = False
        if self.velocity["x"] < 0:
            self.current_action = "run"
            self.flip = True
        if self.velocity["x"] == 0:
            self.current_action = "idle"

        self.image = self.animations[self.current_action][
            self.animation_sequence[self.current_action][self.current_animation_frame]
        ]

        # PERFORMANCE: cache flipped image to prevent pygame.transform operation every frame
        self.image = pygame.transform.flip(self.image, self.flip, False)

        self.current_animation_frame += 1

        if self.current_animation_frame >= len(
            self.animation_sequence[self.current_action]
        ):
            self.current_animation_frame = 0

    def hit_ground(self):
        self.air_timer = 0
        self.velocity["y"] = 0

    def hit_ceiling(self):
        self.velocity["y"] = 0

    def in_air(self):
        self.air_timer += 1

    def jump(self):
        if self.air_timer == 0:
            self.velocity["y"] = -Player.JUMP_SPEED
