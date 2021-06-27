import pygame, sys, random, time


def add_moving_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def add_subject():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = random_pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = random_pipe_surface.get_rect(midbottom=(700, random_pipe_pos - random_pipe_pos))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > 50]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(random_pipe_surface, pipe)

def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if student_rect.colliderect(pipe):
            pygame.mixer.Sound('music/sfx_die.wav').play().get_busy()
            pygame.mixer.Sound('music/oblaneone.wav').play()
            can_score = True
            return False

    if student_rect.top <= -100 or student_rect.bottom >= 900:
        can_score = True
        return False

    return True


def move_student(student):
    new_student = pygame.transform.rotozoom(student, -student_movement * 3, 1)
    return new_student


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Zaliczonych przedmiotow: {int(score)}', True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'Najlepszy semestr: ', True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(288, 750))
        screen.blit(high_score_surface, high_score_rect)

        high_score_surface = game_font.render(f'{int(high_score)} \n zaliczonych egzaminow', True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)

        high_score_surface = game_font.render(f'2 termin -> Spacja', True,
                                              (255, 255, 230))
        high_score_rect = high_score_surface.get_rect(center=(288, 650))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True


pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

gravity = 0.25
student_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True
bg_surface = pygame.image.load('assets/z20662253Q.jpg').convert()

pygame.mixer.init()
pygame.mixer.music.load("music/dlaczego.mp3")
pygame.mixer.music.play(-1, 0.0)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

boy = pygame.transform.scale2x(pygame.image.load('assets/Webp.net-resizeimage.png').convert_alpha())
student_index = 0
student_surface = boy
student_rect = student_surface.get_rect(center=(100, 512))

STUDENTMOVE = pygame.USEREVENT + 1
pygame.time.set_timer(STUDENTMOVE, 200)

random_pipe_surface = random.choice([pygame.image.load('assets/python.png'), pygame.image.load('assets/python.png'),
                                     pygame.image.load('assets/matematyka.png'), pygame.image.load('assets/fizyka.png'),
                                     pygame.image.load('assets/algebra.png')])

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 500, 600, 700]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/cooltext387625819875825.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

victory = pygame.image.load('assets/victory.png').convert_alpha()
victory_rect = game_over_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound('music/sfx_wing.wav')
score_sound = pygame.mixer.Sound('music/sfx_point.wav')
score_sound_countdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                student_movement = 0
                student_movement -= 12
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                student_rect.center = (100, 512)
                student_movement = 0
                score = 0
            if event.key == pygame.K_SPACE and score == 5:
                pygame.mixer.music.stop()
                pygame.mixer.init(48000, -16, 1, 1024)
                pygame.mixer.music.load("music/victory.mp3")
                pygame.mixer.music.play(-1, 0.0)
                game_active = False

        if event.type == SPAWNPIPE:
            random_pipe_surface = random.choice(
                [pygame.image.load('assets/python.png'), pygame.image.load('assets/python.png'),
                 pygame.image.load('assets/matematyka.png'),
                 pygame.image.load('assets/fizyka.png'),
                 pygame.image.load('assets/algebra.png')])
            pipe_list.extend(add_subject())

    screen.blit(bg_surface, (0, 0))
    if game_active:
        student_movement += gravity
        moved_student = move_student(student_surface)
        student_rect.centery += student_movement
        screen.blit(moved_student, student_rect)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        pipe_score_check()
        score_display('main_game')

    elif game_active is False and score == 5:
        screen.blit(victory, victory_rect)
        high_score = update_score(score, high_score)

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    floor_x_pos -= 1
    add_moving_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
