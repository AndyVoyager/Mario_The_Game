__author__ = "AndyVoyager"

from pygame import *
from settings import MONSTER_WIDTH, MONSTER_HEIGHT, MONSTER_COLOR, ANIMATION_MONSTER_HORIZONTAL, SCREEN_START
import pyganim


class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, max_length_left, max_length_up):
        super().__init__()
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.start_x = x
        self.start_y = y
        self.x_val = left
        self.y_val = up
        self.max_length_left = max_length_left
        self.max_length_up = max_length_up

        self.bolt_anim = pyganim.PygAnimation([(anim, 0.3) for anim in ANIMATION_MONSTER_HORIZONTAL])
        self.bolt_anim.play()

    def update(self, platforms):
        self.image.fill(Color(MONSTER_COLOR))
        self.bolt_anim.blit(self.image, SCREEN_START)

        self.rect.x += self.x_val
        self.rect.y += self.y_val

        self.collide(platforms)

        if abs(self.start_x - self.rect.x) > self.max_length_left:
            self.x_val = - self.x_val

        if abs(self.start_y - self.rect.y) > self.max_length_up:
            self.y_val = - self.y_val

    def collide(self, platforms):
        for platform in platforms:
            if sprite.collide_rect(self, platform) and self != platform:
                self.x_val = - self.x_val
                self.y_val = - self.y_val
