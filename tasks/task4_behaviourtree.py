""" Define your behaviour tree and its node types here. """

from enum import IntEnum


class NodeType(IntEnum):
    SELECTOR = 1
    SEQUENCE = 2
    DECORATOR = 3
    LEAF = 4


class BehaviourTree:
    def __init__(self):
        pass


class Node:
    def __init__(self):
        pass
