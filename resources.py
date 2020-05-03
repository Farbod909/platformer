import os
import pygame


def load_image(name, colorkey=None):
    """Loads an image from the assets folder as a Surface.
    
    Args:
        name (str): The name of the image (e.g. "ball.png")
        colorkey (int or (int, int, int)): an RGB value that represents
            the pixels that should be rendered as "transparent". If -1
            is passed as this argument, the color of the top-right
            pixel will be selected.
    
    Returns:
        Surface: The image.
    """
    fullname = os.path.join("assets", "images", name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print("Cannot load image:", name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.locals.RLEACCEL)
    return image


def load_sound(name):
    """Loads a sound from the assets folder.
    
    Args:
        name (str): The name of the sound file (e.g. "explosion.wav")

    Returns:
        Sound
    """

    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join("assets", "sounds", name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print("Cannot load sound:", name)
        raise SystemExit(message)
    return sound


def load_map(map_name):
    fullpath = os.path.join("maps", map_name)
    game_map = []
    with open(fullpath) as map_txt_file:
        for row in map_txt_file.read().split("\n"):
            game_map.append(list(row))
    return game_map
