"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
from bullet import Bullet
from weapon import Weapon
from player import Player
from enemy import Enemy, create_random_level_one_bug, create_random_level_two_bug, create_random_level_three_bug, create_L4_bug
from enemy import FiringPattern, create_swarmer, create_singleton
from battle_line import Horizontal_Battle_Line, parabolic_destination, circle_trajectory
import random
import math
import copy
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
PLAYER_SPRITE_SCALING = .02
SCREEN_TITLE = "Galaga"

INDICATOR_BAR_OFFSET = 32

DEBUG = True

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

        self.enemy_list = []
        self.enemy_bullet_list = None
        self.player_list = None
        self.player_bullet_list = None
        self.background_list = None

        # For Level 2
        self.enemy_list_2 = None

        # sprites for player health
        self.bar_list = None
        self.player_sprite = None
        self.top_label = None

        self.level = 2

        self.wave = 0

        self.time = 0

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

        self.enemy_bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()

        # set up player health
        self.bar_list = arcade.SpriteList()
        self.top_label: arcade.Text = arcade.Text(
            f'LEVEL: {self.level}\t  HEALTH: \t                   SCORE: 0', 10, SCREEN_HEIGHT-20, arcade.color.GREEN, 11,
            width=(SCREEN_WIDTH - 20), align="left", font_name="Kenney Rocket Square"
        )

        # Set up the player
        self.player_sprite = Player(self.bar_list)
        self.player_sprite.scale = PLAYER_SPRITE_SCALING
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

        # GAME PLAY DISPLAY

        for star in self.background_list:
            arcade.draw_circle_filled(star.x, star.y, star.size, arcade.color.YELLOW_ORANGE)

        # Call draw() on all your sprite lists below
        for enemy_row in self.enemy_list:
            enemy_row.draw()
        self.enemy_bullet_list.draw()
        self.player_list.draw()
        self.player_bullet_list.draw()

        # draw the player health bar and top label text
        self.bar_list.draw()
        self.top_label.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # check to see if the sprite is dead -> then exit the game
        #TODO: Change this to go to GAME OVER
        if self.player_sprite.health <= 0:
            arcade.exit()

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

        # Check Collisions
        for bullet in self.enemy_bullet_list:
            # Bullet contact with player sprite
            hits = arcade.check_for_collision_with_list(bullet, self.player_list)

            if len(hits) > 0:
                bullet.remove_from_sprite_lists()

                # Player hurt and has damage done
                # TODO: Remove Debug mode
                if not DEBUG:
                    self.player_sprite.health -= bullet.damage
                # reset indicator bar fullness
                # TODO: Some jankiness causing crashes here
                self.player_sprite.indicator_bar.fullness = (
                    self.player_sprite.health / 5
                )

            # Bullet is off the below screen
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()


        for bullet in self.player_bullet_list:
            # Bullet contact with enemy sprite
            for enemy_row in self.enemy_list:
                hits = arcade.check_for_collision_with_list(bullet, enemy_row)

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

        # Check if any enemies are in contact with the player
        for enemy_row in self.enemy_list:
            for enemy in enemy_row:
                collisions = arcade.check_for_collision_with_list(enemy, self.player_list)

                if len(collisions) > 0:
                    enemy.remove_from_sprite_lists()
                    # Explosion here
                    if not DEBUG:
                        self.player_sprite.health -= 1

        # Move Enemy Ships
        for enemy_row in self.enemy_list:
            enemy_row.update()

        # Update the timer of the level so we can have new enemies spawn
        self.time += delta_time

        if self.level == 1:

            if self.time > 0 and self.wave == 0:
                self.wave += 1
                # Create a trajectory
                curve_1 = parabolic_destination((-100, 750), (SCREEN_WIDTH / 2, 250), 30, SCREEN_WIDTH + 100)

                # Starting enemies
                enemy_row = Horizontal_Battle_Line(speed=1,
                                                   num_ships=10,
                                                   left_pos=120,
                                                   right_pos=480,
                                                   depth=350)
                for i in range(10):
                    enemy = create_random_level_one_bug(destination_list=curve_1)
                    enemy.center_x = -100 - (i * 40)
                    enemy.center_y = 750
                    enemy.angle = 180
                    enemy_row.add_enemy(i, enemy)

                self.enemy_list.append(enemy_row)

            if self.time > 10 and self.wave==1:
                self.wave += 1

                # Spawn a middle row of 8 level 1 regular ships from right side
                # Trajectory:
                curve = parabolic_destination((SCREEN_WIDTH + 100, 750),
                                              (SCREEN_WIDTH/2, 390),
                                              30,
                                              -100)
                # Battle Line
                enemy_row = Horizontal_Battle_Line(speed=1,
                                                   num_ships=10,
                                                   left_pos=120,
                                                   right_pos=480,
                                                   depth=390)
                for i in range(1, 9):
                    enemy = create_random_level_one_bug(destination_list=curve)
                    enemy.center_x = 100 + SCREEN_WIDTH + i*40
                    enemy.center_y = 650
                    enemy.angle = 180
                    enemy_row.add_enemy(9-i, enemy)

                # New entry is at index 1
                self.enemy_list.append(enemy_row)

            if self.time > 14 and self.wave == 2:
                self.wave += 1
                destination_curve_1 = [(30, SCREEN_HEIGHT-30), (60, SCREEN_HEIGHT-90)]
                destination_curve_2 = [(SCREEN_WIDTH-30, SCREEN_HEIGHT-30), (SCREEN_WIDTH-60, SCREEN_HEIGHT-90)]
                enemy_1 = create_random_level_two_bug(destination_list=destination_curve_1)
                enemy_1.center_x = -40
                enemy_1.center_y = SCREEN_HEIGHT + 40
                enemy_1.angle = 180

                self.enemy_list[1].add_enemy(0, enemy_1)

                enemy_2 = create_random_level_two_bug(destination_list=destination_curve_2)
                enemy_2.center_x = SCREEN_WIDTH + 40
                enemy_2.center_y = SCREEN_HEIGHT + 40
                enemy_2.angle = 180
                self.enemy_list[1].add_enemy(9, enemy_2)

            if self.time > 18 and self.wave == 3:
                self.wave += 1
                enemy_row = Horizontal_Battle_Line(speed=1,
                                                   num_ships=8,
                                                   left_pos=120,
                                                   right_pos=480,
                                                   depth=450)
                upper_left_trajectory = parabolic_destination(entrance_loc=(-100, 430),
                                                              turn_point=(10, 480),
                                                              num_points=30,
                                                              break_point=90)
                lower_left_trajectory = parabolic_destination(entrance_loc=(-60, 500),
                                                              turn_point=(100, 420),
                                                              num_points=30,
                                                              break_point=120)
                upper_right_trajectory = parabolic_destination(entrance_loc=(SCREEN_WIDTH+100, 430),
                                                               turn_point=(SCREEN_WIDTH-10, 480),
                                                               num_points=30,
                                                               break_point=SCREEN_WIDTH-90)
                lower_right_trajectory = parabolic_destination(entrance_loc=(SCREEN_WIDTH + 60, 500),
                                                               turn_point=(SCREEN_WIDTH-100, 430),
                                                               num_points=30,
                                                               break_point=SCREEN_WIDTH-150)

                # Create Level 1 Ships and assign their place
                enemy = create_random_level_one_bug(upper_left_trajectory)
                enemy.center_x, enemy.center_y = -100, 430
                enemy.angle = 180
                enemy_row.add_enemy(0, enemy)

                enemy = create_random_level_one_bug(upper_left_trajectory)
                enemy.center_x, enemy.center_y = -140, 430
                enemy.angle = 180
                enemy_row.add_enemy(1, enemy)

                enemy = create_random_level_one_bug(upper_right_trajectory)
                enemy.center_x, enemy.center_y = SCREEN_WIDTH + 100, 430
                enemy.angle = 180
                enemy_row.add_enemy(7, enemy)

                enemy = create_random_level_one_bug(upper_right_trajectory)
                enemy.center_x, enemy.center_y = SCREEN_WIDTH + 140, 430
                enemy.angle = 180
                enemy_row.add_enemy(6, enemy)

                # Create Level 2 Ships and assign their place
                enemy = create_random_level_two_bug(lower_left_trajectory)
                enemy.center_x, enemy.center_y = -120, 460
                enemy.angle = 180
                enemy_row.add_enemy(2, enemy)

                enemy = create_random_level_two_bug(lower_left_trajectory)
                enemy.center_x, enemy.center_y = -160, 460
                enemy.angle = 180
                enemy_row.add_enemy(3, enemy)

                enemy = create_random_level_two_bug(lower_right_trajectory)
                enemy.center_x, enemy.center_y = SCREEN_WIDTH + 120, 460
                enemy.angle = 180
                enemy_row.add_enemy(5, enemy)

                enemy = create_random_level_two_bug(lower_right_trajectory)
                enemy.center_x, enemy.center_y = SCREEN_WIDTH + 120, 460
                enemy.angle = 180
                enemy_row.add_enemy(4, enemy)

                self.enemy_list.append(enemy_row)

            if self.time > 20 and self.wave == 4:
                self.wave += 1

                enemy_row = Horizontal_Battle_Line(speed=1,
                                                   num_ships=10,
                                                   left_pos=120,
                                                   right_pos=480,
                                                   depth=530)

                trajectory = parabolic_destination(entrance_loc=(SCREEN_WIDTH/4, SCREEN_HEIGHT+50),
                                                   turn_point=(SCREEN_WIDTH/2 + 20, SCREEN_HEIGHT/2 - 40),
                                                   break_point=SCREEN_WIDTH/2,
                                                   num_points=30)

                for i in range(5, 10):
                    enemy = create_random_level_one_bug(trajectory)
                    enemy.center_x, enemy.center_y = (SCREEN_WIDTH/4, SCREEN_HEIGHT+50 + 40*i)
                    enemy.angle = 180
                    enemy_row.add_enemy(14-i, enemy)

                trajectory_2 = parabolic_destination(entrance_loc=(1.25*SCREEN_WIDTH, SCREEN_HEIGHT),
                                                     turn_point=(0.75*SCREEN_WIDTH, 0.25*SCREEN_HEIGHT),
                                                     break_point=SCREEN_WIDTH/2,
                                                     num_points=30)

                for i in range(5):
                    enemy = create_random_level_one_bug(trajectory_2)
                    enemy.center_x, enemy.center_y = (1.25*SCREEN_WIDTH, SCREEN_HEIGHT + 200 + 40*i)
                    enemy.angle = 180
                    enemy_row.add_enemy(i, enemy)

                self.enemy_list.append(enemy_row)

            if self.time > 22 and self.wave == 5:
                self.wave += 1
                enemy_row = Horizontal_Battle_Line(speed=1,
                                                   num_ships=10,
                                                   left_pos=120,
                                                   right_pos=480,
                                                   depth=580)

                trajectory_1 = parabolic_destination(entrance_loc=(SCREEN_WIDTH*1.25, SCREEN_HEIGHT*0.75),
                                                     turn_point=(SCREEN_WIDTH, SCREEN_HEIGHT*1.25),
                                                     break_point=SCREEN_WIDTH*0.9,
                                                     num_points=30)

                trajectory_2 = parabolic_destination(entrance_loc=(SCREEN_WIDTH*-.25, SCREEN_HEIGHT*0.75),
                                                     turn_point=(1, SCREEN_HEIGHT*1.25),
                                                     break_point=SCREEN_WIDTH*0.1,
                                                     num_points=30)

                for i in range(5):
                    enemy = create_random_level_two_bug(trajectory_1)
                    enemy.center_x, enemy.center_y = SCREEN_WIDTH*1.25 + 40 * i, SCREEN_HEIGHT*0.75
                    enemy.angle = 180
                    enemy_row.add_enemy(5+i, enemy)

                for i in range(5, 10):
                    enemy = create_random_level_two_bug(trajectory_2)
                    enemy.center_x, enemy.center_y = SCREEN_WIDTH*-.25 - (i-5)*40, SCREEN_HEIGHT*0.75
                    enemy.angle = 180
                    enemy_row.add_enemy(9-i, enemy)

                self.enemy_list.append(enemy_row)

            if self.time > 27 and self.wave == 6:
                self.wave += 1

                # Last attack, introduce a couple level 3 bugs on top row flanked by 2 L2s
                # Two rows of L1 bugs defend from front

                # Big guy line
                enemy_row_1 = Horizontal_Battle_Line(speed=1,
                                                     num_ships=8,
                                                     left_pos=120,
                                                     right_pos=480,
                                                     depth=650)

                # Simple entrance
                destination_curve_1 = [(SCREEN_WIDTH/2-40, 680)]
                destination_curve_2 = [(SCREEN_WIDTH/2+40, 680)]

                enemy = create_random_level_one_bug(destination_curve_1)
                enemy.center_x, enemy.center_y = SCREEN_WIDTH/2-40, SCREEN_HEIGHT+40
                enemy.angle = 180
                enemy_row_1.add_enemy(0, enemy)

                enemy = create_random_level_two_bug(destination_curve_1)
                enemy.center_x, enemy.center_y = SCREEN_WIDTH / 2 - 40, SCREEN_HEIGHT + 80
                enemy.angle = 180
                enemy_row_1.add_enemy(1, enemy)

                enemy = create_random_level_two_bug(destination_curve_1)
                enemy.center_x, enemy.center_y = SCREEN_WIDTH / 2 - 40, SCREEN_HEIGHT + 120
                enemy.angle = 180
                enemy_row_1.add_enemy(2, enemy)

                enemy = create_random_level_three_bug(destination_curve_1)
                enemy.center_x, enemy.center_y = SCREEN_WIDTH / 2 - 40, SCREEN_HEIGHT + 160
                enemy.angle = 180
                enemy_row_1.add_enemy(3, enemy)

                # 2nd half

                enemy = create_random_level_one_bug(destination_curve_2)
                enemy.center_x, enemy.center_y = SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT + 40
                enemy.angle = 180
                enemy_row_1.add_enemy(7, enemy)

                enemy = create_random_level_two_bug(destination_curve_2)
                enemy.center_x, enemy.center_y = SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT + 80
                enemy.angle = 180
                enemy_row_1.add_enemy(6, enemy)

                enemy = create_random_level_two_bug(destination_curve_2)
                enemy.center_x, enemy.center_y = SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT + 120
                enemy.angle = 180
                enemy_row_1.add_enemy(5, enemy)

                enemy = create_random_level_three_bug(destination_curve_2)
                enemy.center_x, enemy.center_y = SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT + 160
                enemy.angle = 180
                enemy_row_1.add_enemy(4, enemy)

                # Battle_formation

                enemy_row_2 = Horizontal_Battle_Line(speed=1,
                                                     num_ships=10,
                                                     left_pos=120,
                                                     right_pos=480,
                                                     depth=400)

                # Add front line enemies
                trajectory_front = [(-40, 400), (-40, 450), (SCREEN_WIDTH+40, 450), (SCREEN_WIDTH+40, 400)]

                for i in range(10):
                    enemy = create_random_level_one_bug(trajectory_front)
                    enemy.center_x, enemy.center_y = SCREEN_WIDTH + 40 + 40*i, 400
                    enemy.angle = 180
                    enemy_row_2.add_enemy(i,enemy)

                # Battle_formation 3

                enemy_row_3 = Horizontal_Battle_Line(speed=1,
                                                     num_ships=10,
                                                     left_pos=120,
                                                     right_pos=480,
                                                     depth=350)

                # Add front line enemies
                trajectory_front = [(SCREEN_WIDTH+40, 350), (SCREEN_WIDTH + 40, 300), (-40, 300), (-40, 350)]

                for i in range(10):
                    enemy = create_random_level_one_bug(trajectory_front)
                    enemy.center_x, enemy.center_y = -40 - (40 * i), 350
                    enemy.angle = 180
                    enemy_row_3.add_enemy(9-i, enemy)

                self.enemy_list.append(enemy_row_1)
                self.enemy_list.append(enemy_row_2)
                self.enemy_list.append(enemy_row_3)


        if self.level == 2:
            # Bullet Hell Level
            if self.time > 0 and self.wave == 0:
                self.wave += 1

                enemy_row = Horizontal_Battle_Line(20, SCREEN_WIDTH+20, speed=0, num_ships=11, depth=SCREEN_HEIGHT/2)

                pattern_1 = FiringPattern([1, 1, 1, 4, 1, 1, 1, 1, 1])
                pattern_2 = FiringPattern([1, 1, 1, 1, 2, 1, 1, 1, 1, 1])
                pattern_3 = FiringPattern([1, 2, 1, 1, 1, 2, 1, 1, 1, 1])
                pattern_4 = FiringPattern([2, 1, 1, 2, 1, 1, 2, 1, 1, 1])
                pattern_end = FiringPattern([.1])
                pattern_mid = FiringPattern([4, 1, 1, 4, 2, 1, 1, 1, 4, 1])
                for i in range(11):
                    spacing = SCREEN_WIDTH/12
                    destination = [((i+1) * SCREEN_WIDTH/12, SCREEN_HEIGHT/2)]
                    if i == 0 or i == 10:
                        pattern = copy.deepcopy(pattern_end)
                    elif i == 1 or i == 9:
                        pattern = copy.deepcopy(pattern_1)
                    elif i == 2 or i == 8:
                        pattern = copy.deepcopy(pattern_2)
                    elif i == 3 or i == 7:
                        pattern = copy.deepcopy(pattern_3)
                    elif i == 4 or i == 6:
                        pattern = copy.deepcopy(pattern_4)
                    elif i == 5:
                        pattern = copy.deepcopy(pattern_mid)
                    bug = create_L4_bug(destination, pattern)
                    bug.center_x, bug.center_y = (i+1) * SCREEN_WIDTH/12, SCREEN_HEIGHT + 10
                    enemy_row.add_enemy(i, bug)

                self.enemy_list.append(enemy_row)

            if self.time > 15 and self.wave == 1:
                self.wave += 1
                trajectory_1 = circle_trajectory(radius=300, center=(400, 100), start_theta=math.pi/4, num_points=30, break_theta = 5*math.pi/4)
                trajectory_2 = circle_trajectory(radius=300, center=(100, 100), start_theta=7*math.pi/4, num_points=30, break_theta = 11*math.pi/4)

                trajectory_1.extend(trajectory_2)

                enemy_row = arcade.SpriteList()
                for i in range(30):
                    enemy = create_swarmer(trajectory_1)
                    enemy.center_x, enemy.center_y = (700 + i*50, 100)
                    enemy_row.append(enemy)

                self.enemy_list.append(enemy_row)

            if self.time > 20 and self.wave == 2:
                self.wave += 1
                trajectory_1 = circle_trajectory(radius=300, center=(400, 100), start_theta=math.pi / 4, num_points=30,
                                                 break_theta=5 * math.pi / 4)
                trajectory_2 = circle_trajectory(radius=300, center=(100, 100), start_theta=7 * math.pi / 4,
                                                 num_points=30, break_theta=11 * math.pi / 4)
                trajectory_1.reverse()
                trajectory_2.reverse()
                trajectory_2.extend(trajectory_1)
                enemy_row = arcade.SpriteList()

                for i in range(30):
                    enemy = create_swarmer(trajectory_1)
                    enemy.center_x, enemy.center_y = (-100 - i * 50, 100)
                    enemy_row.append(enemy)

                self.enemy_list.append(enemy_row)

            if self.time > 25 and self.wave == 3:
                self.wave += 1

                enemy_row = arcade.SpriteList()

                trajectory_left = [(150, SCREEN_HEIGHT+10),
                                   (150, 3*SCREEN_HEIGHT/4),
                                   (110, 3*SCREEN_HEIGHT/4 - 40),
                                   (150, 3*SCREEN_HEIGHT/4 - 80),
                                   (190, 3*SCREEN_HEIGHT / 4 - 120)]
                destination_left = (40, -100)
                firing_pattern_1 = FiringPattern([1.2, 0.2, 0.2, 0.2, 0.2, 0.2])

                enemy_1 = create_singleton(trajectory_left, destination_left, firing_pattern_1)
                enemy_1.center_x, enemy_1.center_y = 150, SCREEN_HEIGHT + 20
                enemy_1.angle = 180

                trajectory_right = [(SCREEN_WIDTH - 150, SCREEN_HEIGHT+10),
                                   (SCREEN_WIDTH - 150, 3*SCREEN_HEIGHT/4),
                                   (SCREEN_WIDTH - 110, 3*SCREEN_HEIGHT/4 - 40),
                                   (SCREEN_WIDTH - 150, 3*SCREEN_HEIGHT/4 - 80),
                                   (SCREEN_WIDTH - 190, 3*SCREEN_HEIGHT / 4 - 120)]

                destination_right = (SCREEN_WIDTH - 40, -100)
                firing_pattern_1 = FiringPattern([1.2, 0.2, 0.2, 0.2, 0.2, 0.2])

                enemy_2 = create_singleton(trajectory_right, destination_right, firing_pattern_1)
                enemy_2.center_x, enemy_2.center_y = SCREEN_WIDTH - 150, SCREEN_HEIGHT + 20
                enemy_2.speed_to_formation = 1
                enemy_2.angle = 180

                enemy_row.append(enemy_1)
                enemy_row.append(enemy_2)

                self.enemy_list.append(enemy_row)

            if self.time > 27 and self.wave == 4:
                self.wave += 1

                enemy_row = arcade.SpriteList()

                trajectory_left = [(160, SCREEN_HEIGHT + 10),
                                   (160, 3 * SCREEN_HEIGHT / 4),
                                   (120, 3 * SCREEN_HEIGHT / 4 - 40),
                                   (160, 3 * SCREEN_HEIGHT / 4 - 80),
                                   (200, 3 * SCREEN_HEIGHT / 4 - 120)]
                destination_left = (40, -100)
                firing_pattern_1 = FiringPattern([1.2, 0.2, 0.2, 0.2, 0.2, 0.2])

                enemy_1 = create_singleton(trajectory_left, destination_left, firing_pattern_1)
                enemy_1.center_x, enemy_1.center_y = 150, SCREEN_HEIGHT + 20
                enemy_1.angle = 180

                trajectory_right = [(SCREEN_WIDTH - 160, SCREEN_HEIGHT + 10),
                                    (SCREEN_WIDTH - 160, 3 * SCREEN_HEIGHT / 4),
                                    (SCREEN_WIDTH - 120, 3 * SCREEN_HEIGHT / 4 - 40),
                                    (SCREEN_WIDTH - 160, 3 * SCREEN_HEIGHT / 4 - 80),
                                    (SCREEN_WIDTH - 200, 3 * SCREEN_HEIGHT / 4 - 120)]

                destination_right = (SCREEN_WIDTH - 40, -100)
                firing_pattern_1 = FiringPattern([1.2, 0.2, 0.2, 0.2, 0.2, 0.2])

                enemy_2 = create_singleton(trajectory_right, destination_right, firing_pattern_1)
                enemy_2.center_x, enemy_2.center_y = SCREEN_WIDTH - 150, SCREEN_HEIGHT + 20
                enemy_2.speed_to_formation = 1
                enemy_2.angle = 180

                enemy_row.append(enemy_1)
                enemy_row.append(enemy_2)

                self.enemy_list.append(enemy_row)

            if self.time > 29 and self.wave == 5:
                self.wave += 1

                enemy_row = arcade.SpriteList()

                trajectory_left = [(170, SCREEN_HEIGHT + 10),
                                   (170, 3 * SCREEN_HEIGHT / 4),
                                   (130, 3 * SCREEN_HEIGHT / 4 - 40),
                                   (170, 3 * SCREEN_HEIGHT / 4 - 80),
                                   (210, 3 * SCREEN_HEIGHT / 4 - 120)]
                destination_left = (40, -100)
                firing_pattern_1 = FiringPattern([1.2, 0.2, 0.2, 0.2, 0.2, 0.2])

                enemy_1 = create_singleton(trajectory_left, destination_left, firing_pattern_1)
                enemy_1.center_x, enemy_1.center_y = 150, SCREEN_HEIGHT + 20
                enemy_1.angle = 180

                trajectory_right = [(SCREEN_WIDTH - 170, SCREEN_HEIGHT + 10),
                                    (SCREEN_WIDTH - 170, 3 * SCREEN_HEIGHT / 4),
                                    (SCREEN_WIDTH - 130, 3 * SCREEN_HEIGHT / 4 - 40),
                                    (SCREEN_WIDTH - 170, 3 * SCREEN_HEIGHT / 4 - 80),
                                    (SCREEN_WIDTH - 210, 3 * SCREEN_HEIGHT / 4 - 120)]

                destination_right = (SCREEN_WIDTH - 40, -100)
                firing_pattern_1 = FiringPattern([1.2, 0.2, 0.2, 0.2, 0.2, 0.2])

                enemy_2 = create_singleton(trajectory_right, destination_right, firing_pattern_1)
                enemy_2.center_x, enemy_2.center_y = SCREEN_WIDTH - 150, SCREEN_HEIGHT + 20
                enemy_2.speed_to_formation = 1
                enemy_2.angle = 180

                enemy_row.append(enemy_1)
                enemy_row.append(enemy_2)

                self.enemy_list.append(enemy_row)

            if self.time > 31 and self.wave == 6:
                self.wave += 1

                enemy_row = arcade.SpriteList()

                trajectory_left = [(180, SCREEN_HEIGHT + 10),
                                   (180, 3 * SCREEN_HEIGHT / 4),
                                   (140, 3 * SCREEN_HEIGHT / 4 - 40),
                                   (180, 3 * SCREEN_HEIGHT / 4 - 80),
                                   (220, 3 * SCREEN_HEIGHT / 4 - 120)]
                destination_left = (40, -100)
                firing_pattern_1 = FiringPattern([1.2, 0.2, 0.2, 0.2, 0.2, 0.2])

                enemy_1 = create_singleton(trajectory_left, destination_left, firing_pattern_1)
                enemy_1.center_x, enemy_1.center_y = 150, SCREEN_HEIGHT + 20
                enemy_1.angle = 180

                trajectory_right = [(SCREEN_WIDTH - 180, SCREEN_HEIGHT + 10),
                                    (SCREEN_WIDTH - 180, 3 * SCREEN_HEIGHT / 4),
                                    (SCREEN_WIDTH - 140, 3 * SCREEN_HEIGHT / 4 - 40),
                                    (SCREEN_WIDTH - 180, 3 * SCREEN_HEIGHT / 4 - 80),
                                    (SCREEN_WIDTH - 220, 3 * SCREEN_HEIGHT / 4 - 120)]

                destination_right = (SCREEN_WIDTH - 40, -100)
                firing_pattern_1 = FiringPattern([1.2, 0.2, 0.2, 0.2, 0.2, 0.2])

                enemy_2 = create_singleton(trajectory_right, destination_right, firing_pattern_1)
                enemy_2.center_x, enemy_2.center_y = SCREEN_WIDTH - 150, SCREEN_HEIGHT + 20
                enemy_2.speed_to_formation = 1
                enemy_2.angle = 180

                enemy_row.append(enemy_1)
                enemy_row.append(enemy_2)

                self.enemy_list.append(enemy_row)

            if self.time > 33 and self.wave == 7:
                self.wave += 1

                enemy_row = arcade.SpriteList()

                # Prepare the various trajectories about to be used

                trajectory_1 = circle_trajectory(75, (SCREEN_WIDTH-100, SCREEN_HEIGHT-100), math.pi/2, 50, 9*math.pi/2)
                trajectory_2 = circle_trajectory(330, (400, 325), 2*math.pi/3, 60, math.pi)
                trajectory_3 = circle_trajectory(50, (70, 275), math.pi/2, 100, 7*math.pi/2)
                trajectory_4 = circle_trajectory(70, (SCREEN_WIDTH-150, SCREEN_HEIGHT-450), 3*math.pi/2, 50, 9* math.pi/2)
                trajectory_4.reverse()

                trajectory_1.extend(trajectory_2)
                trajectory_1.extend(trajectory_3)
                trajectory_1.extend(trajectory_4)

                # All of the following will be used as 4 separate branches for the trajectory above
                trajectory_a = circle_trajectory(150, (175, 0), math.pi / 2, 60, 9 * math.pi / 2)
                trajectory_b = circle_trajectory(150, (325, 0), math.pi / 2, 60, 9 * math.pi / 2)
                trajectory_b.reverse()

                trajectory_a_1 = circle_trajectory(125, (125, 0), math.pi / 2, 60, 7 * math.pi / 2)
                trajectory_a_2 = circle_trajectory(125, (175, 0), 3 * math.pi / 2, 60, 11 * math.pi / 2)
                trajectory_a_2.reverse()

                trajectory_b_1 = circle_trajectory(125, (325, 0), math.pi / 2, 60, 7 * math.pi / 2)
                trajectory_b_2 = circle_trajectory(125, (375, 0), 3 * math.pi / 2, 60, 7 * math.pi / 2)
                trajectory_b_2.reverse()

                trajectory_alpha = trajectory_1.copy()
                trajectory_alpha.extend(trajectory_a)
                trajectory_alpha.extend(trajectory_a_1)

                trajectory_beta = trajectory_1.copy()
                trajectory_beta.extend(trajectory_a)
                trajectory_beta.extend(trajectory_a_2)

                trajectory_gamma = trajectory_1.copy()
                trajectory_gamma.extend(trajectory_b)
                trajectory_gamma.extend(trajectory_b_1)

                trajectory_omega = trajectory_1.copy()
                trajectory_omega.extend(trajectory_b)
                trajectory_omega.extend(trajectory_b_2)

                # Ok now we create a WHOLE lot of bugs to travel 4 different paths
                for i in range(200):
                    if i%4 == 0:
                        swarm = create_swarmer(trajectory_alpha)
                    elif i%4 == 1:
                        swarm = create_swarmer(trajectory_beta)
                    elif i%4 == 2:
                        swarm = create_swarmer(trajectory_gamma)
                    elif i%4 == 3:
                        swarm = create_swarmer(trajectory_omega)

                    swarm.center_x, swarm.center_y = SCREEN_WIDTH + 40 * (i + 1), SCREEN_HEIGHT
                    enemy_row.append(swarm)

                self.enemy_list.append(enemy_row)

            if self.time > 55 and self.wave == 8:
                self.wave += 1
                """
                BOSS TIME
                """
                boss_line = Horizontal_Battle_Line(200, 300, 1, num_ships=1, depth=SCREEN_HEIGHT-50)
                big_goo = Bullet(filename="blue_laser.png", speed=2, scale=2.5)
                big_weapon = Weapon(friendly=False, requires_ammo=False, bullet_type=big_goo, bullet_speed=2)
                destination = [(SCREEN_WIDTH/2, SCREEN_HEIGHT + 100), (SCREEN_WIDTH/2, SCREEN_HEIGHT - 50)]
                boss = Enemy("Player.png", destination_list=destination,
                             scale=.2,
                             hp=150,
                             weapon=big_weapon,
                             speed_to_formation=2,
                             time_between_firing=1.5,
                             speed_in_formation=1,
                             time_until_charge=300
                             )
                boss.center_x, boss.center_y = SCREEN_WIDTH/2, SCREEN_HEIGHT + 200
                boss.angle = 180
                boss_line.add_enemy(0, boss)
                self.enemy_list.append(boss_line)
                print("Boss joined the party")


        # Check if enemies are ready to fire
        for enemy_row in self.enemy_list:
            for enemy in enemy_row:
                if enemy.to_fire:
                    bullet = enemy.fire()
                    self.enemy_bullet_list.append(bullet)

        # Check if enemies are ready to despawn
        for enemy_row in self.enemy_list:
            for enemy in enemy_row:
                if enemy.despawn:
                    enemy.remove_from_sprite_lists()

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
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Galaga")
    start_view = StartScreen()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
