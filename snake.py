# -*- coding: utf-8 -*-
import math
import random
import cocos

from cocos.sprite import Sprite
import define


class Snake(cocos.cocosnode.CocosNode):
    def __init__(self):
        super(Snake, self).__init__()
        self.is_dead = False
        self.angle = random.randrange(360)  # 目前角度
        self.angle_dest = self.angle  # 目标角度
        self.color = random.choice(define.ALL_COLOR)
        self.position = random.randrange(700, 900), random.randrange(350, 450)
        self.speed = 180
        self.path = [self.position] * 100
        self.body = []
        self.schedule(self.update)

    def disable(self):
        self.visible = False
        self.x = -100
        self.y = -100
        self.is_dead = True

    def enable(self):
        self.visible = True
        self.position = random.randrange(700, 900), random.randrange(350, 450)
        self.x = self.position[0]
        self.y = self.position[1]
        self.is_dead = False

    def add_body(self):
        b = Sprite('circle.png', color=self.color)
        b.scale = 1.5
        self.body.append(b)
        if self.x == 0: print self.position
        b.position = self.position
        self.parent.batch.add(b, 9999 - len(self.body))

    def init_body(self):
        def add_eye(lr):
            eye = Sprite('circle.png')
            eye.y = 5*lr
            eye.scale = 0.5
            eyeball = Sprite('circle.png', color=define.BLACK)
            eyeball.scale = 0.5
            eye.add(eyeball)
            self.head.add(eye)
        self.score = 30
        self.length = 4

        self.head = Sprite('circle.png', color=self.color)
        self.scale = 1.5
        self.add(self.head)
        add_eye(1)
        add_eye(-1)

        for i in range(self.length):
            self.add_body()

    def update(self, dt):
        self.angle = (self.angle + 360) % 360

        if self.is_dead:return

        if abs(self.angle - self.angle_dest) < 2:
            self.angle = self.angle_dest
        else:
            if (0 < self.angle - self.angle_dest < 180) or (
                self.angle - self.angle_dest < -180):
                self.angle -= 500 * dt
            else:
                self.angle += 500 * dt
        self.head.rotation = -self.angle

        self.x += math.cos(self.angle * math.pi / 180) * dt * self.speed
        self.y += math.sin(self.angle * math.pi / 180) * dt * self.speed
        self.path.append(self.position)

        lag = int(round(1100.0 / self.speed))
        for i in range(self.length):
            idx = (i + 1) * lag + 1
            self.body[i].position = self.path[-min(idx,len(self.path))]
            if self.body[i].x == 0:
                print self.body[i].position
        m_l = max(self.length * lag * 2, 60)
        if len(self.path) > m_l:
            self.path = self.path[-m_l * 2:]

    def update_angle(self, keys):
        x, y = 0, 0
        if 65361 in keys:  # 左
            x -= 1
        if 65362 in keys:  # 上
            y += 1
        if 65363 in keys:  # 右
            x += 1
        if 65364 in keys:  # 下
            y -= 1
        directs = ((225, 180, 135), (270, None, 90), (315, 0, 45))
        direct = directs[x + 1][y + 1]
        if direct is None:
            self.angle_dest = self.angle
        else:
            self.angle_dest = direct

    def add_score(self, s=1):
        if self.is_dead:
            return
        self.score += s
        l = (self.score - 6) / 6
        if l > self.length:
            self.length = l
            self.add_body()

    def check_crash(self, other):
        if self.is_dead or other.is_dead:
            return False
        if (self.x < 0 or self.x > define.WIDTH) or (
            self.y < 0 or self.y > define.HEIGHT
        ):
            self.crash()
            return True
        for b in other.body:
            dis = math.sqrt((b.x - self.x) ** 2 + (b.y - self.y) ** 2)
            if dis < 24:
                self.crash()
                return True

    def crash(self):
        if not self.is_dead:
            self.is_dead = True
            self.unschedule(self.update)
            #del self.path



class SnakeAI(Snake):
    def __init__(self):
        super(SnakeAI, self).__init__()
        self.position = random.randrange(300, 1300), random.randrange(200, 600)
        if 600 < self.x < 1000: self.x += 400
        self.speed = 150
        self.schedule_interval(self.ai, random.random() * 0.1 + 0.05)

    def ai(self, dt):
        self.angle_dest = (self.angle_dest + 360) % 360
        if (self.x < 100 and 90 < self.angle_dest < 270) or (
            self.x > define.WIDTH - 100 and (
                self.angle_dest < 90 or self.angle_dest > 270)
        ):
            self.angle_dest = 180 - self.angle_dest
        elif (self.y < 100 and self.angle_dest > 180) or (
            self.y > define.HEIGHT - 100 and self.angle_dest < 180
        ):
            self.angle_dest = -self.angle_dest

    def enable(self):
        self.visible = True
        self.position = random.randrange(300, 1300), random.randrange(200, 600)
        self.x = self.position[0]
        self.y = self.position[1]
        self.is_dead = False

    def crash(self):
        if not self.is_dead:
            self.is_dead = True
            #del self.path
            #del self.body
            self.unschedule(self.update)
            self.unschedule(self.ai)

class MySnakeAI(Snake):
    def __init__(self):
        super(MySnakeAI, self).__init__()
        self.dir = 0

    def update(self, dt):
        self.dir = random.randint(0,1)
        print self.dir
        if self.dir == 0: self.update_angle([65362])
        else: self.update_angle([65364])
        super(MySnakeAI, self).update(dt)

    def ai(self, quad):
        if quad.willSnakeCollide(self):
            pass


