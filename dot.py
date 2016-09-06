# -*- coding: utf-8 -*-
import random
from cocos.actions import MoveTo, CallFuncS
from cocos.sprite import Sprite

import define

class Dot(Sprite):
    def __init__(self, pos=None, color=None):
        if color is None:
            color = random.choice(define.ALL_COLOR)

        super(Dot, self).__init__('circle.png', color=color)
        self.killed = False
        if pos is None:
            self.position = (random.randint(40, define.WIDTH - 40),
                             random.randint(40, define.HEIGHT - 40))
            self.is_big = False
            self.scale = 0.8
        else:
            self.position = (pos[0] + random.random() * 32 - 16,
                             pos[1] + random.random() * 32 - 16)
            self.is_big = True
        self.tag = "Dot[%d,%d]"%(self.position[0],self.position[1])
        #self.schedule_interval(self.update, random.random() * 0.2 + 0.1)

    def reposition(self):
        self.position = (random.randint(40, define.WIDTH - 40),
                             random.randint(40, define.HEIGHT - 40))

    # def update(self, dt):
    #     arena = self.parent.parent
    #     snake = arena.snake

    def check_kill(self, snake):
        if (not self.killed and not snake.is_dead) and (
            abs(snake.x - self.x) < 32 and abs(snake.y - self.y) < 32
        ):
            self.do(MoveTo(snake.position, 0.1))
            return True
        return False
