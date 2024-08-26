import pygame
from player import *
from blocks import *
from monsters import *
from settings import WIN_WIDTH, WIN_HEIGHT, DISPLAY, BACKGROUND_COLOR, FILE_PATH, MUSIC_PATH, FPS


class Camera:
    def __init__(self, camera_fn, width, height):
        self.camera_fn = camera_fn
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_fn(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = - l + WIN_WIDTH / 2, - t + WIN_HEIGHT / 2
    # Don't move further than the left boundary
    l = min(0, l)
    # Don't move further than the right boundary
    l = max(-(camera.width - WIN_WIDTH), l)
    # Don't move further than the bottom boundary
    t = max(-(camera.height - WIN_HEIGHT), t)
    # Don't move further than the top boundary
    t = min(0, t)

    return Rect(l, t, w, h)


def load_level():
    # Declare global variables, these are the hero's coordinates
    global player_x, player_y
    level_file = open(FILE_PATH)
    line = " "
    # commands = []
    # Until we find the end of file symbol
    while line[0] != "/":
        # Read line by line
        line = level_file.readline()
        # If we find the level start symbol
        if line[0] == "[":
            # Until we find the level end symbol
            while line[0] != "]":
                # Read the level line
                line = level_file.readline()
                # If there is no level end symbol
                if line[0] != "]":
                    # Find the end of the line symbol
                    endLine = line.find("|")
                    # Add the line to the level from the beginning to the "|" symbol
                    level.append(line[0: endLine])
        # If the line is not empty
        if line[0] != "":
            # Split it into individual commands
            commands = line.split()
            # If the number of commands > 1, search for these commands
            if len(commands) > 1:
                # If the first command is "player"
                if commands[0] == "player":
                    # Record the hero's coordinates
                    player_x = int(commands[1])
                    player_y = int(commands[2])
                # If the first command is "portal", create a portal
                if commands[0] == "portal":
                    tp = BlockTeleport(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]))
                    entities.add(tp)
                    platforms.append(tp)
                    animated_entities.add(tp)
                # If the first command is "monster", create a monster
                if commands[0] == "monster":
                    mn = Monster(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                                 int(commands[5]), int(commands[6]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)


def music():
    # Initialize the mixer object
    mixer.init()
    # Specify the path to the file
    mixer.music.load(MUSIC_PATH)
    # Set the playback volume level
    mixer.music.set_volume(0.1)
    # Loop the playback cyclically
    mixer.music.play(-1)


def main():
    load_level()
    # Initialize PyGame, required line
    pygame.init()
    # Create a window
    screen = pygame.display.set_mode(DISPLAY)
    # Set the title
    pygame.display.set_caption("Super Mario")
    # Create a visible surface
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    # Fill the surface with a solid color
    bg.fill(Color(BACKGROUND_COLOR))

    music()
    # By default, stay idle
    left = right = up = running = False
    # Create a hero at (x, y) coordinates
    hero = Player(player_x, player_y)
    entities.add(hero)

    timer = pygame.time.Clock()
    # Coordinates
    x = y = 0
    # The entire row
    for row in level:
        # Each symbol
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "P":
                pr = Princess(x, y)
                entities.add(pr)
                platforms.append(pr)
                animated_entities.add(pr)

            x += PLATFORM_WIDTH  # Place platform blocks at block width
        y += PLATFORM_HEIGHT  # Same for height
        x = 0  # Start from zero on each new line

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Calculate the actual width of the level
    total_level_height = len(level) * PLATFORM_HEIGHT  # Calculate the height

    camera = Camera(camera_configure, total_level_width, total_level_height)
    # Main program loop
    while not hero.winner:
        # Process events
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit("QUIT")
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    up = True
                if event.key == K_LEFT:
                    left = True
                if event.key == K_RIGHT:
                    right = True
                if event.key == K_LSHIFT:
                    running = True

            if event.type == KEYUP:
                if event.key == K_UP:
                    up = False
                if event.key == K_RIGHT:
                    right = False
                if event.key == K_LEFT:
                    left = False
                if event.key == K_LSHIFT:
                    running = False

        # Redraw everything every iteration
        screen.blit(bg, SCREEN_START)
        # Show animation
        animated_entities.update()
        # Move all monsters
        monsters.update(platforms)
        # Center the camera relative to the character
        camera.update(hero)
        # Movement
        hero.update(left, right, up, running, platforms)

        for entity in entities:
            screen.blit(entity.image, camera.apply(entity))

        timer.tick(FPS)
        # Update and display all changes on the screen
        pygame.display.update()


level = []
# What we will collide with or stand on
platforms = []
# All objects
entities = pygame.sprite.Group()
# All animated objects except the hero
animated_entities = pygame.sprite.Group()
# All moving objects
monsters = pygame.sprite.Group()


if __name__ == "__main__":
    main()
