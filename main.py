import pygame
from os import listdir
from os.path import isfile, join

# Initialize Pygame
pygame.init()

# Set the title of the game window
pygame.display.set_caption("Platformer Game")

# Define game constants
WIDTH, HEIGHT = 1000, 800  # Window dimensions
FPS = 60  # Frames per second
PLAYER_VEL = 5  # Player movement speed

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Function to flip sprite images horizontally
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

# Function to load sprite sheets and split them into individual sprites
def load_sprite_sheets(directory1, directory2, width, height, direction=False):
    path = join('assets', directory1, directory2)  # Construct path to sprite sheets
    images = [f for f in listdir(path) if isfile(join(path, f))]  # Get all files in the directory

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()  # Load sprite sheet

        sprites = []
        for i in range(sprite_sheet.get_width() // width):  # Extract individual sprites from the sheet
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)  # Define the area to extract
            surface.blit(sprite_sheet, (0, 0), rect)  # Copy the sprite onto a new surface
            sprites.append(pygame.transform.scale2x(surface))  # Scale up the sprite

        if direction:  # If the sprite has left and right versions
            all_sprites[image.replace('.png', '') + '_right'] = sprites
            all_sprites[image.replace('.png', '') + '_left'] = flip(sprites)
        else:
            all_sprites[image.replace('.png', '')] = sprites

    return all_sprites

# Function to load a single block texture
def load_block(size):
    path = join('assets', 'Terrain', 'Terrain.png')  # Path to the terrain texture
    image = pygame.image.load(path).convert_alpha()  # Load the image
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)  # Create a new surface
    rect = pygame.Rect(96, 0, size, size)  # Define the area of the texture to extract
    surface.blit(image, (0, 0), rect)  # Copy the block onto the surface
    return pygame.transform.scale2x(surface)  # Scale the block up

# Player class representing the character controlled by the player
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)  # Default color (not used in rendering)
    GRAVITY = 1  # Gravity constant
    SPRITES = load_sprite_sheets('MainCharacters', 'MaskDude', 32, 32, True)  # Load character sprites
    ANIMATION_DELAY = 3  # Frames per animation update

    def __init__(self, x , y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)  # Player's position and size
        self.x_vel = 0  # Horizontal velocity
        self.y_vel = 0  # Vertical velocity
        self.mask = None  # Collision mask
        self.direction = 'left'  # Default direction
        self.animation_count = 0  # Animation frame counter
        self.fall_count = 0  # Falling frame counter
        self.jump_count = 0  # Jump counter
        self.hit = False  # Hit state
        self.hit_count = 0  # Frames since being hit

    # Function to make the player jump
    def jump(self):
        self.y_vel = -self.GRAVITY * 8  # Apply an upward velocity
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:  # Reset fall count on first jump
            self.fall_count = 0

    # Function to move the player by a given amount
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    # Function to indicate the player was hit
    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    # Move player left
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != 'left':  # Change direction if necessary
            self.direction = 'left'
            self.animation_count = 0

    # Move player right
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != 'right':  # Change direction if necessary
            self.direction = 'right'
            self.animation_count = 0

    # Main update loop for the player
    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)  # Apply gravity
        self.move(self.x_vel, self.y_vel)  # Move player

        if self.hit:  # If hit, increase hit counter
            self.hit_count += 1
        if self.hit_count > fps * 2:  # Reset hit state after 2 seconds
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1  # Increase fall counter
        self.update_sprite()  # Update animation

    # Function to handle landing
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    # Function to handle hitting the head on an object
    def hit_head(self):
        self.fall_count = 0
        self.y_vel *= -1  # Reverse velocity

    # Update the player's sprite based on movement state
    def update_sprite(self):
        sprite_sheet = 'idle'  # Default to idle animation
        if self.hit:
            sprite_sheet = 'hit'
        if self.y_vel < 0:  # Jumping animations
            if self.jump_count == 1:
                sprite_sheet = 'jump'
            elif self.jump_count == 2:
                sprite_sheet = 'double_jump'
        elif self.y_vel > self.GRAVITY * 2:  # Falling animation
            sprite_sheet = 'fall'
        elif self.x_vel != 0:  # Running animation
            sprite_sheet = 'run'

        sprite_sheet_name = sprite_sheet + '_' + self.direction  # Get appropriate sprite list
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)  # Cycle through animation frames
        self.sprite = sprites[sprite_index]
        self.animation_count += 1  # Increment animation frame counter
        self.update()  # Update position

    # Update the player's position and collision mask
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))  # Update rect position
        self.mask = pygame.mask.from_surface(self.sprite)  # Update collision mask

    # Draw the player on the screen
    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

