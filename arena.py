import cocos
from cocos.director import director

import define
from snake import Snake,SnakeAI
from dot import Dot

class Arena(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(Arena, self).__init__(250, 255, 255, 255, define.WIDTH, define.HEIGHT)
        self.center = (director.get_window_size()[0] / 2, director.get_window_size()[1] / 2)
        self.batch = cocos.batch.BatchNode()
        self.add(self.batch)

        self.snake = Snake()
        self.add(self.snake, 10000)
        self.snake.init_body()

        self.enemies = []
        self.dots = []
        for i in range(7):
            self.add_enemy()

        self.keys_pressed = set()

        for i in range(50):self.add_dot()

        self.schedule(self.update)

    def add_enemy(self):
        enemy = SnakeAI()
        self.add(enemy, 10000)
        enemy.init_body()
        self.enemies.append(enemy)

    def remove_enemy(self, snake):
        self.remove(snake)
        self.enemies.remove(snake)

    def add_dot(self):
        d = Dot()
        self.dots.append(d)
        self.batch.add(d,name=d.tag)

    def remove_dot(self, dot):
        self.batch.remove(dot.tag)
        self.dots.remove(dot)

    def detect_collision(self):
        snakes = self.enemies + [self.snake]
        sn = len(snakes)
        for i in range(sn):
            for j in range(sn):
                sni = snakes[i]
                snj = snakes[j]
                if (i!=j):
                    if sni.check_crash(snj):
                        if self.snake == sni:
                            self.parent.end_game()
                        else:
                            self.remove(sni)
                            self.add_enemy()

                        for b in sni.body:
                            self.batch.add(Dot(b.position, b.color))
                            self.batch.add(Dot(b.position, b.color))
                            self.batch.remove(b)

        for snake in snakes:
            for dot in self.dots:
                if dot.check_kill(snake):
                    snake.add_score(2 if dot.is_big else 1)
                    if snake == self.snake: self.parent.update_score()
                    self.remove_dot(dot)


    def update(self, dt):
        self.x = self.center[0] - self.snake.x
        self.y = self.center[1] - self.snake.y
        self.detect_collision()

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        self.snake.update_angle(self.keys_pressed)

    def on_key_release (self, key, modifiers):
        self.keys_pressed.remove(key)
        self.snake.update_angle(self.keys_pressed)
