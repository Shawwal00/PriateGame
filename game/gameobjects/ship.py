import math
import pyasge
from abc import ABC, abstractmethod

from game.fsm import FSM
from game.shipcondition import ShipCondition
from tasks.task1_shipstates import update_healthy, update_damaged, update_very_damaged, deaded


class Ship(ABC):
    """
    A ship is the base class for all other ships in the game.

    This includes both the enemy and the player. Ideally any
    code that is required for both derived classes should be
    stored here instead.
    """

    def __init__(self):
        # used for drawing the frames
        self.frames = []
        self.active_frame = None

        # current and destination
        self.position = pyasge.Point2D(0, 0)
        self.destination = [pyasge.Point2D(0, 0)]
        self.direction = pyasge.Point2D(0, 0)

        # set the initial state
        self.prev_ship_condition = ShipCondition.HEALTHY
        self.ship_condition = ShipCondition.HEALTHY

        # each ship has an FSM for its condition
        self.hp = 10
        self.fsm = FSM()
        self.fsm.setstate(self.update_healthy)

    @abstractmethod
    def update(self, game_time: pyasge.GameTime):
        pass

    @abstractmethod
    def render(self, renderer: pyasge.Renderer, game_time: pyasge.GameTime):
        pass

    def redraw(self) -> None:
        """Redraws the ship based on its current condition"""
        if self.ship_condition != self.prev_ship_condition:
            if self.ship_condition <= ShipCondition.SUNK:
                self.active_frame = self.frames[self.ship_condition]
            self.prev_ship_condition = self.ship_condition

    def set_sail(self, path: list[pyasge.Point2D]) -> None:
        """Updates the ship's destination route"""
        self.destination = path

        for path in self.destination:
            path.x -= self.width * 0.5
            path.y -= self.height * 0.5

        self.rotate()

    def rotate(self) -> None:
        """Orientate the ship depending on its direction"""
        if len(self.destination):
            if self.destination[0] == self.position:
                return

            # direction becomes target - current position normalised
            self.direction.x = self.destination[0].x - self.x
            self.direction.y = self.destination[0].y - self.y
            normalise = math.sqrt(self.direction.x * self.direction.x + self.direction.y * self.direction.y)
            self.direction.x /= normalise
            self.direction.y /= normalise

    # These functions will call your brain FSM implementations from task 1
    def update_healthy(self, game_time: pyasge.GameTime):
        update_healthy(self, game_time)

    def update_damaged(self, game_time: pyasge.GameTime):
        update_damaged(self, game_time)

    def update_very_damaged(self, game_time: pyasge.GameTime):
        update_very_damaged(self, game_time)

    def deaded(self, game_time: pyasge.GameTime):
        deaded(self, game_time)

    @property
    def height(self) -> float:
        return self.active_frame.height

    @height.setter
    def height(self, value: float) -> None:
        for frame in self.frames:
            frame.height = value

    @property
    def midpoint(self) -> pyasge.Point2D:
        return self.active_frame.midpoint

    @property
    def position(self) -> pyasge.Point2D:
        return pyasge.Point2D(self.active_frame.x, self.active_frame.y)

    @position.setter
    def position(self, value: pyasge.Point2D) -> None:
        for frame in self.frames:
            frame.x = value.x
            frame.y = value.y

    @property
    def rotation(self) -> float:
        return self.active_frame.rotation

    @rotation.setter
    def rotation(self, value: float) -> None:
        for frame in self.frames:
            frame.rotation = value

    @property
    def width(self) -> float:
        return self.active_frame.width

    @width.setter
    def width(self, value: float) -> None:
        for frame in self.frames:
            frame.width = value

    @property
    def world_bounds(self):
        return self.active_frame.getWorldBounds()

    @property
    def x(self):
        return self.active_frame.x

    @x.setter
    def x(self, value):
        for frame in self.frames:
            frame.x = value

    @property
    def y(self):
        return self.active_frame.y

    @y.setter
    def y(self, value):
        for frame in self.frames:
            frame.y = value
