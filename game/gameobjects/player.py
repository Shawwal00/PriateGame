import math
import pyasge

from game.gameobjects.ship import Ship
PLAYER_SPEED = 750


class Player(Ship):

    """A player is a type of ship and is user controlled"""
    def __init__(self):
        super().__init__()

        # player game data/state
        self.score = 0
        self.score_add = 0
        self.hp = 10

        # load the various sprites for each ship condition
        filenames = [
            "data/sprites/ships/ship (2).png",
            "data/sprites/ships/ship (8).png",
            "data/sprites/ships/ship (14).png",
            "data/sprites/ships/ship (20).png"]

        for filename in filenames:
            self.frames.append(pyasge.Sprite())
            self.frames[-1].loadTexture(filename)
            self.frames[-1].setMagFilter(pyasge.MagFilter.LINEAR)
            self.frames[-1].z_order = 10
            self.frames[-1].width = 66
            self.frames[-1].height = 113

        # set the active frame to be the first sprite loaded
        self.active_frame = self.frames[0]

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        """The fixed-update function moves the player at a constant speed"""
        if len(self.destination):
            if abs(self.position.distance(self.destination[0])) < PLAYER_SPEED * 0.02:
                self.position = self.destination.pop(0)
                self.rotate()
                return

            self.position += self.direction * PLAYER_SPEED * game_time.fixed_timestep

    def update(self, game_time: pyasge.GameTime) -> None:
        """Updates the player's rotation and score"""
        if len(self.destination):
            v1 = self.position
            v2 = self.destination[0]
            dx = v2.x - v1.x
            dy = v2.y - v1.y

            angle = math.atan2(dy, dx) - 1.5708
            self.rotation = angle

        # is there score to add?
        if self.score_add:
            self.score_add -= int(300 * game_time.frame_time)
            self.score += int(300 * game_time.frame_time)

        # update the fsm
        self.fsm.update(game_time)

        # if the ship's condition has changed we need to redraw it
        self.redraw()

    def render(self, renderer: pyasge.Renderer, game_time: pyasge.GameTime) -> None:
        renderer.render(self.active_frame)





