import pyasge

from game.shipcondition import ShipCondition


def update_healthy(ship, game_time: pyasge.GameTime):
    """ The first of your FSM functions, this one is complete """
    ship.ship_condition = ShipCondition.HEALTHY
    if ship.hp <= 6:
        ship.fsm.setstate(ship.update_damaged)

def update_damaged(ship, game_time: pyasge.GameTime):
    """ Create the logic here for the ship when it's damaged """
    ship.ship_condition = ShipCondition.DAMAGED
    if ship.hp <= 3:
        ship.fsm.setstate(ship.update_very_damaged)

def update_very_damaged(ship, game_time: pyasge.GameTime):
    """ Create the logic here for the ship when it's very damaged """
    ship.ship_condition = ShipCondition.VERY_DAMAGED
    if ship.hp == 0:
        ship.fsm.setstate(ship.deaded)

def deaded(ship, game_time: pyasge.GameTime):
    """ Create the logic here for the ship is sunk """
    ship.ship_condition = ShipCondition.SUNK


