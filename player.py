import arcade
from typing import Tuple
from weapon import Weapon

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700


class Player(arcade.Sprite):
    def __init__(self, bar_list: arcade.SpriteList,
                 filename="Player.png",
                 health=3,
                 weapon=Weapon(),
                 movement_speed=10,
                 ):
        super().__init__(filename, scale=0.035)
        self.health = health
        self.weapon = weapon
        self.movement_speed = movement_speed
        self.left_pressed = False
        self.right_pressed = False
        # stuff to create the bar for player health
        self.indicator_bar: IndicatorBar = IndicatorBar(
            self, bar_list, (self.center_x, self.center_y)
        )

    def update(self):
        # Move player.
        self.center_x += self.change_x

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

    # Creates a bullet that the weapon should create
    def fire(self):
        bullet = self.weapon.fire(self.center_x, self.bottom + self.height)
        return bullet

    def update_player_speed(self):
        # Calculate speed based on the keys pressed
        self.change_x = 0
        if self.left_pressed and not self.right_pressed:
            self.change_x = -self.movement_speed
        elif self.right_pressed and not self.left_pressed:
            self.change_x = self.movement_speed


class IndicatorBar:
    """
       Represents a bar which can display information about a sprite.
       :param Player owner: The owner of this indicator bar.
       :param arcade.SpriteList sprite_list: The sprite list used to draw the indicator
        bar components.
       :param Tuple[float, float] position: The initial position of the bar.
       :param arcade.Color full_color: The color of the bar.
       :param arcade.Color background_color: The background color of the bar.
       :param int width: The width of the bar.
       :param int height: The height of the bar.
       :param int border_size: The size of the bar's border.
    """
    def __init__(
        self,
        owner: Player,
        sprite_list: arcade.SpriteList,
        position: Tuple[float, float] = (0, 0),
        full_color: arcade.Color = arcade.color.GREEN,
        background_color: arcade.Color = arcade.color.BARBIE_PINK,
        width: int = 100,
        height: int = 5,
        border_size: int = 4,
    ) -> None:
        # Store the reference to the owner and the sprite list
        self.owner: Player = owner
        self.sprite_list: arcade.SpriteList = sprite_list

        # Set the needed size variables
        self._box_width: int = width
        self._box_height: int = height
        self._half_box_width: int = self._box_width // 2
        self._center_x: float = 0.0
        self._center_y: float = 0.0
        self._fullness: float = 0.0

        # Create the boxes needed to represent the indicator bar
        self._background_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width + border_size,
            self._box_height + border_size,
            background_color,
        )
        self._full_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width,
            self._box_height,
            full_color,
        )
        self.sprite_list.append(self._background_box)
        self.sprite_list.append(self._full_box)

        # Set the fullness and position of the bar
        self.fullness: float = 1.0
        self._center_x, self._center_y = (275, 665)
        self.background_box.position = (275, 665)
        self.full_box.position = (275, 665)

        # Make sure full_box is to the left of the bar instead of the middle
        self.full_box.left = self._center_x - (self._box_width // 2)

    def __repr__(self) -> str:
        return f"<IndicatorBar (Owner={self.owner})>"

    @property
    def background_box(self) -> arcade.SpriteSolidColor:
        """Returns the background box of the indicator bar."""
        return self._background_box

    @property
    def full_box(self) -> arcade.SpriteSolidColor:
        """Returns the full box of the indicator bar."""
        return self._full_box

    @property
    def fullness(self) -> float:
        """Returns the fullness of the bar."""
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness: float) -> None:
        """Sets the fullness of the bar."""
        # Check if new_fullness if valid
        if not (0.0 <= new_fullness <= 1.0):
            if new_fullness < 0.0:
                new_fullness = 0
            if new_fullness > 1.0:
                new_fullness = 1.0

        # Set the size of the bar
        self._fullness = new_fullness
        if new_fullness == 0.0:
            # Set the full_box to not be visible since it is not full anymore
            self.full_box.visible = False
        else:
            # Set the full_box to be visible incase it wasn't then update the bar
            self.full_box.visible = True
            self.full_box.width = self._box_width * new_fullness
            self.full_box.left = self._center_x - (self._box_width // 2)

    @property
    def position(self) -> Tuple[float, float]:
        """Returns the current position of the bar."""
        return self._center_x, self._center_y
