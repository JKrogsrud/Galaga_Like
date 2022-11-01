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
from enemy import Enemy, create_level_one_bug, create_level_two_bug, create_level_three_bug
from battle_line import Horizontal_Battle_Line, parabolic_destination
import random
import math
from arcade.experimental import Shadertoy
import arcade.gui

FULL_SCREEN_HEIGHT = 700
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 680
HUD_WIDTH = 500
HUD_HEIGHT = 30
HUD_X_CENTER = 250
HUD_Y_CENTER = 685
HUD_LIVES_START = 350
ENEMY_SPRITE_SCALING = .0375
PLAYER_SPRITE_SCALING = .5
SCREEN_TITLE = "Galaga"


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


class EndButton(arcade.gui.UIFlatButton):

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        game_view = EndScreen()
        game_view.setup()
        game_view.window.show_view(game_view)

class StartScreen(arcade.View):

    def setup(self):
        self.logo = arcade.Sprite("Galaga.png", .15)
        self.logo.center_x = SCREEN_WIDTH/2
        self.logo.center_y = SCREEN_HEIGHT - 200

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
        #start_button_2 = StartButton(text="Two Players", width=150, style=default_style)
        #self.start_screen_alignment.add(start_button_2)
        end_button = EndButton(text="end screen", width=150, style=default_style)
        self.start_screen_alignment.add(end_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.start_screen_alignment)
        )


    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.logo.draw()

class MyGame(arcade.View):

    def __init__(self, width, height, title):
        super().__init__()

        # If you have sprite lists, you should create them here,
        # and set them to None

        self.enemy_list = None
        self.enemy_bullet_list = None
        self.player_list = None
        self.player_bullet_list = None
        self.background_list = None

        self.life_1 = None
        self.life_2 = None
        self.life_3 = None
        self.life_4 = None

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

        self.enemy_list = Horizontal_Battle_Line(speed=1, num_ships=10, left_pos=120, right_pos=480, depth=600)
        self.enemy_bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()

        # Create a trajectory
        curve_1 = parabolic_destination((-100, 750), (SCREEN_WIDTH/2, 400), 30, SCREEN_WIDTH+100)


        for i in range(10):
            enemy = create_level_one_bug(destination_list=curve_1)
            enemy.center_x = -100 - (i * 40)
            enemy.center_y = 750
            enemy.angle = 180
            self.enemy_list.add_enemy(i, enemy)


        # set up spacing for lives
        self.life_1 = arcade.Sprite("heart.png", scale=.07)
        self.life_1.center_y = HUD_Y_CENTER
        self.life_1.center_x = HUD_LIVES_START
        self.life_2 = arcade.Sprite("heart.png", scale=.07)
        self.life_2.center_y = HUD_Y_CENTER
        self.life_2.center_x = HUD_LIVES_START + 25
        self.life_3 = arcade.Sprite("heart.png", scale=.07)
        self.life_3.center_y = HUD_Y_CENTER
        self.life_3.center_x = HUD_LIVES_START + 50
        self.life_4 = arcade.Sprite("heart.png", scale=.07)
        self.life_4.center_y = HUD_Y_CENTER
        self.life_4.center_x = HUD_LIVES_START + 75

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

        level = 1

        # draw the HUD: level, points, lives
        # arcade.draw_rectangle_filled(HUD_X_CENTER, HUD_Y_CENTER, HUD_WIDTH, HUD_HEIGHT, arcade.color.GREEN)
        arcade.draw_text(f'LEVEL: {level}\t  SCORE: 0\t  LIVES:', 10, SCREEN_HEIGHT, arcade.color.GREEN, 12,
                         width=(SCREEN_WIDTH-20), align="left", font_name="Kenney Rocket Square")
        lives = 4
        if lives > 0:
            self.life_1.draw()
            if lives > 1:
                self.life_2.draw()
                if lives > 2:
                    self.life_3.draw()
                    if lives > 3:
                        self.life_4.draw()


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
            hits = arcade.check_for_collision_with_list(bullet, self.player_list)

            if len(hits) > 0:
                bullet.remove_from_sprite_lists()

                # Player hurt and loses a life



            # Bullet is off the below screen
            if bullet.bottom < 0:
                bullet.remove_from_sprite_lists()


        for bullet in self.player_bullet_list:
            # Bullet contact with enemy sprite
            hits = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            if len(hits) > 0:
                bullet.remove_from_sprite_lists()
                for enemy_hit in hits:
                    enemy_hit.hp -= bullet.damage
                    if enemy_hit.hp <= 0:
                        enemy_hit.remove_from_sprite_lists()
                        # Explosion here

            # Bullet is above the screen
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

        # Move Enemy Ships
        self.enemy_list.update()

        # Check if any enemies are ready to fire
        for enemy in self.enemy_list:
            if enemy.to_fire:
                bullet = enemy.fire()
                self.enemy_bullet_list.append(bullet)
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

class ReturnStartButton(arcade.gui.UIFlatButton):
    """ Return to start screen"""

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        start_view = StartScreen()
        start_view.setup()
        start_view.window.show_view(start_view)

class EndScreen(arcade.View):

    def setup(self):
        self.logo = arcade.Sprite("Galaga.png", .15)
        self.logo.center_x = SCREEN_WIDTH/2
        self.logo.center_y = SCREEN_HEIGHT - 200

    def on_show_view(self):
        # sets up the end screen

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.end_screen_alignment = arcade.gui.UIBoxLayout(space_between=20)

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

        return_button = ReturnStartButton(text="Return to Start", width=150, style=default_style)
        self.end_screen_alignment.add(return_button)
        replay_button = StartButton(text="Play Again", width=150, style=default_style)
        self.end_screen_alignment.add(replay_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.end_screen_alignment)
        )

    def on_draw(self):
        self.clear()
        self.manager.draw()

        # draws GAME OVER text
        start_x = 0
        start_y = (SCREEN_HEIGHT / 2) + 50
        arcade.draw_text("GAME OVER", start_x, start_y, arcade.color.LIGHT_BLUE, 20, width=SCREEN_WIDTH, align="center")

        start_x -= 50
        start_y = (SCREEN_HEIGHT / 2) + 30
        arcade.draw_text("SCORE:", start_x, start_y, arcade.color.WHITE, 10, width=SCREEN_WIDTH, align="center")
        self.logo.draw()

def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, FULL_SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartScreen()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()