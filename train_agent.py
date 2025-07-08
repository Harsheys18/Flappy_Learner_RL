import pygame, random, time
from dataclasses import dataclass

from flappy import *

BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()

@dataclass
class Args:
    # Game Flow
    run_name: str = "Flappy_learner"
    iterations: int = 10
    time_steps: int = 200
    total_time_steps: int = iterations*time_steps
    
    # For learning
    epochs: int = 10
    mini_batches: int = 4
    mini_batch_size: int = 10
    batches: int = time_steps/(mini_batch_size*mini_batches)
    
    # PPO Algorithm specific
    lr: float = 0.1

    # Other 
    save_agent: bool = False

def layer_init():
    
    pass
    
class Agent:
    def __init__(self):
        pass
    
    def get_action(self):
        pass
    
    def get_expected_reward(self):
        pass
    
    def send_flap_signal(self):
        pass

def ppo_train(args):
    
    for epoch in range(args.epochs):
        for batch in range(0,args.batches, args.minibatch_size):
            pass
        
        
    pass

def make_screen(screen):
    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)
    ground_group = pygame.sprite.Group()

    for i in range (2):
        ground = Ground(GROUND_WIDTH * i)
        ground_group.add(ground)
    
    pipe_group = pygame.sprite.Group()
    for i in range (2):
        pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
        
    clock = pygame.time.Clock()
    begin = True
    while begin:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    bird.bump()
                    pygame.mixer.music.load(wing)
                    pygame.mixer.music.play()
                    begin = False

        screen.blit(BACKGROUND, (0, 0))
        screen.blit(BEGIN_IMAGE, (120, 150))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(GROUND_WIDTH - 20)
            ground_group.add(new_ground)

        bird.begin()
        ground_group.update()
        bird_group.draw(screen)
        ground_group.draw(screen)
        pygame.display.update()
    
    return clock, bird, screen, ground_group, pipe_group, bird_group

if __name__ == "__main__":
    # Game window making
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Flappy Bird')
    
    clock, bird, screen, ground_group, pipe_group, bird_group = make_screen()

    args = Args()
    for iteration in range(1, args.iterations+1):
        # Initialise the storage
        steps = 0
        
        
        # Game loop
        while steps < args.time_steps:
            clock.tick(15)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE or event.key == K_UP:
                        bird.bump()
                        pygame.mixer.music.load(wing)
                        pygame.mixer.music.play()
                

            screen.blit(BACKGROUND, (0, 0))

            if is_off_screen(ground_group.sprites()[0]):
                ground_group.remove(ground_group.sprites()[0])
                new_ground = Ground(GROUND_WIDTH - 20)
                ground_group.add(new_ground)

            if is_off_screen(pipe_group.sprites()[0]):
                pipe_group.remove(pipe_group.sprites()[0])
                pipe_group.remove(pipe_group.sprites()[0])
                pipes = get_random_pipes(SCREEN_WIDTH * 2)
                pipe_group.add(pipes[0])
                pipe_group.add(pipes[1])

            bird_group.update()
            ground_group.update()
            pipe_group.update()

            bird_group.draw(screen)
            pipe_group.draw(screen)
            ground_group.draw(screen)

            pygame.display.update()

            if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
                    pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
                pygame.mixer.music.load(hit)
                pygame.mixer.music.play()
                time.sleep(1)
                break
            
        # Make screen to the start
        ppo_train()
        print(f"Iteration: {iteration} Completed!")
        clock, bird, screen, ground_group, pipe_group, bird_group = make_screen()
        
    
    # Save agent
    