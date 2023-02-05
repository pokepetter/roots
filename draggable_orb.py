from ursina import *
from enemy import Enemy
import spells

orb_colors = [color.orange, color.lime, color.azure]
orb_shapes = ['quad', 'quad', 'circle']

def is_valid_combination(orb_type_a, orb_type_b):
    return sum(orb_type_a) + sum(orb_type_b) <= 3


class DraggableOrb(Draggable):
    def __init__(self, orb_type=[1,0,0], **kwargs):
        super().__init__(model='quad', color=hsv(0,0,.9), texture='roots_orb', **kwargs)
        self.empty_color = color.clear
        self.sub_orbs = [Entity(parent=self, model='quad', texture='orb', z=-.001, scale=.3, color=self.empty_color, position=Vec2(pos)*.8) for pos in ((0,.2), (.15,-.1), (-.15,-.1))]
        self.tooltip = Tooltip('<yellow>...')
        self._prev_target = None

        self.orb_type = orb_type

        for key, value in kwargs.items():
            setattr(self, key, value)


    def update(self):
        super().update()
        if self.dragging:
            entities_under_mouse = [hit_info.entity for hit_info in mouse.collisions]
            targets = [e for e in entities_under_mouse if isinstance(e, (DraggableOrb)) and not e == self]
            if not targets:
                BATTLE.merge_result.enabled = False
                return

            target = targets[0]
            if isinstance(target, DraggableOrb) and is_valid_combination(self.orb_type, target.orb_type):
                new_orb_type = [sum(e) for e in zip(target.orb_type, self.orb_type)]
                spell = spells.get_spell_for_combination(new_orb_type)
                target.tooltip.enabled = False

                BATTLE.merge_result.enabled = True
                if target != self._prev_target:
                    combine_text =(
                    f'<gold>Combine into:\n'
                    f'<{spells.rarity_colors[sum(new_orb_type)-1]}>\n'
                    f'{spell.__name__}\n<default><scale:.75>{spell.description}<scale:1>\n'
                    )

                    BATTLE.merge_result.text = combine_text
                    BATTLE.merge_result.wordwrap = 40
                    BATTLE.merge_result.create_background(padding=.05, color=hsv(40,.5,.1,.98))
                    self._prev_target = target


    def drag(self):
        self.start_position = self.position
        self.z = -10
        #ursfx([(0.0, 1.0), (0.13, 0.5), (0.16, 0.2), (0.41, 0.0), (1.0, 0.0)], volume=0.3, wave='sine', pitch=random.randint(12,16), speed=3.2)


    def drop(self):
        BATTLE.merge_result.enabled = False
        # from battle import Enemy
        mouse.update()
        entities_under_mouse = [hit_info.entity for hit_info in mouse.collisions]
        targets = [e for e in entities_under_mouse if isinstance(e, (Enemy, DraggableOrb)) and not e == self]

        if not targets:
            self.position = self.start_position
            return


        target = targets[0]
        if isinstance(target, Enemy):
            print('---------------USE ORB')
            self.spell.use(target, PLAYER, BATTLE)
            ursfx([(0.0, 0.0), (0.1, 0.9), (0.19, 0.81), (0.24, 0.07), (1.0, 0.0)], volume=0.5, wave='noise', pitch=-18, speed=2.0)

        if isinstance(target, DraggableOrb):
            if BATTLE.actions_left <= 0:
                self.position = self.start_position
                return

            if not is_valid_combination(self.orb_type, target.orb_type):
                self.position = self.start_position
                print_on_screen("<red>CAN'T COMBINE", position=Vec3(mouse.position.xy, -10), origin=(0,-1))
                ursfx([(0.0, 0.0), (0.11, 0.74), (0.19, 0.81), (0.34, 0.47), (1.0, 0.0)], volume=0.19, wave='square', pitch=-9, pitch_change=-8, speed=3.2)
                return

            combine_impact = Text('COMBINE', position=Vec3(mouse.position.xy, -10), origin=(0,-1),color=color.clear)
            combine_impact.animate('y', combine_impact.y+.1, duration=.1)
            combine_impact.fade_in(duration=.2)
            destroy(combine_impact, delay=.2)
            ursfx([(0.0, 0.0), (0.1, 0.9), (0.19, 0.58), (0.38, 0.3), (0.56, 0.0)], volume=0.75, wave='triangle', pitch=8, pitch_change=10, speed=1.0)


            new_orb_type = [sum(e) for e in zip(target.orb_type, self.orb_type)]
            target.orb_type = new_orb_type
            BATTLE.actions_left -= 1
            destroy(self)
            BATTLE.reorder_orbs()
            return

        BATTLE.bag.append(self.orb_type)    # add back to the bottom of the bag
        BATTLE.bag = BATTLE.bag
        BATTLE.actions_left -= 1
        BATTLE.update_gui()
        destroy(self)
        BATTLE.reorder_orbs()
        return


    @property
    def orb_type(self):
        return self._orb_type

    @orb_type.setter
    def orb_type(self, value):
        self._orb_type = value
        import spells
        self.spell = spells.get_spell_for_combination(value)

        level = sum(value)
        self.tooltip.text = f'<{spells.rarity_colors[level-1]}>{self.spell.__name__}\n<default><scale:.75>{self.spell.description}'
        self.tooltip.create_background()

        for e in self.sub_orbs:         # reset suborbs
            e.color = self.empty_color

        n = 0
        for i, particle in enumerate(value):
            for j in range(particle):
                self.sub_orbs[n].color = orb_colors[i]
                # self.sub_orbs[n].model = copy(orb_shapes[i])
                n += 1

        # self.scale = 1.5
        # self.animate_scale(1, duration=.5)
        # print('set orb type to:', value)


if __name__ == '__main__':
    app = Ursina()
    import battle
    DraggableOrb(scale=.1)
    DraggableOrb(scale=.1, x=.15)

    app.run()
