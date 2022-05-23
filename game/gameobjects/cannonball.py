import pyasge
CANNONBALL_SPEED = 8


class Cannonball:

    """Represents a cannonball projectile that can be fired"""
    def __init__(self, spawn: pyasge.Point2D, dest: pyasge.Point2D) -> None:
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("data/sprites/ship parts/cannonBall.png")
        self.sprite.width = 10
        self.sprite.height = 10
        self.sprite.x = spawn.x
        self.sprite.y = spawn.y
        self.sprite.z_order = 50
        self.destination = pyasge.Point2D(dest.x - self.sprite.width * 0.5, dest.y - self.sprite.width * 0.5)

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        self.sprite.x += (self.destination.x - self.sprite.x) * CANNONBALL_SPEED * game_time.fixed_timestep
        self.sprite.y += (self.destination.y - self.sprite.y) * CANNONBALL_SPEED * game_time.fixed_timestep

    def update(self, game_time: pyasge.GameTime) -> None:
        if self.destination.distance([self.sprite.x, self.sprite.y]) < 5:
            self.sprite.z_order = 0

        if abs(self.destination.x - self.sprite.x) < 0.01:
            self.sprite.x = self.destination.x

        if abs(self.destination.y - self.sprite.y) < 0.01:
            self.sprite.y = self.destination.y

    def render(self, renderer: pyasge.Renderer, game_time: pyasge.GameTime) -> None:
        renderer.render(self.sprite)

    @property
    def position(self) -> pyasge.Point2D:
        return pyasge.Point2D(self.sprite.x, self.sprite.y)

    @property
    def world_bounds(self):
        return self.sprite.getWorldBounds()
