import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Galaga"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

    """def draw_square(self):
        arcade.draw_text("draw_polygon_filled", 123, 207, arcade.color.BLUEBERRY, 9)
        point_list = ((150, 240),
                      (165, 240),
                      (180, 255),
                      (180, 285),
                      (165, 300),
                      (150, 300))
        arcade.draw_polygon_filled(point_list, arcade.color.SPANISH_VIOLET)"""

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        #draw_square()
        pass

    def on_key_press(selfself, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        pass

    def on_mouse_release(self, x, y, delta_x, delta_y):
        pass

    def on_mouse_press(self, x, y, delta_x, delta_y):
        pass



def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()