# Base class for objects in the game world
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)  # Object's position and size
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a transparent surface
        self.width = width
        self.height = height
        self.name = name  # Optional name for the object

    # Draw the object on the screen
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    # Represents a solid block in the game world
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = load_block(size)  # Load the block texture
        self.image.blit(block, (0, 0))  # Draw block image onto the object's surface
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for collision detection


def set_background(name):
    # Loads and tiles a background image across the game window
    image = pygame.image.load(join('assets', 'Background', name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):  # Repeat background horizontally
        for j in range(HEIGHT // height + 1):  # Repeat background vertically
            tile_position = (i * width, j * height)
            tiles.append(tile_position)  # Store tile positions

    return tiles, image  # Return list of tile positions and the image itself


class Fire(Object):
    ANIMATION_DELAY = 3  # Delay between animation frames

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, 'fire')
        self.fire = load_sprite_sheets('Traps', 'Fire', width, height)  # Load fire animations
        self.image = self.fire['off'][0]  # Start with fire turned off
        self.mask = pygame.mask.from_surface(self.image)  # Mask for collision detection
        self.animation_count = 0
        self.animation_name = 'off'  # Initial animation state

    def set_on(self):
        self.animation_name = 'on'  # Activate fire animation

    def set_off(self):
        self.animation_name = 'off'  # Deactivate fire animation

    def loop(self):
        # Handle fire animation updates
        sprites = self.fire[self.animation_name]  # Get current animation sprites
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]  # Set the current sprite image
        self.animation_count += 1

        # Update object's rect and mask for collisions
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        # Reset animation count if it exceeds sprite length
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


def draw(window, background, bg_image, player, objects, offset_x):
    # Draw background tiles
    for tile in background:
        window.blit(bg_image, tile)

    # Draw all game objects
    for obj in objects:
        obj.draw(window, offset_x)

    # Draw the player
    player.draw(window, offset_x)

    pygame.display.update()  # Update display


def handle_vertical_collision(player, objects, dy):
    # Check for vertical collisions between player and objects
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):  # Detect pixel-perfect collision
            if dy > 0:  # Falling down
                player.rect.bottom = obj.rect.top  # Stop at object's top
                player.landed()
            elif dy < 0:  # Jumping up
                player.rect.top = obj.rect.bottom  # Stop at object's bottom
                player.hit_head()

            collided_objects.append(obj)  # Store collided object

    return collided_objects


def collide(player, objects, dx):
    # Check for horizontal collision and return first collided object
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)  # Move player back to original position
    player.update()
    return collided_object


def handle_move(player, objects):
    # Handle player movement and collisions
    keys = pygame.key.get_pressed()
    player.x_vel = 0  # Reset horizontal velocity

    # Check for obstacles on the left and right
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    # Move player based on input and collision checks
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    # Handle vertical collisions
    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == 'fire':  # Check if player touches fire
            player.make_hit()  # Apply damage effect


def main(window):
    clock = pygame.time.Clock()  # Create clock for frame rate control
    background, bg_image = set_background("Blue.png")  # Load background
    block_size = 96  # Define block size

    # Create player and fire object
    player = Player(100, 100, 50, 50)
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.set_on()

    # Create ground and platform blocks
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)]
    objects = [*floor,
               Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size),
               Block(block_size * 6, HEIGHT - block_size * 3, block_size),
               Block(block_size * 9, HEIGHT - block_size * 5, block_size),
               Block(block_size * 12, HEIGHT - block_size * 6, block_size),
               fire]

    offset_x = 0  # Initial camera offset
    scroll_area_width = 200  # Define scrolling area

    run = True
    while run:
        clock.tick(FPS)  # Maintain constant frame rate

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Handle window close event
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:  # Double jump
                    player.jump()

        player.loop(FPS)  # Update player state
        fire.loop()  # Update fire animation
        handle_move(player, objects)  # Handle movement and collisions
        draw(window, background, bg_image, player, objects, offset_x)  # Render frame

        # Handle camera scrolling
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel  # Adjust camera offset

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)  # Start the game
