import math
import random

import pyasge
from pyfmodex.flags import MODE

from game.gameobjects.cannonball import Cannonball
from game.shipcondition import ShipCondition
from tasks.task4_enemy import Enemy
from game.gamedata import GameData
from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID
from tasks.task3_pathfinding import resolve


class GamePlay(GameState):
    """ The game play state is the core of the game itself.

    The role of this class is to process the game logic, update
    the players positioning and render the resultant game-world.
    The logic for deciding on victory or loss should be handled by
    this class and its update function should return GAME_OVER or
    GAME_WON when the end game state is reached.
    """

    def __init__(self, data: GameData) -> None:
        """ Creates the game world

        Use the constructor to initialise the game world in a "clean"
        state ready for the player. This includes resetting of player's
        health and the enemy positions.

        Args:
            data (GameData): The game's shared data
        """
        super().__init__(data)

        self.id = GameStateID.GAMEPLAY
        self.debug = True
        self.data.renderer.setClearColour((201 / 255, 236 / 255, 251 / 255))

        # gameplay data
        self.cannonballs = []
        self.reset_player()
        self.enemies = []
        self.spawn_enemies()

        # ui elements
        self.ui_score = None
        self.ui_enemy_icon = None
        self.init_ui()

        # debug text on screen
        self.debug_player_rotation = None
        self.debug_player_tile = None
        self.debug_player_pos = None
        self.init_debug_text()

        # sets up the camera and points it at the player
        self.camera = pyasge.Camera([0, 0], self.data.game_res[0], self.data.game_res[1])
        self.camera.zoom = 1
        self.camera.lookAt(self.data.player.midpoint)

        # loads the sounds needed
        self.sounds = {
            "fire": self.data.audio_system.create_sound("./data/audio/Weapons_CannonsShot_02.ogg", mode=MODE.LOOP_OFF),
            "sunk": self.data.audio_system.create_sound("./data/audio/Impact_Ship_01.ogg", mode=MODE.LOOP_OFF),
            "miss": self.data.audio_system.create_sound("./data/audio/Impact_Cannon_OnWater_03.ogg", mode=MODE.LOOP_OFF),
            "hit": self.data.audio_system.create_sound("./data/audio/Impact_Ship_03.ogg", mode=MODE.LOOP_OFF),
            "applause": self.data.audio_system.create_sound("./data/audio/Emotions_Group_Applause.ogg", mode=MODE.LOOP_OFF)
        }

    def init_debug_text(self):
        """Initialises the debug text on the screen"""
        self.debug_player_pos = pyasge.Text(self.data.fonts["debug"])
        self.debug_player_pos.x = 25
        self.debug_player_pos.y = 75
        self.debug_player_pos.scale = 1.0
        self.debug_player_pos.string = \
            f'(' + f'{int(self.data.player.x):04}' + f',' + f'{int(self.data.player.y):04}' + f')'

        tile_location = self.data.game_map.tile(self.data.player.position)
        self.debug_player_tile = pyasge.Text(self.data.fonts["debug"])
        self.debug_player_tile.x = 25
        self.debug_player_tile.y = self.debug_player_pos.y + 20
        self.debug_player_tile.scale = 1.0
        self.debug_player_tile.string = \
            f'(' + f'{int(tile_location[0]):04}' + f',' + f'{int(tile_location[1]):04}' + f')'

        self.debug_player_rotation = pyasge.Text(self.data.fonts["debug"])
        self.debug_player_rotation.x = 25
        self.debug_player_rotation.y = self.debug_player_tile.y + 20
        self.debug_player_rotation.scale = 1.0
        self.debug_player_rotation.string = \
            f'(' + f'{abs(float(self.data.player.rotation * 180 / math.pi)):04f}' + f')'

    def init_ui(self):
        """Initialises the UI elements"""
        self.ui_enemy_icon = self.data.renderer.loadTexture("./data/sprites/ships/ship (4).png")
        self.ui_enemy_icon.setMagFilter(pyasge.MagFilter.LINEAR)
        self.ui_score = pyasge.Text(self.data.fonts["score"], str(000000))
        self.ui_score.x = 25
        self.ui_score.y = 18 + self.ui_score.local_bounds.v3.x
        self.ui_score.colour = pyasge.COLOURS.BLACK
        self.ui_score.scale = 1

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        if event.button is pyasge.MOUSE.MOUSE_BTN2 and \
                event.action is pyasge.MOUSE.BUTTON_PRESSED:

            # launch a cannonball from the ship's origin to click position
            cannonball = Cannonball(self.data.player.midpoint, self.to_world(pyasge.Point2D(event.x, event.y)))
            self.cannonballs.append(cannonball)

            # play audio to signal a cannonball has been launched
            channel = self.data.audio_system.play_sound(self.sounds["fire"])

        if event.button is pyasge.MOUSE.MOUSE_BTN1 and \
                event.action is pyasge.MOUSE.BUTTON_PRESSED:

            # updates the player's route
            self.data.player.set_sail((resolve(self.to_world(pyasge.Point2D(event.x, event.y)), self.data)))

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        """ Listens for mouse movement events from the game engine """
        pass

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        """ Listens for key events from the game engine """
        # toggle debug mode if d key is pressed
        if event.action == pyasge.KEYS.KEY_PRESSED and event.key == pyasge.KEYS.KEY_D:
            self.debug = not self.debug
            return

    def spawn_enemies(self) -> None:
        """ Loads the map and spawns enemies"""
        rands = random.sample(self.data.game_map.spawns, 5)
        while len(self.enemies) != 5:
            self.enemies.append(Enemy())
            x, y = rands.pop()
            self.enemies[-1].x = x
            self.enemies[-1].y = y

    def reset_player(self) -> None:
        """ Loads the player and sets its initial position"""
        self.data.player.position = pyasge.Point2D(5407, 775)
        self.data.player.destination = [self.data.player.position]

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        """ Simulates deterministic time steps for the game objects"""
        for cannonball in self.cannonballs:
            cannonball.fixed_update(game_time)
        self.resolveCannonballs()
        self.data.player.fixed_update(game_time)

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        """ Updates the game world

        Processes the game world logic. You should handle collisions,
        actions and AI actions here. At present cannonballs are
        updated and so are player collisions with the islands, but
        consider how the ships will react to each other

        Args:
            game_time (pyasge.GameTime): The time between ticks.
        """

        # update the player
        self.data.player.update(game_time)

        # follow the player and clamp the camera
        self.update_camera()

        # updates the cannonballs
        for cannonball in self.cannonballs:
            cannonball.update(game_time)

        # updates the enemy ships
        for enemy in self.enemies:
            enemy.update(game_time)

        # if all the enemies are dead, we should play an audio cue and wait for it to finish
        if all([x.hp == 0 for x in self.enemies]):
            channel = self.data.audio_system.play_sound(self.sounds["applause"])
            while channel.is_playing:
                pass
            return GameStateID.WINNER_WINNER

        # if the player is dead, it's game over man!
        if self.data.player.ship_condition is ShipCondition.SUNK:
            return GameStateID.GAME_OVER

        return GameStateID.GAMEPLAY

    def update_camera(self):
        self.camera.lookAt(self.data.player.midpoint)
        # as the player can move around, we need to clamp the camera every
        # update to ensure the tile map is shown correctly.
        view = [
            self.data.game_res[0] * 0.5 / self.camera.zoom,
            self.data.game_map.width * 128 - self.data.game_res[0] * 0.5 / self.camera.zoom,
            self.data.game_res[1] * 0.5 / self.camera.zoom,
            self.data.game_map.height * 128 - self.data.game_res[1] * 0.5 / self.camera.zoom
        ]
        self.camera.clamp(view)

    def render(self, game_time: pyasge.GameTime) -> None:
        """ Renders the game world and the UI """
        self.data.renderer.setProjectionMatrix(self.camera.view)
        self.data.game_map.render(self.data.renderer, game_time)
        self.data.player.render(self.data.renderer, game_time)

        for enemy in self.enemies:
            enemy.render(self.data.renderer, game_time)

        for cannonball in self.cannonballs:
            cannonball.render(self.data.renderer, game_time)

        self.render_ui()

    def resolveCannonballs(self) -> None:
        """
        Updates the active cannonballs in the world

        Checks to see if the cannonballs have reached their target
        or collided with a ship. If they hit a ship the ship's hp
        will drop by 1. This of course can be changed or tweaked.
        At present if the ship's hp is below 0, the console will
        print the "dead" message
        """
        # check to see if canonballs are finished
        for cannonball in self.cannonballs:

            # check for collisions
            for enemy in self.enemies:
                if enemy.hp == 0:
                    continue

                b2 = cannonball.world_bounds
                b1 = enemy.world_bounds

                if (b1.v1.x < b2.v2.x and
                        b1.v2.x > b2.v1.x and
                        b1.v1.y < b2.v4.y and
                        b1.v4.y > b2.v1.y):
                    self.data.player.score_add += 100
                    self.cannonballs.remove(cannonball)
                    enemy.hp -= 1
                    channel = self.data.audio_system.play_sound(self.sounds["hit"])
                    channel.volume = 0.35

                if enemy.hp == 0:
                    self.data.audio_system.play_sound(self.sounds["sunk"])

            if cannonball.position == cannonball.destination:
                tile_xy = self.data.game_map.tile(cannonball.position)
                tile = (self.data.game_map.map[2][1])[tile_xy[1]][tile_xy[0]]
                if not tile:
                    self.data.audio_system.play_sound(self.sounds["miss"])
                self.cannonballs.remove(cannonball)

    def render_ui(self) -> None:
        """ Render the UI elements and map to the whole window """
        vp = self.data.renderer.resolution_info.viewport
        self.data.renderer.setProjectionMatrix(0, 0, vp.w, vp.h)
        self.ui_score.string = f'{self.data.player.score:06}'
        self.data.renderer.render(self.ui_score)

        count = 0
        for enemy in self.enemies:
            if enemy.ship_condition is not ShipCondition.SUNK:
                self.data.renderer.render(self.ui_enemy_icon, vp.w - (100 + (50*count)), 10, 45, 75, 20)
                count += 1

        if self.debug:
            self.render_debug()
        self.data.renderer.setProjectionMatrix(0, 0, self.data.game_res[0], self.data.game_res[1])

    def render_debug(self) -> None:
        """ Renders debug information """
        self.debug_player_pos.string = \
            f'(' + f'{int(self.data.player.x):04}' + f',' + f'{int(self.data.player.y):04}' + f')'
        self.data.renderer.render(self.debug_player_pos)

        tile_location = self.data.game_map.tile(self.data.player.position)
        self.debug_player_tile.string = \
            f'(' + f'{int(tile_location[0]):04}' + f',' + f'{int(tile_location[1]):04}' + f')'
        self.data.renderer.render(self.debug_player_tile)

        self.debug_player_rotation.string = \
            f'(' + f'{abs(float(self.data.player.rotation * 180 / math.pi)):04f}' + f')'
        self.data.renderer.render(self.debug_player_rotation)

    def to_world(self, pos: pyasge.Point2D) -> pyasge.Point2D:
        """
        Converts from screen position to world position
        :param pos: The position on the current game window camera
        :return: Its actual/absolute position in the game world
        """
        view = self.camera.view
        x = (view.max_x - view.min_x) / self.data.game_res[0] * pos.x
        y = (view.max_y - view.min_y) / self.data.game_res[1] * pos.y
        x = view.min_x + x
        y = view.min_y + y

        return pyasge.Point2D(x, y)
