import os

# mario.py
WIN_WIDTH, WIN_HEIGHT = 800, 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = '#000000'
FPS = 60
SCREEN_START = (0, 0)
FILE_DIR = os.path.dirname(__file__)
FILE_PATH = '%s/levels/1.txt' % FILE_DIR
MUSIC_PATH = 'audio/level_music.wav'

# monsters.py
MONSTER_WIDTH, MONSTER_HEIGHT, MONSTER_COLOR = 32, 32, '#2111FF'
ICON_DIR = os.path.dirname(__file__)
ANIMATION_MONSTER_HORIZONTAL = [('%s/monsters/fire1.png' % ICON_DIR), ('%s/monsters/fire2.png' % ICON_DIR)]

# blocks.py
PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR = 32, 32, '#000000'
# ICON_DIR = os.path.dirname(__file__)
ANIMATION_BLOCK_TELEPORT = [('%s/blocks/portal1.png' % ICON_DIR), ('%s/blocks/portal2.png' % ICON_DIR)]
ANIMATION_PRINCESS = [('%s/blocks/princess_l.png' % ICON_DIR), ('%s/blocks/princess_r.png' % ICON_DIR)]
PATH_BLOCK_PLATFORM = '%s/blocks/platform.png' % ICON_DIR
PATH_BLOCK_DIE = '%s/blocks/dieBlock.png' % ICON_DIR

# player.py
MOVE_SPEED = 4
MOVE_EXTRA_SPEED = 1.5
WIDTH, HEIGHT, COLOR = 30, 38, '#888888'
JUMP_POWER, JUMP_EXTRA_POWER, GRAVITY = 6, 1, 0.2
ANIMATION_DELAY, ANIMATION_SUPER_SPEED_DELAY = 0.05, 0.025

PLATFORM_IMAGE = "%s/blocks/platform.png" % ICON_DIR

ANIMATION_LEFT = [('%s/mario/l1.png' % ICON_DIR),
                  ('%s/mario/l2.png' % ICON_DIR),
                  ('%s/mario/l3.png' % ICON_DIR),
                  ('%s/mario/l4.png' % ICON_DIR),
                  ('%s/mario/l5.png' % ICON_DIR)
                  ]

ANIMATION_RIGHT = [('%s/mario/r1.png' % ICON_DIR),
                   ('%s/mario/r2.png' % ICON_DIR),
                   ('%s/mario/r3.png' % ICON_DIR),
                   ('%s/mario/r4.png' % ICON_DIR),
                   ('%s/mario/r5.png' % ICON_DIR)
                   ]

ANIMATION_JUMP = [('%s/mario/j.png' % ICON_DIR, ANIMATION_DELAY)]
ANIMATION_JUMP_LEFT = [('%s/mario/jl.png' % ICON_DIR, ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [('%s/mario/jr.png' % ICON_DIR, ANIMATION_DELAY)]
ANIMATION_STAY = [('%s/mario/0.png' % ICON_DIR, ANIMATION_DELAY)]

# pyganim.py
PLAYING, PAUSED, STOPPED = 'playing', 'paused', 'stopped'
# These are used in PygAnimation.anchor():
NORTH, SOUTH, WEST, EAST, CENTER = 'north', 'south', 'west', 'east', 'center'
NORTH_WEST, SOUTH_WEST, NORTH_EAST, SOUTH_EAST = 'northwest', 'southwest', 'northeast', 'southeast'

# popup_menu.py
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
HIGHLIGHTED_GREEN = (0, 200, 0)
HIGHLIGHTED_RED = (200, 0, 0)
