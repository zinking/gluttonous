import cocos
from cocos.director import director

import define
from snake import Snake,SnakeAI,MySnakeAI
from dot import Dot
from quadtree import QuadTree

class Arena(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(Arena, self).__init__(250, 255, 255, 255, define.WIDTH, define.HEIGHT)
        self.center = (director.get_window_size()[0] / 2, director.get_window_size()[1] / 2)
        self.batch = cocos.batch.BatchNode()
        self.add(self.batch)

        self.snake = MySnakeAI()
        self.snake = Snake()
        self.add(self.snake, 10000)
        self.snake.init_body()

        self.enemies = set([])
        self.dots = set([])
        for i in range(7):
            self.add_enemy()

        self.keys_pressed = set()

        for i in range(50):self.add_dot()

        self.schedule(self.update)

    def add_enemy(self):
        enemy = SnakeAI()
        self.add(enemy, 10000)
        enemy.init_body()
        self.enemies.add(enemy)

    def remove_enemy(self, snake):
        self.remove(snake)
        self.enemies.remove(snake)

    def add_dot(self, d = None):
        if d is None: d = Dot()
        self.dots.add(d)
        self.batch.add(d,name=d.tag)

    def remove_dot(self, dot):
        try:
            self.dots.remove(dot)
            self.batch.remove(dot.tag)
        except Exception,e:
            print e

    def detect_collision(self):
        snakes = set(self.enemies)
        snakes.add(self.snake)
        dots = self.dots
        quad = QuadTree(3,(0,0,define.WIDTH,define.HEIGHT),snakes,dots)
        def onSnakeCollide(snake):
            if self.snake == snake:
                self.parent.end_game()
            else:
                self.remove(snake)
                self.add_enemy()

            for b in snake.body:
                bdot = Dot(b.position, b.color)
                #self.batch.add(bdot)
                #self.batch.add(Dot(b.position, b.color))
                self.add_dot(bdot)
                self.batch.remove(b)
        def onSnakeDotCollide(dot,snake):
            snake.add_score(2 if dot.is_big else 1)
            if snake == self.snake: self.parent.update_score()
            self.remove_dot(dot)
            self.add_dot()

        quad.detect_collision(onSnakeCollide, onSnakeDotCollide)



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
