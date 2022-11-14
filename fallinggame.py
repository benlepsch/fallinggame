"""
    written by ben lepsch
    UNFINISHED

    todos:
     - add a score counter
     - make it quit if you get pushed above the screen height
     - (maybe) fix the side collision oddness, but idk i kind of like how it feels
"""

import uvage as u
from random import randint

screen_width = 800
screen_height = 600

camera = u.Camera(screen_width, screen_height)

# turn on for print statment in terminal
debug = False

# the box things you have to jump thru
# actually each one will have a left and a right part
# actually no each one will be either a left or a right part
# then i'll make another class that keeps them in an array or something
# actually i have no idea
'''
    hjang on
    it will be easy to make each Thing either left or right
    but how do i do collisions
    actually keepign each THing left or right wil lmake collisions easier too i becha

        print(b1.touches(b2))         # True if they touch, False if they don't
        print(b1.touches(b2, -5, 10)) # if overlap by at least 5 in x and within 10 in y
        print(b1.bottom_touches(b2))  # True if b1's bottom edge touches b2
        print(b1.contains(17,21))     # True if the point (17, 21) is inside b1

        b1.move_to_stop_overlapping(b2)      # b1 will move, not b2 (also updates b1's speed)
        b1.move_both_to_stop_overlapping(b2) # b1 and b2 move same amount (and update speed
    
    they really just give you everything huh
'''
class Thing:
    def __init__(self, x, y, color, width, height):
        self.gb = u.from_color(x, y, color, width, height)
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0

    def update(self):
        global thing_up_speed
        self.gb.move(0, -thing_up_speed)
        self.left = self.gb.x - self.gb.width/2
        self.right = self.gb.x + self.gb.width/2
        self.top = self.gb.y - self.gb.height/2
        self.bottom = self.gb.y + self.gb.height/2
    
    def is_off_screen(self):
        # returning (self.bottom < 0) would make the Thing directly below the despawning 
        # thing flash for out of vision for a second, which was really distracting
        # doing this means that the next Thing is also off screen when the first one despawns
        return (self.bottom + screen_height) < 0

    def draw(self):
        camera.draw(self.gb)

