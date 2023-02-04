from ursina import *
from ursina.prefabs.health_bar import HealthBar


class Enemy(Entity):
    def __init__(self, max_health, **kwargs):
        super().__init__(model='quad', collider='box', scale=(.3,.3), color=color.white, texture='rutabaga', name='enemy', **kwargs)
        self.health_bar = HealthBar(max_value=max_health, scale_x=.2, world_parent=self, position=Vec3(-.1,.6,0))
        self.health_bar.x = -self.health_bar.scale_x / 2
        self.max_hp = max_health
        self._hp = max_health
        self.hp = max_health
        self.block = 0
        self.strength = 0
        self.enemy_ui = Entity(parent=self, position=(0.5,.5), scale=.2)
        self.strength_label = Button(parent=self.enemy_ui, position=(1,-1.25), text=f'{self.strength}', tooltip=Tooltip('Strength increases Damage dealt'), color=color.orange)
        self.intention_label = Button(parent=self, position=(-1,0), text='', tooltip=Tooltip('Next move that the enemy will perform'), color=color.black66, scale=.4)
        self.intention_label.scale_x = 1
        self.update_next_move_text(1)

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        print(f'set enemy hp from {self._hp} to {value}')
        value = clamp(value, 0, self.max_hp)
        self.health_bar.value = value

        if value < self._hp:
            print('ow!')
            self.blink(color.red, duration=.2)
            self.shake(duration=.2, magnitude=.03)

        if value <= 0:
            self.die()

        elif value > self._hp:
            print('heal enemy')

        self._hp = value

    def damage(self, damage):
        damage_taken = damage - self.block
        if damage_taken < 0:
            damage_taken = 0
            self.block -= damage
        else:
            self.block = 0
        self.health_bar.value -= damage_taken
        self._hp -= damage_taken
        if self._hp <= 0:
            self.die()

    def heal(self, heal):
        self._hp += heal
        self.health_bar.value += heal
        if (self._hp > self.max_hp):
            self._hp = self.max_hp
            self.health_bar.value = self.max_hp

    def die(self):
        BATTLE.enemies.remove(self)
        BATTLE.check_for_win()
        destroy(self, delay=.1)

    def update_next_move_text(self, turn_count):
        if (turn_count % 3 == 1):
            self.intention_label.text = f'Deal {5 + self.strength} Damage'
        elif (turn_count % 3 == 2):
            self.intention_label.text = f"Deal {3 + self.strength} Damage \nand Gain 3 Block"
        else:
            self.intention_label.text = "Gain 2 Strength"

    def do_next_move(self, turn_count):
        if (turn_count % 3 == 1):
            PLAYER.damage(5 + self.strength)
        elif (turn_count % 3 == 2):
            PLAYER.damage(3 + self.strength)
            self.block += 3
        else:
            self.strength += 2
            self.strength_label.text = f'self.strength'