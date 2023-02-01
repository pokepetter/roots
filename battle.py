from ursina import *
import player
from draggableOrb import *

if __name__ == '__main__':
    app = Ursina()

# code here
def start(enemy='default_enemy'):
    enemy

for i, orb in enumerate(player.orbs):
    draggableOrb = DraggableOrb(orb=player.orbs[i], x=-.5+(i*.14))
    draggableOrb.tooltip = Tooltip(text=f'{player.orbs[i].getName()}')

if __name__ == '__main__':
    app.run()
