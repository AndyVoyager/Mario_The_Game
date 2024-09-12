import pygame.display
from pygame import *
import pyganim
import blocks
import monsters
from popup_menu import ask_to_play_again
from settings import MOVE_SPEED, MOVE_EXTRA_SPEED, WIDTH, HEIGHT, COLOR, JUMP_POWER, JUMP_EXTRA_POWER, GRAVITY, \
    ANIMATION_DELAY, ANIMATION_SUPER_SPEED_DELAY, ANIMATION_RIGHT, ANIMATION_LEFT, ANIMATION_JUMP_LEFT, \
    ANIMATION_JUMP_RIGHT, ANIMATION_JUMP, ANIMATION_STAY, SCREEN_START


class Player(sprite.Sprite):
    def __init__(self, x, y):
        # sprite.Sprite.__init__(self)
        super().__init__()
        # movement speed: 0 - standing still
        self.x_val = 0
        # vertical movement speed
        self.y_val = 0
        # Initial X position, useful when replaying the level
        self.start_x = x
        self.start_y = y
        # Am I on the ground?
        self.on_ground = False
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        # Rectangular object
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        # make the background transparent
        self.image.set_colorkey(Color(COLOR))

        # Animation of moving left, using list comprehension to optimize the code
        bolt_anim = [(anim, ANIMATION_DELAY) for anim in ANIMATION_LEFT]
        bolt_anim_super_speed = [(anim, ANIMATION_SUPER_SPEED_DELAY) for anim in ANIMATION_LEFT]

        self.bolt_anim_left = pyganim.PygAnimation(bolt_anim)
        self.bolt_anim_left.play()
        self.bolt_anim_left_super_speed = pyganim.PygAnimation(bolt_anim_super_speed)
        self.bolt_anim_left_super_speed.play()

        # Animation of moving right, using list comprehension to optimize the code
        self.bolt_anim_right = pyganim.PygAnimation([(anim, ANIMATION_DELAY) for anim in ANIMATION_RIGHT])
        self.bolt_anim_right.play()
        self.bolt_anim_right_super_speed = pyganim.PygAnimation([(anim, ANIMATION_SUPER_SPEED_DELAY) for anim in
                                                                 ANIMATION_RIGHT])
        self.bolt_anim_right_super_speed.play()

        self.bolt_anim_stay = pyganim.PygAnimation(ANIMATION_STAY)
        self.bolt_anim_stay.play()

        # By default, we are standing still
        self.bolt_anim_stay.blit(self.image, SCREEN_START)

        self.bolt_anim_jump_left = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.bolt_anim_jump_left.play()

        self.bolt_anim_jump_right = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.bolt_anim_jump_right.play()

        self.bolt_anim_jump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.bolt_anim_jump.play()
        self.winner = False

    def update(self, left, right, up, running, platforms):

        if up:
            # Jump only if we can push off the ground
            if self.on_ground:
                self.y_val = - JUMP_POWER
                # if there is acceleration and we are moving
                if running and (left or right):
                    # then jump higher
                    self.y_val -= JUMP_EXTRA_POWER
                self.image.fill(Color(COLOR))
                self.bolt_anim_jump.blit(self.image, SCREEN_START)

        if left:
            # Left = x - n
            self.x_val = - MOVE_SPEED
            self.image.fill(Color(COLOR))
            # if running
            if running:
                # then move faster
                self.x_val -= MOVE_EXTRA_SPEED
                # and if not jumping
                if not up:
                    # then display fast animation
                    self.bolt_anim_left_super_speed.blit(self.image, SCREEN_START)
            # if not running
            else:
                # and not jumping
                if not up:
                    # display movement animation
                    self.bolt_anim_left.blit(self.image, SCREEN_START)
            # if jumping
            if up:
                # display jump animation
                self.bolt_anim_jump_left.blit(self.image, SCREEN_START)

        if right:
            # Right = x + n
            self.x_val = MOVE_SPEED
            self.image.fill(Color(COLOR))
            if running:
                self.x_val += MOVE_EXTRA_SPEED
                if not up:
                    self.bolt_anim_right_super_speed.blit(self.image, SCREEN_START)
            else:
                if not up:
                    self.bolt_anim_right.blit(self.image, SCREEN_START)
            if up:
                self.bolt_anim_jump_right.blit(self.image, SCREEN_START)

        # stand still when there are no instructions to move
        if not (left or right):
            self.x_val = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.bolt_anim_stay.blit(self.image, SCREEN_START)

        if not self.on_ground:
            self.y_val += GRAVITY

        # We don't know when we're on the ground
        self.on_ground = False
        self.rect.y += self.y_val
        self.collide(0, self.y_val, platforms)
        # Move position by x_val
        self.rect.x += self.x_val
        self.collide(self.x_val, 0, platforms)

    def collide(self, x_val, y_val, platforms):
        for platform in platforms:
            # If there is a collision with the player
            if sprite.collide_rect(self, platform):
                # If the collided block is blocks.BlockDie or Monster
                if isinstance(platform, blocks.BlockDie) or isinstance(platform, monsters.Monster):
                    # We die
                    self.die()
                elif isinstance(platform, blocks.BlockTeleport):
                    self.teleporting(platform.go_x, platform.go_y)
                # If we touched the princess
                elif isinstance(platform, blocks.Princess):
                    # WE WON!
                    self.winner = True
                    # if self.winner:
                    #     player_answer = ask_to_play_again(pygame.display.get_surface())
                    #     if player_answer:
                    #         self.winner = False
                    #         self.die()
                    #     else:
                    #         raise SystemExit("QUIT")
                else:
                    # If moving to the right
                    if x_val > 0:
                        # then don't move right
                        self.rect.right = platform.rect.left
                    # If moving left
                    if x_val < 0:
                        # then don't move left
                        self.rect.left = platform.rect.right
                    # If falling down
                    if y_val > 0:
                        # then don't fall down
                        self.rect.bottom = platform.rect.top
                        # and land on something solid
                        self.on_ground = True
                        # and the falling energy disappears
                        self.y_val = 0
                    # If moving up
                    if y_val < 0:
                        # then don't move up
                        self.rect.top = platform.rect.bottom
                        # and the jump energy disappears
                        self.y_val = 0

    def teleporting(self, go_x, go_y):
        self.rect.x = go_x
        self.rect.y = go_y

    def die(self):
        # Wait
        time.wait(500)
        # Move to the initial coordinates
        self.teleporting(self.start_x, self.start_y)
