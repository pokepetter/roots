from ursina import *
import player

if __name__ == '__main__':
    app = Ursina()

# code here
def start(enemy='default_enemy'):
    enemy

for i, e in enumerate(player.orbs):
    orb = Draggable(scale=.1, texture='orb', color=color.white, lock=(0,1,1), x=-.5+(i*.14))
    orb.tooltip = Tooltip(text=f'orb {player.orbs[i]}')

if __name__ == '__main__':
    app.run()
