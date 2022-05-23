"""
This is the pathfinding script.

You will need to complete the resolve function in order to
get movement to work correctly. You should start with
BFS and consider more advanced approaches if you have time.

The function will take a player's mouse click and return a
list of tile locations it needs to visit in order to get
to its destination.

note: you should also use this pathfinding function for task4
"""

import pyasge
from game.gamedata import GameData


def resolve(xy: pyasge.Point2D, data: GameData):
    """
    Resolves the path needed to get to the destination point.

    Making use of the cost map, a suitable search algorithm should
    be used to create a series of tiles that the ship may pass
    through. These tiles should then be returned as a series of
    positions in world space.

    :param xy: The destination for the ship
    :param data: The game data, needed for access to the game map
    :return: list[pyasge.Point2D]
    """
    # convert point to tile location
    tile_loc = data.game_map.tile(xy)

    # use these to make sure you don't go out of bounds when checking neighbours
    map_width = data.game_map.width
    map_height = data.game_map.height

    # here's an example of tiles that the player should visit

    start = data.game_map.tile(pyasge.Point2D(data.player.x, data.player.y))

    path = []
    frontier = []
    tileX = []
    tileY = []
    tile_distribution = 0
    route = dict()

    """The below is setting up the lists"""
    tileX.append(data.player.x)
    tileY.append(data.player.y)
    frontier.append(start)
    main_tile = data.game_map.tile(pyasge.Point2D(tileX[0], tileY[0]))

    while len(frontier) > 0:
        before_tile = frontier[0]
        frontier.pop(0)

        """The offsetts are 128 due to the tile size"""
        offsettY = 128
        offsettX = 0

        if tile_distribution > 0:
            tileX.pop(0)
            tileY.pop(0)

        tile_distribution = 0

        """The below is looking at the tiles around the starting tile and 
        then looks at the tiles around the next frontier[0] """
        for i in range(4):
            if main_tile == data.game_map.tile(xy):
                break
            main_tile = data.game_map.tile(pyasge.Point2D(tileX[0] + offsettX, tileY[0] + offsettY))

            if 0 < main_tile[0] < map_width and 0 < main_tile[1] < map_height:

                tile_cost = data.game_map.costs[main_tile[1]][main_tile[0]]
                if tile_cost <= 1:
                    if (abs(main_tile[0] - tile_loc[0])) <= abs((before_tile[0] - tile_loc[0])) and\
                            abs((main_tile[1] - tile_loc[1])) <= abs((before_tile[1] - tile_loc[1])):
                        frontier.append(main_tile)
                        route[main_tile] = before_tile
                        tileX.append(tileX[0] + offsettX)
                        tileY.append(tileY[0] + offsettY)
                    else:
                        pass

            tile_distribution = tile_distribution + 1
            """Will start with the top tile then go to the left tile 
            then to the bottom tile then to the right tile"""
            if offsettX == 0 and offsettY == -128:
                offsettX = offsettX + 128
            elif offsettX < -127:
                offsettX = offsettX + 128
            else:
                offsettX = offsettX - 128

            if offsettY > -127:
                offsettY = offsettY - 128
            else:
                offsettY = offsettY + 128

        if main_tile == data.game_map.tile(xy):
            break

    """The dictionary will create a set of links between
    the various tiles so that it can be followed to get from the start to the end"""
    current = data.game_map.tile(xy)
    while current != start:
        path.append(current)
        current = route[current]
    path.append(start)
    path.reverse()
    # convert everything to a world position
    for i in range(len(path)):
        path[i] = data.game_map.world(path[i])
    return path
