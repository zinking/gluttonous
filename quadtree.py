class QuadTree(object):

    def __init__(self,lvl,rect,snakes,dots):
        (x,y,w,h) = rect
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.lvl = lvl
        hw = w/2
        hh = h/2
        cx = x + w/2
        cy = y + h/2
        self.snakes = self.filterSnakes(snakes)
        self.dots = self.filterDots(dots)
        self.quads = []

        if lvl > 0:
            nw = QuadTree(lvl-1,(x,y,hw,hh),self.snakes,self.dots)
            ne = QuadTree(lvl-1,(cx,y,hw,hh),self.snakes,self.dots)
            sw = QuadTree(lvl-1,(x,cy,hw,hh),self.snakes,self.dots)
            se = QuadTree(lvl-1,(cx,cy,hw,hh),self.snakes,self.dots)
            self.quads = [nw,ne,sw,se]

    def detect_collision(self, snake_action, dot_action):
        if self.lvl > 0:
            for quad in self.quads: quad.detect_collision(snake_action,dot_action)
        elif self.lvl == 0:
            for si in self.snakes:
                for sj in self.snakes:
                    if si != sj and si.check_crash(sj): snake_action(si)

            for si in self.snakes:
                for dot in self.dots:
                    if dot.check_kill(si): dot_action(dot,si)


    def willSnakeCollide(self,s):
        sx,sy = s.x,s.y
        xwithin = (self.x <= sx < self.x + self.w)
        ywithin = (self.y <= sy < self.y + self.h)
        if not xwithin or not ywithin: return False
        if self.lvl > 0:
            for quad in self.quads:
                if (quad.willSnakeCollide(s)): return True
        elif self.lvl == 0:
            for si in self.snakes:
                if si != s and s.check_crash(si): return True


    def filterSnakes(self, snakes):
        rr = []
        for snake in snakes:
            for body in snake.body:
                sx,sy = body.x, body.y
                xwithin = (self.x <= sx < self.x + self.w)
                ywithin = (self.y <= sy < self.y + self.h)
                if  xwithin and ywithin:
                    rr.append(snake)
                    break
        return rr

    def filterDots(self, dots):
        rr = []
        for dot in dots:
            sx,sy = dot.x, dot.y
            xwithin = (self.x <= sx <= self.x + self.w)
            ywithin = (self.y <= sy <= self.y + self.h)
            if xwithin and ywithin:
                rr.append(dot)
        return rr


    def print_quad(self):
        if self.lvl > 0:
            for quad in self.quads: quad.print_quad()
        if self.lvl == 0:
            print "Quad","*"*15
            print "Rect:",self.x,self.y,self.w,self.h
            for snake in self.snakes:
                print "snake:",snake.x, snake.y
            print "*"*20

