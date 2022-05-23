import random
import pyasge
from pyfmodex.flags import MODE

from game.gamedata import GameData
from game.gameobjects.player import Player
from game.gameobjects.gamemap import GameMap
from game.gamestates.gameplay import GamePlay
from tasks.task2_gamemenu import GameMenu
from tasks.task2_gamewon import GameWon


class MyASGEGame(pyasge.ASGEGame):
    """The ASGE Game in Python."""

    def __init__(self, settings: pyasge.GameSettings):
        """
        The constructor for the game.

        The constructor is responsible for initialising all the needed
        subsystems,during the game's running duration. It directly
        inherits from pyasge.ASGEGame which provides the window
        management and standard game loop.

        :param settings: The game settings
        """
        pyasge.ASGEGame.__init__(self, settings)
        self.renderer.setClearColour(pyasge.COLOURS.BLACK)
        self.renderer.setBaseResolution(1920, 1080, pyasge.ResolutionPolicy.MAINTAIN)
        random.seed(a=None, version=2)

        # create a game data object, we can store all shared game content here
        self.data = GameData()
        self.data.cursor = pyasge.Sprite()
        self.data.game_map = GameMap(self.renderer)
        self.data.game_res = [1920, 1080]
        self.data.inputs = self.inputs
        self.data.player = Player()
        self.data.renderer = self.renderer

        # setup the background and load the fonts for the game
        self.init_audio()
        self.init_cursor()
        self.init_fonts()

        # register the key and mouse click handlers for this class
        self.key_id = self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.key_handler)
        self.mouse_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click_handler)
        self.mousemove_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_MOVE, self.move_handler)

        # start the game in the menu
        self.current_state = GameMenu(self.data)

    def init_cursor(self):
        """Initialises the mouse cursor and hides the OS cursor."""
        self.data.cursor.loadTexture("./data/sprites/cursors/crosshairs.png")
        self.data.cursor.width = 32
        self.data.cursor.height = 32
        self.data.cursor.src_rect = [0, 0, 128, 128]
        self.data.cursor.scale = 1
        self.data.cursor.z_order = 127
        self.data.cursor.opacity = 0.75
        self.data.cursor.colour = pyasge.COLOURS.HOTPINK
        self.data.cursor.setMagFilter(pyasge.MagFilter.NEAREST)
        self.inputs.setCursorMode(pyasge.CursorMode.HIDDEN)

    def init_audio(self) -> None:
        """Plays the background audio."""
        self.data.audio_system.init()
        self.data.bg_audio = self.data.audio_system.create_sound("./data/audio/the-buccaneers-haul.ogg", mode=MODE.LOOP_NORMAL)
        self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_audio)
        self.data.bg_audio_channel.volume = 0.25

    def init_fonts(self) -> None:
        """Loads the game fonts."""
        self.data.fonts['game'] = self.renderer.loadFont('./data/fonts/Kenney Pixel Square.ttf', 28, 4)
        self.data.fonts['debug'] = self.renderer.loadFont('./data/fonts/Kenney Future.ttf', 28)

        metrics = pyasge.AtlasMetrics()
        metrics.id = "erbos"
        metrics.size = 64
        metrics.range = 4
        metrics.em_size = 1
        metrics.line_height = 0.5625
        metrics.ascender = -0.5625
        metrics.descender = 0
        self.data.fonts['score'] = self.renderer.loadFontAtlas(metrics, './data/fonts/erbos.png', './data/fonts/erbos.csv')
        self.data.fonts['score'].setMagFilter(pyasge.MagFilter.NEAREST)

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        """Handles the mouse movement and delegates to the active state."""
        self.data.cursor.x = event.x - self.data.cursor.width * 0.5
        self.data.cursor.y = event.y - self.data.cursor.height * 0.5
        self.current_state.move_handler(event)

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        """Forwards click events on to the active state."""
        self.current_state.click_handler(event)

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        """Forwards Key events on to the active state."""
        self.current_state.key_handler(event)
        if event.key == pyasge.KEYS.KEY_ESCAPE:
            self.signalExit()

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        """Processes fixed updates."""
        self.current_state.fixed_update(game_time)
        self.data.audio_system.update()

    # Imported methods
    from tasks.task2_update import update

    def render(self, game_time: pyasge.GameTime) -> None:
        """Renders the game state and mouse cursor"""
        self.current_state.render(game_time)
        self.renderer.render(self.data.cursor)



