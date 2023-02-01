from ursina import *

class DraggableOrb(Draggable):

    def __init__(self, orb, x, **kwargs):
        self.orb = orb
        super().__init__(scale=.1, texture='orb', color=color.white, lock=(0,1,1), x=x)

    def drag():
        self.start_position = self.position

    def drop():
        self.position = self.start_position