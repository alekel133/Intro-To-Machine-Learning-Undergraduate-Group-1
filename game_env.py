import pygame
import random
from Utils import *

pygame.init()
w, h = 500, 500
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("Brick Breaker")
font = pygame.font.SysFont("comicsans", 30)
win_font = pygame.font.SysFont("comicsans", 50)
clock = pygame.time.Clock()
running = True
paddle = Paddle(h,w)
box_obs = [paddle]
brick_y = 80
def_brick_w = Brick().width
def_brick_h = Brick().height
for _ in range(5):
    brick_x = 0
    for _ in range((w//Brick().width)):
        box_obs.append(Brick(brick_x, brick_y))
        brick_x += def_brick_w
    brick_y += def_brick_h
ball = Ball()
dead_ball = 0
score, deaths = 0, 0

while running:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Check if mouse button is pressed
            if event.button == 1:  # Left mouse button
                if paddle.x <= event.pos[0] <= paddle.x + paddle.width and \
                   paddle.y <= event.pos[1] <= paddle.y + paddle.height:
                    paddle.start_drag()  # Start dragging the paddle
        elif event.type == pygame.MOUSEBUTTONUP:  # Check if mouse button is released
            if event.button == 1:  # Left mouse button
                paddle.stop_drag()  # Stop dragging the paddle

    if dead_ball:
        pygame.time.delay(1000)
    if len(box_obs) == 1:
        win_label = win_font.render("YOU WIN!", 1, (255, 255, 255))
        win.blit(win_label, ((w - win_label.get_width()) // 2, 200))
        pygame.display.update()
        pygame.time.delay(1000)
        break

    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    paddle.move(keys, mouse_pos)
    dead_ball = ball.move(box_obs)
    if dead_ball:
        del ball
        box_obs.remove(paddle)
        del paddle
        pygame.time.delay(1000)
        paddle = Paddle()
        box_obs.insert(0, paddle)
        ball = Ball()
        deaths += 1

    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255, 255, 255), (paddle.x, paddle.y, paddle.width, paddle.height))
    pygame.draw.circle(win, (255, 255, 255), (ball.x, ball.y), ball.radius)
    for brick in box_obs[1:]:
        pygame.draw.rect(win, (0, 0, 255), (brick.x+1, brick.y+1, brick.width-2, brick.height-2))
    score = 51 - len(box_obs)
    score_label = font.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (10, 10))
    death_label = font.render("Deaths: " + str(deaths), 1, (255, 255, 255))
    win.blit(death_label, (w - death_label.get_width() - 10, 10))
    pygame.display.update()

pygame.quit()
