from ursina import *
from spells import Spells, rarity_colors

class SpellTree(Entity):
    def __init__(self, enabled=False, **kwargs):
        super().__init__(parent=camera.ui, enabled=enabled, z=-10, **kwargs)
        from draggable_orb import DraggableOrb
        self.bg = Sprite('shore', parent=self, ppu=1080, color=hsv(0,0,0,.9), z=2)

        combinations = [value for (key,value) in Spells.__dict__.items() if key.startswith('Combination_')]
        # print(combinations)
        orb_parent = Entity(parent=self, scale=.1, y=.25)
        layers = [Entity(parent=orb_parent, y=-i*2) for i in range(3)]

        for y, combo in enumerate(combinations):
            level = sum([int(e) for e in combo.__name__[-3:]])
            print(f'{combo.__name__}  (lvl: {level})')
            orb = DraggableOrb([int(e) for e in combo.__name__[-3:]], parent=layers[level-1], ignore=True)
            orb.tooltip.text = ''

            spells = [value for (key,value) in combo.__dict__.items() if not key.startswith('_')]
            for s in spells:
                print(' aaaaaa', s.__name__, rarity_colors[level-1])
                orb.tooltip.text = f'<{rarity_colors[level-1]}>{s.__name__}<default>\n'
                # orb.tooltip.text += f'<scale:.75>{s.description}'
                print(orb.tooltip.raw_text)

            orb.tooltip.create_background()

        for e in layers:
            grid_layout(e.children, origin=(0,0,0), max_x=10)



if __name__ == '__main__':
    app = Ursina()
    st = SpellTree(enabled=True)

    EditorCamera()
    app.run()
