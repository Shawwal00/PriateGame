import pyasge
from pyfmodex.flags import MODE


from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID
from game.gamedata import GameData



class GameMenu(GameState):

    def __init__(self, gamedata: GameData) -> None:
        super().__init__(gamedata)
        self.id = GameStateID.START_MENU
        self.transition = False
        self.background = pyasge.Sprite()
        self.playButton = pyasge.Sprite()
        self.quitButton = pyasge.Sprite()
        self.initBackground()
        self.initText()
        self.initPlay()
        self.initQuit()

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        if self.isInside(self.playButton, event.x, event.y):
            self.transition = True
        if self.isInside(self.quitButton, event.x, event.y):
            quit()

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if event.key == pyasge.KEYS.KEY_ENTER:
            self.transition = True

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        pass

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        pass

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if self.transition:
            self.transition = False
            return GameStateID.GAMEPLAY

        return GameStateID.START_MENU

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.render(self.background)
        self.data.renderer.render(self.menuText)
        self.data.renderer.render(self.playButton)
        self.data.renderer.render(self.quitButton)

    def initBackground(self) -> bool:

        if self.background.loadTexture("/data/sprites/backdrops/Sample.png"):
            # loaded, so make sure this gets rendered first
            self.background.z_order = -100
            self.background.scale = 2.1
            return True
        else:
            return False

    def initText(self) -> bool:
        self.menuText = pyasge.Text(self.data.fonts['game'])
        self.menuText.string = "The Ship game"
        self.menuText.position = [450, 300]
        self.menuText.scale = 5
        self.menuText.colour = pyasge.COLOURS.BLACK
        return True

    def initPlay(self)-> bool:
        if self.playButton.loadTexture("/data/Levelgreen-min.png"):
            # loaded, so make sure this gets rendered first
            self.playButton.z_order = -10
            self.playButton.x = 450
            self.playButton.y = 500
            return True
        else:
            return False

    def initQuit(self)-> bool:
        if self.quitButton.loadTexture("/data/Levelreoundred-min.png"):
            # loaded, so make sure this gets rendered first
            self.quitButton.z_order = -10
            self.quitButton.x = 950
            self.quitButton.y = 500
            return True
        else:
            return False

    def isInside(self, sprite, mouse_x, mouse_y) -> bool:
        bounds = sprite.getWorldBounds()
        yOffset = 150
        xOffset = 200

        if bounds.v1.x + xOffset < mouse_x < bounds.v2.x - xOffset and bounds.v1.y + yOffset < mouse_y < bounds.v3.y -\
                yOffset:

            return True

        return False