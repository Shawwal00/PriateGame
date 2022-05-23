import pyasge
from game.fsm import FSM
from game.gameobjects.ship import Ship
from tasks.task1_shipstates import update_healthy, update_damaged, update_very_damaged, deaded
from tasks.task4_behaviourtree import BehaviourTree


class Enemy(Ship):
    """
    An enemy ship

    This is a basic class to get you started. You will need to
    implement a number of improvements to it in order to complete
    the game. Provided within the class is an empty behaviour tree
    class for you to complete. You will need to create the structure
    and the nodes inside the `task4_behaviourtree.py` file and then
    hook the tree in to this class to allow for decision-making to
    work.
    """

    def __init__(self) -> None:
        super().__init__()

        filenames = ["data/sprites/ships/ship (4).png",
                     "data/sprites/ships/ship (10).png",
                     "data/sprites/ships/ship (16).png",
                     "data/sprites/ships/ship (22).png"]

        for filename in filenames:
            self.frames.append(pyasge.Sprite())
            self.frames[-1].loadTexture(filename)
            self.frames[-1].z_order = 2
            self.frames[-1].width = 66
            self.frames[-1].height = 113

        self.active_frame = self.frames[0]
        self.behaviour = BehaviourTree()

    def update(self, game_time: pyasge.GameTime) -> None:
        """ Updates the enemy and its FSM

        Calls the FSM for controlling the condition of the ship and will
        redraw the ship if it's current condition changes. This allows
        progressive damage to be shown using additional sprites.

        Args:
            game_time (pyasge.GameTime): The game time used for ticks
        """

        # update the fsm
        self.fsm.update(game_time)

        # if the ship's condition has changed we need to redraw it
        self.redraw()

    def render(self, renderer: pyasge.Renderer, game_time: pyasge.GameTime) -> None:
        """ Renders the enemy ship """
        renderer.render(self.active_frame)
