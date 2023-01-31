from ursina import *

class DraggableOrb(Draggable):
    types = {
        "mist": color.azure,
        "light": color.yellow,
        "seed": color.green
    }

    def __init__(self, name, **kwargs):
        super().__init__()(scale=.1, texture='orb', color=DraggableOrb.types[name], lock=(0,1,1), x=-.5+(i*.14))

    def drag():
        self.start_position = self.position

    def drop():
        self.position = self.start_position
