# AI-Plays-Brick-Breaker

This project utilizes neural networks with NEAT to train and excel at the classic Atari game 'Breakout', also known as Brick Breaker.

**Note:** Due to randomness in the starting velocity and direction of the ball, neural networks may only optimize a subset of possible options. Consequently, even the `Test_best_AI.py` script may perform well only 50% of the time, despite leveraging multiple neural networks. Achieving a perfect AI might require training for more generations (default is at 300) after removing the fitness threshold from `NEAT_config.txt`. Alternatively, creating neural networks for each random option of the ball and selecting the best of each could be explored. However, note that this may entail several hours of training (approximately 100 generations ~ 1 hour) and has not been implemented yet.

### Requirements:
- pygame
- neat-python (ensure you install neat-python and not just neat)

### Instructions for Use:
- To play the game manually, execute `game_env.py`.
- To modify the fitness function and/or retrain the neural network, run `Train_Brick_Breaker_AI.py`.
- Use `Test_best_AI.py` to run the pickled models.
- Adjust the configuration of the NEAT neural networks by modifying parameters in `NEAT_config.txt`.
- The winning game, as per my fitness function, is available in the `.mp4` video.
- `bestGenome.txt` contains details of the winning neural network, as reported by NEAT's stat reporter. However, it cannot be executed directly. Utilize it to examine the specifics of the winning neural network.