# player object
class Player:
    def __init__(self):
        # position / velocity / acceleration variables
        self.x = 0
        self.y = 0
        self.x_vel = 0
        self.y_vel = 0
        self.x_acc = 0
        self.y_acc = 0

        # gravity constant
        self.gravity = 10

        # move speed
        self.msx = 10
        self.msy = 10

        # have a cap
        self.max_vel_x = 20
        self.max_vel_y = 20

        self.w = False # which image
        self.imgs = ['https://benlepsch.github.io/walk_left.png', 'https://benlepsch.github.io/walk_right.png']
        self.gb = u.from_image(self.x, self.y, self.imgs[self.w])

    # handle key input and call update()
    def get_keys(self):
        dx = dy = 0

        if u.is_pressing('left arrow'):
            dx -= self.msx
        if u.is_pressing('right arrow'):
            dx += self.msx
        
        if u.is_pressing('up arrow'):
            dy -= self.msy
        if u.is_pressing('down arrow'):
            dy += self.msy
        
        self.update(dx, dy)

    # update acceleration and velocity, move the player
    def update(self, dx=None, dy=None):
        # decay acceleration if the key isn't being held
        self.x_acc = dx if dx else (self.x_acc / 2 if (abs(self.x_acc) > 1) else 0)
        # commenting this out cause im not sure if i want jumping allowed or not
        # self.y_acc = dy if dy else (self.y_acc / 2 if (abs(self.y_acc) > 1) else 0)
        self.y_acc = self.gravity

        # update velocity + make sure it's within max velocity
        self.x_vel += self.x_acc
        self.y_vel += self.y_acc

        self.x_vel = self.x_vel if abs(self.x_vel) < self.max_vel_x else (self.max_vel_x if self.x_vel > 0 else -self.max_vel_x)
        self.y_vel = self.y_vel if abs(self.y_vel) < self.max_vel_y else (self.max_vel_y if self.y_vel > 0 else -self.max_vel_y)

        # make sure we won't go off the edges
        if (self.gb.bottom + self.y_vel) >= screen_height:
            self.y_vel = screen_height - self.gb.bottom
        if (self.gb.left + self.x_vel) <= 0:
            self.x_vel = -self.gb.left
        if (self.gb.right + self.x_vel) >= screen_width:
            self.x_vel = screen_width - self.gb.right


        # make sure we won't go thru any boxes
        self.left = self.x - self.gb.width/2
        self.right = self.x + self.gb.width/2
        self.top = self.y - self.gb.height/2
        self.bottom = self.y + self.gb.height/2

        global things
        for t in things:
            # i tried to use the built in collision functions like touches() and move_to_stop_overlapping()
            # but they sucked and i kept glitching inside ofthe boxes
            # so i do it myself
            if (self.bottom > t.top and self.top < t.top) and not ((self.left > t.right) or (self.right < t.left)):
                # print('hitting')
                # bottom touching
                self.gb.move(0, t.top - self.bottom)
                self.y += t.top - self.bottom
            if (self.top < t.bottom and self.bottom > t.bottom) and not ((self.left > t.right) or (self.right < t.left)):
                # top touching
                self.gb.move(0, t.bottom - self.top)
            if (self.left < t.right and self.right > t.right) and not ((self.top > t.bottom) or (self.bottom < t.top)):
                # left touching
                self.gb.move(t.right - self.left, 0)
            if (self.right > t.left and self.left < t.left) and not ((self.top > t.bottom) or (self.bottom < t.top)):
                # right touching
                self.gb.move(t.left - self.right, 0)


        # move the player
        self.x += self.x_vel
        self.y += self.y_vel

        if self.x_vel < 0:
            self.w = 0
        elif self.x_vel > 0:
            self.w = 1

        self.gb = u.from_image(self.x, self.y, self.imgs[self.w])

        if debug:
            print('x vel: {}\t y vel: {}\t x acc: {}\t y acc: {}'.format(self.x_vel, self.y_vel, self.x_acc, self.y_acc))

        # decay velocity
        self.x_vel = self.x_vel / 2 if abs(self.x_vel) > 1 else 0
        self.y_vel = self.y_vel / 2 if abs(self.y_vel) > 1 else 0

    # draws player onto screen
    def draw(self):
        camera.draw(self.gb)

p = Player()
things = []
# things.append(Thing(150, screen_height, 'red', 300, 40))

# constaants to determine speed of things / how fast things spawn
thing_up_speed = 3
thing_timer = 30*3*3
thing_c = thing_timer
nottoofast = 0

# player score
score = 0

def tick():
    # set background color
    camera.clear('grey') # make this get darker or something as you keep falling

    # spawn some things
    global thing_c, thing_timer, thing_up_speed, nottoofast
    thing_c += 1
    if thing_c >= thing_timer/thing_up_speed:
        gap_center = randint(200, screen_width - 200)
        gap_width = randint(p.gb.width + 30, p.gb.width + 200)
        
        # print('gap center: {}\tgap width: {}'.format(gap_center, gap_width))
        
        # make the left thing
        t_x = (gap_center - gap_width/2)/2
        t_w = (gap_center - gap_width/2)
        things.append(Thing(t_x, screen_height + 20, 'red', t_w, 40))

        # make the right thing
        t_x = (gap_center + gap_width/2 + screen_width)/2
        t_w = screen_width - (gap_center + gap_width/2)
        things.append(Thing(t_x, screen_height + 20, 'red', t_w, 40))

        thing_c = 0
        nottoofast += 1

        if thing_timer > 10*12:
            thing_timer -= 5
        # speed up spawning and MS
        if thing_up_speed <= 12 and nottoofast > 3:
            nottoofast = 0
            thing_up_speed += 1


    # update the things
    for t in things:
        if not t.is_off_screen():
            t.update()
            t.draw()
        else:
            things.remove(t)

    # draw score on after thihngs
    global score
    score += 1
    
    # take inputs and move player
    # important to do this after updating the things
    p.get_keys()
    p.draw()

    camera.display()

u.timer_loop(30, tick)
