class Camera:
    def __init__(self, display_size):
        self.position = [0, 0]
        self.display_size = display_size
        self.following_sprite = None

    def follow(self, sprite):
        self.following_sprite = sprite

    def update(self):
        if self.following_sprite is None:
            print("Camera has not been set to follow any sprite.")
            raise SystemExit

        diff_x = (
            self.following_sprite.rect.centerx
            - self.position[0]
            - (self.display_size[0] / 2)
        ) / 20
        diff_y = (
            self.following_sprite.rect.centery
            - self.position[1]
            - (self.display_size[1] / 2)
        ) / 20
        self.position[0] += diff_x
        self.position[1] += diff_y
