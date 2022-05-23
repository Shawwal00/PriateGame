""" These enums are helpers for showing the correct sprite"""
from enum import IntEnum


class ShipCondition(IntEnum):
    """
    Each enum represents a ship's state and can be used to
    control various aspects of the game's logic and rendering.
    """
    HEALTHY = 0
    DAMAGED = 1
    VERY_DAMAGED = 2
    SUNK = 3
