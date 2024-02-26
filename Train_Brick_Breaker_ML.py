import pygame
import random
import os
import neat
import pickle
from Utils import *

pygame.init()
w, h = 500, 500
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("AI BRICK BREAKER")
font = pygame.font.SysFont("comicsans", 30)
clock = pygame.time.Clock()

gen = 0
def fitness(genomes, config):
    global win, gen
    gen += 1
    nets = []
    agents = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        agents.append(AI_Paddle())
        ge.append(genome)

    for index in range(len(nets)):
        paddle = agents[index]
        running = True
        box_obs = [paddle]
        brick_y = 80
        def_brick_w = AI_Brick().width
        def_brick_h = AI_Brick().height
        boxIndex = 0
        for _ in range(5):
            brick_x = 0
            for _ in range((w // AI_Brick().width)):
                box_obs.append(AI_Brick(brick_x, brick_y, boxIndex))
                boxIndex += 1
                brick_x += def_brick_w
            brick_y += def_brick_h
        ball = Ball()
        dead_ball = 0
        penalty = 0  # time penalty for fitness function
        start_ticks = pygame.time.get_ticks()  # to prevent infinite loop, break after 200 seconds
        paddle_bonus = 0
        while running:
            clock.tick(1000)  # sets highest fps possible for fastest training
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                    break
            penalty += 0.0001  # time penalty of 1 point per 100 seconds
            paddle.currvel = 0
            keys = {'left': False, 'right': False}
            # input for NEAT will be the following + 1 or 0 for each brick that's unbroken/broken in order.
            inputList = [paddle.x, paddle.y, ball.x, ball.y, ball.xvel, ball.yvel]
            brokenList = [0] * boxIndex
            for box in box_obs[1:]:
                brokenList[box.index] = 1
            inputList.extend(brokenList)
            output = nets[index].activate(tuple(inputList))
            if output[0] > 0.5:
                keys['left'] = True
            if output[1] > 0.5:
                keys['right'] = True
            paddle.move(keys)
            dead_ball = ball.move(box_obs)
            score = 51 - len(box_obs)
            if score < 5 and paddle.y == ball.y + ball.radius and paddle.x - ball.radius/2 <= ball.x <= paddle.x + paddle.width + ball.radius/2:
                paddle_bonus += 0.8
            ge[index].fitness = score + paddle_bonus - penalty
            if dead_ball:
                ge[index].fitness -= abs(ball.x - paddle.x)/50
                if score == 1:
                    ge[index].fitness -= 5
                running = False

            win.fill((0, 0, 0))  # Change background color to black
            pygame.draw.rect(win, (255, 0, 0), (paddle.x, paddle.y, paddle.width, paddle.height))  # Change paddle color to red
            pygame.draw.circle(win, (0, 255, 0), (ball.x, ball.y), ball.radius)  # Change ball color to green
            for brick in box_obs[1:]:
                pygame.draw.rect(win, (0, 0, 255), (brick.x + 1, brick.y + 1, brick.width - 2, brick.height - 2))
            score_label = font.render("Score: " + str(score), 1, (255, 255, 255))
            win.blit(score_label, (10, 10))
            gen_label = font.render("Gen: " + str(gen) + " Species: " + str(index+1), 1, (255, 255, 255))
            win.blit(gen_label, (w - gen_label.get_width() - 10, 10))
            pygame.display.update()

            if score >= 49 and dead_ball:  # saves models that score 49 or beat the game
                pickle.dump(nets[index], open("perfect.pickle", "wb"))
                break
            elif score - penalty >= 46 and dead_ball:  # saves models that scored 47 or more
                pickle.dump(nets[index], open("best.pickle", "wb"))
                break
            elif score - penalty >= 40 and ge[index].fitness > 44 and dead_ball:  # saves models with a score over ~42
                pickle.dump(nets[index], open("good.pickle", "wb"))
                break

            if (pygame.time.get_ticks() - start_ticks)/1000 > 20:
                ge[index].fitness -= 8
                running = False
                print("Infinite loop occurred")
                break

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    winner = population.run(fitness, 300)

    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'NEAT_config.txt')
    run(config_path)
