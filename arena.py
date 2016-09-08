import cocos
from cocos.director import director

import define
from snake import Snake,SnakeAI,MySnakeAI
from dot import Dot
from quadtree import QuadTree

class Arena(cocos.layer.ColorLayer):
    is_event_handler = True
    MAX_DOTS = 50
    MAX_SNAKES = 5

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
        self.keys_pressed = set()
        self.init_pool()

        for i in range(7):self.add_enemy()
        for i in range(5):self.add_dot()

        self.schedule(self.update)

    def init_pool(self):
        self.dot_pool = []
        for i in range(Arena.MAX_DOTS):
            d = Dot()
            d.disable()
            self.dot_pool.append(d)
            self.batch.add(d,name=d.tag)

        self.snake_pool = []
        for i in range(Arena.MAX_SNAKES):
            enemy = SnakeAI()
            enemy.disable()
            self.snake_pool.append(enemy)
            self.add(enemy, 10000)
            enemy.init_body()


    def add_enemy(self):
        if len(self.snake_pool) == 0: return
        enemy = self.snake_pool.pop()
        enemy.enable()
        self.enemies.add(enemy)

    def remove_enemy(self, enemy):
        enemy.disable()
        self.enemies.remove(enemy)
        self.snake_pool.insert(0,enemy)

    def add_dot(self):
        if len(self.dot_pool) == 0: return
        dot = self.dot_pool.pop()
        dot.enable()
        self.dots.add(dot)

    def add_snake_dot(self,pos,color):
        if len(self.dot_pool) == 0: return
        dot = self.dot_pool.pop()
        dot.enable()
        dot.position = pos
        dot.color = color
        self.dots.add(dot)

    def remove_dot(self, dot):
        dot.disable()
        self.dots.remove(dot)
        self.dot_pool.insert(0,dot)

    def detect_collision(self):
        snakes = set(self.enemies)
        snakes.add(self.snake)
        dots = self.dots
        quad = QuadTree(3,(0,0,define.WIDTH,define.HEIGHT),snakes,dots)
        def onSnakeCollide(snake):
            if self.snake == snake:
                self.parent.end_game()
            else:
                for b in snake.body:
                    self.add_snake_dot(b.position,b.color)
                    self.batch.remove(b)

                self.add_enemy()
        def onSnakeDotCollide(dot,snake):
            #print 'snake dot',dot.tag, dot.position
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
