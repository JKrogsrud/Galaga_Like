"""
Starting Template

"""
import arcade

ENEMY_SPRITE_SCALING = .0375
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Galaga"

MOVEMENT_SPEED = 5

level = 5

# **** the amount of each enemy type per level can be changed here
# **** don't let number of enemy 2 or number of enemy 3 be greater than 7
if level == 1:
    NUM_OF_ENEMY_1 = 5
    NUM_OF_ENEMY_2 = 3
    NUM_OF_ENEMY_3 = 0
elif level == 2:
    NUM_OF_ENEMY_1 = 7
    NUM_OF_ENEMY_2 = 5
    NUM_OF_ENEMY_3 = 0
elif level == 3:
    NUM_OF_ENEMY_1 = 10
    NUM_OF_ENEMY_2 = 5
    NUM_OF_ENEMY_3 = 1
elif level == 4:
    NUM_OF_ENEMY_1 = 12
    NUM_OF_ENEMY_2 = 6
    NUM_OF_ENEMY_3 = 3
else:
    NUM_OF_ENEMY_1 = 14
    NUM_OF_ENEMY_2 = 9
    NUM_OF_ENEMY_3 = 5


class Enemy(arcade.Sprite):

    def update(self):
        # Check for out-of-bounds
        if self.left < 10:
            self.change_x = 5
        elif self.right > SCREEN_WIDTH - 10:
            self.change_x = -5

        # Move the enemies
      #  self.center_x += self.change_x


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.enemy_list_1 = None
        self.enemy_list_2 = None
        self.enemy_list_3 = None

        # Set up the enemy info
        self.enemy_sprite = None

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        #Set up the game and initialize the variables

        #set up level
        level = 7

        # Sprite lists
        self.enemy_list_1 = arcade.SpriteList()
        self.enemy_list_2 = arcade.SpriteList()
        self.enemy_list_3 = arcade.SpriteList()


        # Set up the enemies for enemey_list_1
        # ******num of enemies per level can be edited here*****

        if level == 1 or level == 2:
            num_of_enemies_1 = 6
        elif level == 3 or level == 4:
            num_of_enemies_1 = 10
        else:
            num_of_enemies_1 = 12

        for i in range(NUM_OF_ENEMY_1):
            self.enemy_sprite = Enemy("Enemy_1.png", ENEMY_SPRITE_SCALING)
            if NUM_OF_ENEMY_1 <= 6:

                self.enemy_sprite.center_x = 75 + (SCREEN_WIDTH-150)/7/2 + ((SCREEN_WIDTH-150)/NUM_OF_ENEMY_1)*i
                self.enemy_sprite.center_y = SCREEN_HEIGHT - 200
            else:
                if i <= 6:
                    spacing = (SCREEN_WIDTH-150)
                    self.enemy_sprite.center_x = 75 + (SCREEN_WIDTH-150)/7/2 + ((SCREEN_WIDTH - 150)/7)*(i)
                    self.enemy_sprite.center_y = SCREEN_HEIGHT - 200
                else:
                    self.enemy_sprite.center_x = 75+ (SCREEN_WIDTH-150)/(NUM_OF_ENEMY_1- 7)/2 + ((SCREEN_WIDTH - 150)/(NUM_OF_ENEMY_1- 7))*(i - 7)
                    self.enemy_sprite.center_y = SCREEN_HEIGHT - 150

            self.enemy_list_1.append(self.enemy_sprite)

        # Set up the enemies for list 2
        for i in range(NUM_OF_ENEMY_2):
            self.enemy_sprite = Enemy("Enemy_2.png", ENEMY_SPRITE_SCALING)
            self.enemy_sprite.center_x = 75 + + (SCREEN_WIDTH - 150) / NUM_OF_ENEMY_2 / 2 + (
                        (SCREEN_WIDTH - 150) / NUM_OF_ENEMY_2) * i
            self.enemy_sprite.center_y = SCREEN_HEIGHT - 100
            self.enemy_list_2.append(self.enemy_sprite)

        # Set up the enemies for list 3
        for i in range(NUM_OF_ENEMY_3):
            self.enemy_sprite = Enemy("Enemy_3.png", ENEMY_SPRITE_SCALING)
            self.enemy_sprite.center_x = 75 + + (SCREEN_WIDTH-150)/NUM_OF_ENEMY_3/2 + ((SCREEN_WIDTH-150)/NUM_OF_ENEMY_3)*i
            self.enemy_sprite.center_y = SCREEN_HEIGHT - 50
            self.enemy_list_3.append(self.enemy_sprite)

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.enemy_list_1.draw()
        self.enemy_list_2.draw()
        self.enemy_list_3.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the enemy
        self.enemy_list_1.update()

    def on_key_press(self, key, modifiers):
        pass

    def on_key_release(self, key, modifiers):
        pass


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

        self.enemy_list_1_draw()
        self.enemy_list_2_draw()
        self.enemy_list_3_draw()


    def on_update(self, delta_time):
        self.enemy_list_1.update()
        self.enemy_list_2.update()
        self.enemy_list_3.update()

    def on_key_press(self, key, key_modifiers):
        pass

    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":

    main()
