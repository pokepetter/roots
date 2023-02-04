from ursina import *
from enemy import Enemy

orb_colors = [color.orange, color.lime, color.azure]
orb_shapes = ['quad', 'quad', 'circle']

class DraggableOrb(Draggable):
    def __init__(self, orb_type=[1,0,1], **kwargs):
        super().__init__(model='quad', color=hsv(0,0,.9), texture='roots_orb', **kwargs)
        self.empty_color = color.clear
        self.sub_orbs = [Entity(parent=self, model='quad', texture='orb', z=-.001, scale=.3, color=self.empty_color, position=Vec2(pos)*.8) for pos in ((0,.2), (.15,-.1), (-.15,-.1))]
        self.tooltip = Tooltip('...')

        self.orb_type = orb_type
        for key, value in kwargs.items():
            setattr(self, key, value)


    def drag(self):
        self.start_position = self.position
        self.z = -10

    def drop(self):
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

        if isinstance(target, DraggableOrb):
            if BATTLE.actions_left <= 0:
                self.position = self.start_position
                return

            if sum(target.orb_type) == 3:   # can't combine with a complete orb
                print_on_screen('<red>ALREADY FULL', position=Vec3(mouse.position.xy, -10), origin=(0,-1))
                self.position = self.start_position
                return

            print_on_screen('COMBINE', position=Vec3(mouse.position.xy, -10), origin=(0,-1))
            new_orb_type = [sum(e) for e in zip(target.orb_type, self.orb_type)]
            target.orb_type = new_orb_type
            BATTLE.actions_left -= 1
            destroy(self)
            BATTLE.reorder_orbs()
            return

        BATTLE.bag.append(self.orb_type)    # add back to the bottom of the bag
        BATTLE.bag = BATTLE.bag
        BATTLE.actions_left -= 1
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
        print('------------', self.spell)
        self.tooltip.text = f'<{spells.rarity_colors[level-1]}>{self.spell.__name__}\n<default>'
        self.tooltip.text += f'<scale:.75>{self.spell.description}'
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
