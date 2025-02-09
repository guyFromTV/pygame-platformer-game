# Platformer Game

![Game Screenshot](https://drive.google.com/uc?export=view&id=1P_xb1AYOBSFFAiMm1crPJCKt8n51JjOu)

This is a platformer game built using Pygame. The game features a player character that can move left, right, and jump, as well as interact with various objects and obstacles in the game world.

## Features

- **Player Movement**: The player can move left, right, and jump. The player can also perform a double jump.
- **Collision Detection**: The game includes collision detection for the player with the ground, blocks, and fire traps.
- **Animated Sprites**: The player and fire traps have animated sprites to enhance the visual experience.
- **Scrolling Background**: The game features a scrolling background to give the illusion of a larger game world.

## Getting Started

### Prerequisites

- Python 3.x
- Pygame library

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/guyFromTV/pygame-platformer-game.git
    ```
2. Navigate to the project directory:
    ```sh
    cd pygame-platformer-game
    ```
3. Install the required dependencies:
    ```sh
    pip install pygame
    ```

### Running the Game

To run the game, execute the following command:
```sh
python main.py
```

## Game Controls

- **Left Arrow**: Move left
- **Right Arrow**: Move right
- **Spacebar**: Jump (double jump is also supported)

## Code Overview

### `main.py`

This is the main file that initializes the game, sets up the game window, and contains the game loop.

### `Player` Class

- Handles player movement, jumping, and collision detection.
- Manages player animations based on their state (idle, running, jumping, etc.).

### `Object` Class

- Base class for all objects in the game.
- Includes methods for drawing objects on the screen.

### `Block` Class

- Inherits from `Object`.
- Represents a block in the game world.

### `Fire` Class

- Inherits from `Object`.
- Represents a fire trap with animated sprites.

### `load_sprite_sheets` Function

- Loads and splits sprite sheets into individual sprites.

### `set_background` Function

- Sets up the background image and tiles.

### `draw` Function

- Draws all game elements on the screen.

### `handle_vertical_collision` Function

- Handles vertical collisions between the player and objects.

## Acknowledgements

The assets pack used in this project was taken from https://pixelfrog-assets.itch.io/pixel-adventure-1

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.