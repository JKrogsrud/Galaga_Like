"Final Project - Galaga Remake"

"""
Platformer Game
"""
import random
import math
import arcade
from arcade.experimental import Shadertoy

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Galaga"


class Snowflake:
    """
    Each instance of this class represents a single snowflake.
    Based on drawing filled-circles.
    """

    def __init__(self):
        self.x = 0
        self.y = 0

    def reset_pos(self):
        # Reset flake to random position above screen
        self.y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT + 100)
        self.x = random.randrange(SCREEN_WIDTH)


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """ Initializer """
        # Calls "__init__" of parent class (arcade.Window) to setup screen
        super().__init__(width, height, title)

        "self.background = None"

        # Sprite lists
        self.snowflake_list = None

        #Loads a file and creates a shader from it
        """shader_file_path1 = "circle_1.glsl"
        shader_file_path2 = "Purple.glsl"""
        window_size = self.get_size()
        self.shadertoy = Shadertoy.create_from_file(window_size, "circle_1.glsl")
        self.shadertoy = Shadertoy.create_from_file(window_size, "Purlple.glsl")

    def start_snowfall(self):
        """ Set up snowfall and initialize variables. """
        self.snowflake_list = []

        for i in range(50):
            # Create snowflake instance
            snowflake = Snowflake()

            # Randomly position snowflake
            snowflake.x = random.randrange(SCREEN_WIDTH)
            snowflake.y = random.randrange(SCREEN_HEIGHT + 200)

            # Set other variables for the snowflake
            snowflake.size = random.randrange(4)
            snowflake.speed = random.randrange(20, 40)
            snowflake.angle = random.uniform(math.pi, math.pi * 2)

            # Add snowflake to snowflake list
            self.snowflake_list.append(snowflake)

        # Don't show the mouse pointer
        self.set_mouse_visible(False)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Render the screen. """

        # This command is necessary before drawing
        self.clear()

        # Run the GLSL code
        self.shadertoy.render()
        self.shadertoy.render()

        # Draw the current position of each snowflake
        for snowflake in self.snowflake_list:
            arcade.draw_circle_filled(snowflake.x, snowflake.y,
                                      snowflake.size, arcade.color.WHITE)

    def on_update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """

        # Animate all the snowflakes falling
        for snowflake in self.snowflake_list:
            snowflake.y -= snowflake.speed * delta_time

            # Check if snowflake has fallen below screen
            if snowflake.y < 0:
                snowflake.reset_pos()


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.start_snowfall()
    arcade.run()


if __name__ == "__main__":
    main()