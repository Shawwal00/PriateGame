import pyasge

from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID
from game.gamedata import GameData


class GameOver(GameState):

    def __init__(self, data: GameData) -> None:
        super().__init__(data)
        self.id = GameStateID.GAME_OVER
        self.initText()
        self.transition = False

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        print("processing click event")

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        print("processing key event")
        if event.key == pyasge.KEYS.KEY_M:
            self.transition = True

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        print("processing mouse move event")

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        pass

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        """ If user_clicked go to game menu else return GAME_OVER """
        if self.transition:
            return GameStateID.START_MENU
        return GameStateID.GAME_OVER

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.render(self.loseText)
        self.data.renderer.render(self.again_text)

    def initText(self):
        self.loseText = pyasge.Text(self.data.fonts['game'])
        self.loseText.string = "You have lost"
        self.loseText.position = [600, 300]
        self.loseText.scale = 3
        self.loseText.colour = pyasge.COLOURS.BLACK

        self.again_text = pyasge.Text(self.data.fonts['game'])
        self.again_text.string = "Press M to go back to the menu"
        self.again_text.position = [475, 600]
        self.again_text.scale = 1.7
        self.again_text.colour = pyasge.COLOURS.BLACK