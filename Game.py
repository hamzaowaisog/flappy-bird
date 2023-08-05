import pygame
from pygame.locals import *
import random
def main():

    pipes_list = ['sprites/pipe-red.png', 'sprites/pipe-green.png']
    pipe_surface = pygame.image.load(random.choice(pipes_list))
    pipe_list2 = []

    pygame.mixer.pre_init(frequency=44100, size=32, channels=1, buffer=512)

    pygame.init()
    gravity = 0.26
    bird_movement = 0
    game_on = True
    score = 0
    high_score = 0
    scoring_timer =100
    show_pipe = pygame.USEREVENT
    pygame.time.set_timer(show_pipe, 800)
    display = pygame.display.set_mode((285, 510))
    pygame.display.set_caption("Flappy Bird")
    speed = pygame.time.Clock()
    background_image = ['sprites/background-day.png','sprites/background-night.png']
    background = pygame.image.load(random.choice(background_image)).convert()
    base = pygame.image.load('sprites/base.png').convert()
    base_x_pos = 0
    pipe_height = [200, 300, 400]

    bird = pygame.image.load('sprites/bluebird-midflap.png').convert_alpha()
    bird_rect = bird.get_rect(center = (25, 255))

    font = pygame.font.Font('FontsFree-Net-EvilEmpire.ttf', 35)
    game_over_sur = pygame.image.load('sprites/gameover.png').convert_alpha()
    game_over_rect = game_over_sur.get_rect(center = (142, 255))

    flap_sound = pygame.mixer.Sound('audio/wing.wav')
    death_sound = pygame.mixer.Sound('audio/hit.wav')
    score_sound = pygame.mixer.Sound('audio/point.wav')
    die_sound = pygame.mixer.Sound('audio/die.wav')


    def base_movement():
        display.blit(base, (base_x_pos, 435))
        display.blit(base, (base_x_pos + 285, 435))

    def create_pipe():
        random_pipe_pos = random.choice(pipe_height)
        top_pipe = pipe_surface.get_rect(midtop = (288, random_pipe_pos))
        bottom_pipe = pipe_surface.get_rect(midbottom=(288, random_pipe_pos-150))
        return bottom_pipe, top_pipe

    def move_pipes(pipes):
        for pipe in pipes:
            pipe.centerx -= 5
        return pipes

    def show_pipes(pipes):
        for pipe in pipes:
            if pipe.bottom >= 510:
                display.blit(pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(pipe_surface, False, True)
                display.blit(flip_pipe, pipe)



    def collision(pipes):
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                death_sound.play()
                die_sound.play()
                return False
        if bird_rect.top <= -25 or bird_rect.bottom >= 435:
            return False
        return True

    def bird_rotation(bird):
        new_bird = pygame.transform.rotozoom(bird, bird_movement*5, 1)
        return new_bird

    def score_display(game):
        if game == 'game_on':
            score_surf = font.render(f'Score: {str(int(score))}', True, (255, 255, 255))
            score_rect = score_surf.get_rect(center = (142, 30))
            display.blit(score_surf, score_rect)
        elif game == 'game_over':
            score_surf = font.render(f'Score: {str(int(score))}', True, (255, 255, 255))
            score_rect = score_surf.get_rect(center=(142, 30))
            display.blit(score_surf, score_rect)

            high_surf = font.render(f'High-Score: {str(int(high_score))}', True, (255, 255, 255))
            high_rect = score_surf.get_rect(center=(120, 100))
            display.blit(high_surf, high_rect)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and game_on:
                if event.key == pygame.K_SPACE:
                    bird_movement =0
                    bird_movement -= 5
                    flap_sound.play()
            elif event.type == pygame.KEYDOWN and game_on == False:
                if event.key == pygame.K_SPACE:
                    pipe_list2.clear()
                    game_on = True
                    bird_rect.center = (25, 255)
                    bird_movement =0
                if random.choice(pipes_list) == pipes_list[0] or pipe_surface == pygame.image.load(pipes_list[0]):
                    pipe_surface = pygame.image.load(pipes_list[1])
                else:
                    pipe_surface = pygame.image.load(pipes_list[0])

            if event.type == show_pipe:
                pipe_list2.extend(create_pipe())



        speed.tick(65)
        display.blit(background, (0, 0))

        if game_on:
            bird_movement += gravity
            flappy_bird = bird_rotation(bird)
            bird_rect.centery += bird_movement
            display.blit(flappy_bird, bird_rect)
            game_on = collision(pipe_list2)
            pipe_list2 = move_pipes(pipe_list2)
            show_pipes(pipe_list2)
            score += 0.01
            score_display('game_on')
            scoring_timer -= 1
            if scoring_timer <= 0:
                score_sound.play()
                scoring_timer = 100
        else:
            score_display('game_over')
            if score > high_score:
                high_score = score
            score = 0
            display.blit(game_over_sur, game_over_rect)


        base_movement()
        base_x_pos -= 1
        pygame.display.update()

        if base_x_pos <= -285:
            base_x_pos = 0









if __name__ == "__main__":
    main()
