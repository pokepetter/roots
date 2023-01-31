from ursina import *


app = Ursina()

import battle
battle.start('enemy')

# Entity(parent=camera.ui, model='quad', collider='box', on_click=Func(print,'hei'))
for i in range(5):
    orb = Draggable(scale=.1, texture='orb', color=color.white, lock=(0,1,1), x=-.5+(i*.14))
    orb.tooltip = Tooltip(text=f'orb {i}')

def my_drop():
    print('dropped oirugherigohrsiug')

orb.drop = my_drop


app.run()
