import pyasge as pyasge

from game.gamedata import GameData
from game.gamestates.gamestate import GameState, GameStateID


class GameWon(GameState):

    def __init__(self, data: GameData) -> None:
        super().__init__(data)
        self.id = GameStateID.WINNER_WINNER
        self.transition = False
        self.initText()

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        pass

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if event.key == pyasge.KEYS.KEY_M:
            self.transition = True

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        pass

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        pass

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if self.transition:
            return GameStateID.START_MENU

        return GameStateID.WINNER_WINNER

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.render(self.win_text)
        self.data.renderer.render(self.again_text)

    def initText(self):
        self.win_text = pyasge.Text(self.data.fonts['game'])
        self.win_text.string = "Congrats, you have won"
        self.win_text.position = [400, 300]
        self.win_text.scale = 3
        self.win_text.colour = pyasge.COLOURS.BLACK

        self.again_text = pyasge.Text(self.data.fonts['game'])
        self.again_text.string = "Press M to go back to the menu"
        self.again_text.position = [475, 600]
        self.again_text.scale = 1.7
        self.again_text.colour = pyasge.COLOURS.BLACK