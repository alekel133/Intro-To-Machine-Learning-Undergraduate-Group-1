import pygame
import random

class AI_Paddle:
    def __init__(self, h = 500, w = 500):
        self.width = 100  # Increase paddle width
        self.height = 20
        self.x = (w - self.width) // 2
        self.y = h - 10 - self.height
        self.w = w
        self.h = h
        self.vel = 5
        self.currvel = 0  # for applying spin to ball
        self.breakable = False

    def move(self, keys):
        if keys['left'] and self.x > 0:
            self.x -= self.vel
            self.currvel = -2
            if self.x < 0:
                self.x = 0
                self.currvel = 0
        if keys['right'] and self.x < self.w - self.width:
            self.x += self.vel
            self.currvel = 2
            if self.x > self.w - self.width:
                self.x = self.w - self.width
                self.currvel = 0


class Paddle:
    def __init__(self, h = 500, w = 500):
        self.width = 80
        self.height = 20
        self.w = w
        self.h = h
        self.x = (w - self.width) // 2
        self.y = h - 10 - self.height
        self.vel = 5
        self.currvel = 0  # for applying spin to ball
        self.breakable = False
        self.dragging = False  # flag to indicate if paddle is being dragged

    def move(self, keys, mouse_pos):
        if self.dragging:  # if dragging, update paddle position based on mouse position
            self.x = mouse_pos[0] - self.width // 2
            if self.x < 0:
                self.x = 0
            elif self.x > self.w - self.width:
                self.x = self.w - self.width
        else:  # if not dragging, move paddle using arrow keys
            if keys[pygame.K_LEFT] and self.x > 0:
                self.x -= self.vel
                self.currvel = -2
                if self.x < 0:
                    self.x = 0
                    self.currvel = 0
            if keys[pygame.K_RIGHT] and self.x < self.w - self.width:
                self.x += self.vel
                self.currvel = 2
                if self.x > self.w - self.width:
                    self.x = self.w - self.width
                    self.currvel = 0

    def start_drag(self):
        self.dragging = True

    def stop_drag(self):
        self.dragging = False

class AI_Brick:
    def __init__(self, x=0, y=0, boxIndex=0):
        self.width = 50
        self.height = 20
        self.x = x
        self.y = y
        self.currvel = 0  # only to avoid errors in collision detection
        self.breakable = True
        self.index = boxIndex

class Brick:
    def __init__(self, x=0, y=0):
        self.width = 50
        self.height = 20
        self.x = x
        self.y = y
        self.currvel = 0  # only to avoid errors in collision detection
        self.breakable = True

class Ball:
    def __init__(self, h = 500, w = 500):
        self.radius = 8
        self.x = w // 2
        self.y = h - 150
        self.h = h
        self. w = w
        self.xvel = random.randrange(-5, 6, 2)
        self.yvel = -5
        self.softcap = 7

    def move(self, box_obs):
        self.x += self.xvel
        self.y += self.yvel
        # make sure you actually collide for a single frame before changing direction
        if self.x < self.radius:
            self.x = self.radius
            self.xvel = -self.xvel
        if self.x > self.w - self.radius:
            self.x = self.w - self.radius
            self.xvel = -self.xvel
        if self.y < self.radius:
            self.y = self.radius
            self.yvel = -self.yvel

        x_cooldown, y_cooldown = 0, 0  # to prevent multiple collisions in a single axis in a single frame
        for box in box_obs:
            if y_cooldown == 1 and x_cooldown == 1:
                break  # exits early to save computation
            #collision from above
            if y_cooldown == 0 and 0 < box.y - self.y <= self.radius and box.x - self.radius/2 <= self.x <= box.x + box.width + self.radius/2:
                self.y = box.y - self.radius
                self.yvel = -self.yvel
                self.xvel += box.currvel
                if self.xvel > 0 and self.xvel > self.softcap:
                    self.xvel = self.softcap
                elif self.xvel < 0 and self.xvel < -self.softcap:
                    self.xvel = -self.softcap
                y_cooldown = 1  # so that it doesn't register multiple collisions in the same frame
                if box.breakable:
                    box_obs.pop(box_obs.index(box))
            #collision from below - only for bricks, not paddle, so no currvel
            elif y_cooldown == 0 and 0 < self.y - box.y - box.height <= self.radius and box.x - self.radius/2 <= self.x <= box.x + box.width + self.radius/2:
                #self.x -= int((self.xvel/abs(self.xvel))*(self.xvel/self.yvel)*(self.radius - self.y + box.y + box.height))
                self.y = box.y + box.height + self.radius
                self.yvel = -self.yvel
                y_cooldown = 1
                if box.breakable:
                    box_obs.pop(box_obs.index(box))
            #collision from left - not adding currvel for same reason
            elif x_cooldown == 0 and 0 < box.x - self.x <= self.radius and box.y - self.radius <= self.y <= box.y + box.height + self.radius:
                self.x = box.x - self.radius
                self.xvel = -self.xvel
                x_cooldown = 1
                if box.breakable:
                    box_obs.pop(box_obs.index(box))
            #collision from right - same as above
            elif x_cooldown == 0 and 0 < self.x - box.x - box.width <= self.radius and box.y - self.radius <= self.y <= box.y + box.height + self.radius:
                self.x = box.x + box.width + self.radius
                self.xvel = -self.xvel
                x_cooldown = 1
                if box.breakable:
                    box_obs.pop(box_obs.index(box))

        if self.y > self.h - 5:  # kill ball
            return 1
        return 0
