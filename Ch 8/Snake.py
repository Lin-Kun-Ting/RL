import random
import pygame
class SnakeGame():
    def __init__(self, height = 5, width = 5, seed = 1115):
        random.seed(seed)
        self.height = height
        self.width = width
        self.emptyGrid = [(x, y) for x in range(height) for y in range(width)]
        self.snake = [random.choice(self.emptyGrid)]
        self.emptyGrid.remove(self.snake[0])
        self.food = random.choice(self.emptyGrid)
        self.eaten = 0
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.steps = 0
        self.terminate = False
    def takeAction(self, action):
        self.prevAction = action
        x, y = self.snake[0]
        direction = self.directions[action]
        dx, dy = direction
        nx, ny = x + dx, y + dy
        if (nx, ny) == self.food:
            self.steps = 0
            self.emptyGrid.remove(self.food)
            self.snake.insert(0, self.food)
            if len(self.emptyGrid) > 0:
                self.food = random.choice(self.emptyGrid)
            else:
                self.food = None
                self.terminate = True
            self.eaten += 1
            return 100
        elif (nx, ny) not in self.emptyGrid:
            self.terminate = True
            return -1000
        else:
            self.steps += 1
            self.snake.insert(0, (nx, ny))
            self.emptyGrid.remove((nx, ny))
            self.emptyGrid.append(self.snake.pop())
            return -abs(nx - self.food[0]) - abs(ny - self.food[1])
    def decideAction(self, Q, state, epsilon):
        if not Q.get(state):
            Q[state] = dict()
            for action in range(4):
                Q[state][action] = 0
        sample = random.random()
        if sample < epsilon:
            # random
            return random.choice([num for num in range(4)])
        else:
            # greedy
            maxQ = -1e6
            for action in range(4):
                if Q[state][action] > maxQ:
                    maxQ = Q[state][action]
                    optimalAction = action
            return optimalAction
agent = SnakeGame()
while not agent.terminate:
    pygame.init()
    
    CELL_SIZE = 20
    screen = pygame.display.set_mode((agent.width * CELL_SIZE, agent.height * CELL_SIZE))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    
    while not agent.terminate:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                agent.terminate = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    agent.takeAction(0)
                if event.key == pygame.K_DOWN:
                    agent.takeAction(1)
                if event.key == pygame.K_LEFT:
                    agent.takeAction(2)
                if event.key == pygame.K_UP:
                    agent.takeAction(3)
        
        screen.fill((255, 255, 255))
        
        # Draw snake
        for i, segment in enumerate(agent.snake):
            pygame.draw.rect(screen, (0, 255 - i * 8, 0), (segment[1] * CELL_SIZE, segment[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw food
        pygame.draw.rect(screen, (255, 0, 0), (agent.food[1] * CELL_SIZE, agent.food[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.display.flip()
        clock.tick(10)
    
    pygame.quit()

T = 1500
epsilon = 0.1
alpha = 0.5
Q = {}
for t in range(T + 1):
    agent = SnakeGame()
    currState = tuple(agent.snake), agent.food
    while not agent.terminate:
        if t % 100 == 0:
            pygame.init()
    
            CELL_SIZE = 20
            screen = pygame.display.set_mode((agent.width * CELL_SIZE, agent.height * CELL_SIZE))
            pygame.display.set_caption("Snake Game")
            clock = pygame.time.Clock()
            
            while not agent.terminate:
                currAction = agent.decideAction(Q, currState, 1 / (t + 1))
                reward = agent.takeAction(currAction)
                nextState = tuple(agent.snake), agent.food
                optimalAction = agent.decideAction(Q, nextState, -1)
                Q[currState][currAction] = Q[currState][currAction] + alpha * (reward + Q[nextState][optimalAction] - Q[currState][currAction])
                currState = nextState
                
                screen.fill((255, 255, 255))
                
                # Draw snake
                for i, segment in enumerate(agent.snake):
                    pygame.draw.rect(screen, (0, 255 - i * 8, 0), (segment[1] * CELL_SIZE, segment[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                
                # Draw food
                if agent.food != None:
                    pygame.draw.rect(screen, (255, 0, 0), (agent.food[1] * CELL_SIZE, agent.food[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                
                pygame.display.flip()
                clock.tick(10)
            print(f"Score = {agent.eaten}")
            pygame.quit()
        else:
            currAction = agent.decideAction(Q, currState, epsilon / (t + 1))
            reward = agent.takeAction(currAction)
            nextState = tuple(agent.snake), agent.food
            optimalAction = agent.decideAction(Q, nextState, -1)
            Q[currState][currAction] = Q[currState][currAction] + alpha * (reward + Q[nextState][optimalAction] - Q[currState][currAction])
            currState = nextState