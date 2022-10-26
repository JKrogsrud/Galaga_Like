"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
from bullet import Bullet
from player import Player
from enemy import Enemy
import random
import math
import arcade.gui
from arcade.experimental import Shadertoy

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
ENEMY_SPRITE_SCALING = .0375
PLAYER_SPRITE_SCALING = .5
SCREEN_TITLE = "Galaga"


"""
Shows the enemy tiles for sprint 1, will have enemies arrive based on time in final product
"""


class Star:
    def __init__(self):
        self.x = 0
        self.y = 0

    def reset_pos(self):
        # Reset flake to random position above screen
        self.y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT + 100)
        self.x = random.randrange(SCREEN_WIDTH)

class StartButton(arcade.gui.UIFlatButton):
    """
    StartButton class for start screen
    """
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        game_view = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "Galaga")
        game_view.setup()
        game_view.window.show_view(game_view)

class StartScreen(arcade.View):

    def on_show_view(self):
        # SET UP START SCREEN

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.start_screen_alignment = arcade.gui.UIBoxLayout(space_between=20)

        default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "font_color_pressed": arcade.color.WHITE,
            "border_width": 5,
            "border_color": None,
            "bg_color": (43, 80, 227),
            "bg_color_pressed": (173, 27, 10),
            "bg_color_hover": (43, 80, 227),
            "border_color_hover": (173, 27, 10),
            "border_color_pressed": (173, 27, 10)
        }

        start_button_1 = StartButton(text="One Player", width=150, style=default_style)
        self.start_screen_alignment.add(start_button_1)
        start_button_2 = StartButton(text="Two Players", width=150, style=default_style)
        self.start_screen_alignment.add(start_button_2)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.start_screen_alignment)
        )


    def on_draw(self):
        self.clear()
        self.manager.draw()


class MyGame(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """
    def __init__(self, width, height, title):
        super().__init__()

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.enemy_list = None
        self.enemy_bullet_list = None
        self.player_list = None
        self.player_bullet_list = None
        self.background_list = None

        self.level= 1

        # Loads a file and creates a shader from it
        #window_size = self.get_size()
        #self.shadertoy = Shadertoy.create_from_file(window_size, "Purple.glsl")



    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Setup Background
        self.background_list = []

        for i in range(50):
            star = Star()

            # Randomly position it
            star.x = random.randrange(SCREEN_WIDTH)
            star.y = random.randrange(SCREEN_HEIGHT)

            # Setup other variables
            star.size = random.randrange(4)
            star.speed = random.randrange(20, 40)
            star.angle = random.uniform(math.pi, math.pi * 2)

            self.background_list.append(star)

        arcade.set_background_color(arcade.color.BLACK)

        # Create your sprites and sprite lists here
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()

        #ENEMY SETUP
        # **** the amount of each enemy type per level can be changed here
        # **** don't let number of enemy 2 or number of enemy 3 be greater than 7
        if self.level == 1:
            num_of_enemy_1 = 5
            num_of_enemy_2 = 3
            num_of_enemy_3 = 0
        elif self.level == 2:
            num_of_enemy_1 = 7
            num_of_enemy_2 = 5
            num_of_enemy_3 = 0
        elif self.level == 3:
            num_of_enemy_1 = 10
            num_of_enemy_2= 5
            num_of_enemy_3 = 1
        elif self.level == 4:
            num_of_enemy_1 = 12
            num_of_enemy_2 = 6
            num_of_enemy_3 = 3
        else:
            num_of_enemy_1 = 14
            num_of_enemy_2 = 9
            num_of_enemy_3 = 5

        #SET UP ENEMIES
        #Set up list 1 enemies
        for i in range(num_of_enemy_1):
            self.enemy_sprite = Enemy("Enemy_1.png", scale=ENEMY_SPRITE_SCALING)
            if num_of_enemy_1 <= 6:

                self.enemy_sprite.center_x = 75 + (SCREEN_WIDTH-150)/7/2 + ((SCREEN_WIDTH-150)/num_of_enemy_1)*i
                self.enemy_sprite.center_y = SCREEN_HEIGHT - 200
            else:
                if i <= 6:
                    spacing = (SCREEN_WIDTH-150)
                    self.enemy_sprite.center_x = 75 + (SCREEN_WIDTH-150)/7/2 + ((SCREEN_WIDTH - 150)/7)*(i)
                    self.enemy_sprite.center_y = SCREEN_HEIGHT - 200
                else:
                    self.enemy_sprite.center_x = 75+ (SCREEN_WIDTH-150)/(num_of_enemy_1- 7)/2 + ((SCREEN_WIDTH - 150)/(num_of_enemy_1- 7))*(i - 7)
                    self.enemy_sprite.center_y = SCREEN_HEIGHT - 150

            self.enemy_list.append(self.enemy_sprite)

        # Set up the enemies for list 2
        for i in range(num_of_enemy_2):
            self.enemy_sprite = Enemy("Enemy_2.png", ENEMY_SPRITE_SCALING)
            self.enemy_sprite.center_x = 75 + (SCREEN_WIDTH - 150) / num_of_enemy_2 / 2 + (
                        (SCREEN_WIDTH - 150) / num_of_enemy_2) * i
            self.enemy_sprite.center_y = SCREEN_HEIGHT - 100
            self.enemy_list.append(self.enemy_sprite)

        # Set up the enemies for list 3
        for i in range(num_of_enemy_3):
            self.enemy_sprite = Enemy("Enemy_3.png", ENEMY_SPRITE_SCALING)
            self.enemy_sprite.center_x = 75 + (SCREEN_WIDTH-150)/num_of_enemy_3/2 + ((SCREEN_WIDTH-150)/num_of_enemy_3)*i
            self.enemy_sprite.center_y = SCREEN_HEIGHT - 50
            self.enemy_list.append(self.enemy_sprite)

        # Set up the player
        self.player_sprite = Player()
        self.player_sprite.center_x = int(SCREEN_WIDTH / 2)
        self.player_sprite.center_y = 40
        self.player_list.append(self.player_sprite)

        # Setup Background
        self.background_list = []

        for i in range(50):
            star = Star()

            # Randomly position it
            star.x = random.randrange(SCREEN_WIDTH)
            star.y = random.randrange(SCREEN_HEIGHT)

            # Setup other variables
            star.size = random.randrange(4)
            star.speed = random.randrange(20, 40)
            star.angle = random.uniform(math.pi, math.pi * 2)

            self.background_list.append(star)

        arcade.set_background_color(arcade.color.BLACK)

        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        #GAME PLAY DISPLAY

        for star in self.background_list:
            arcade.draw_circle_filled(star.x, star.y, star.size, arcade.color.YELLOW_ORANGE)

        # Call draw() on all your sprite lists below
        self.enemy_list.draw()
        self.enemy_bullet_list.draw()
        self.player_list.draw()
        self.player_bullet_list.draw()

        # Run the GLSL code
        #self.shadertoy.render()
        #self.shadertoy.render()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # Animate all the stars falling
        for star in self.background_list:
            star.y -= star.speed * delta_time

            # Check if star has fallen below screen
            if star.y < 0:
                star.reset_pos()


        # Call update on bullet sprites
        self.enemy_bullet_list.update()
        self.player_bullet_list.update()
        self.player_list.update()

        # Check stuff
        for bullet in self.enemy_bullet_list:
            # Bullet contact with player sprite

            # Bullet is off the below screen
            if bullet.bottom < 0:
                bullet.remove_from_sprite_lists()

        for bullet in self.player_bullet_list:
            # Bullet contact with enemy sprite
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

        # Move Enemy Ships
        self.enemy_list.update()
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == 32:
            # Fire a weapon from current weapon of player at their location
            bullet = self.player_sprite.fire()
            self.player_bullet_list.append(bullet)
        elif key == arcade.key.LEFT:
            self.player_sprite.left_pressed = True
            self.player_sprite.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.player_sprite.right_pressed = True
            self.player_sprite.update_player_speed()

        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.LEFT:
            self.player_sprite.left_pressed = False
            self.player_sprite.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.player_sprite.right_pressed = False
            self.player_sprite.update_player_speed()
        pass

def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Galaga")
    start_view = StartScreen()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()

