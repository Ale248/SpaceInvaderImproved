import pygame
import os
import random
import math

# Center window when run
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Init
pygame.init()

ENEMY_X_SPEED = 7
PLAYER_X_SPEED = 9
BULLET_Y_SPEED = 15

# Game window
display_width = 800
display_height = 600
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

bullet_img = pygame.image.load('torpedo.png')
background = pygame.image.load('background.png')
player_img = pygame.image.load('player.png')
explosion_img = pygame.image.load('explosion.png')

pause = False

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
yellow = (207, 173, 23)
bright_yellow = (255, 208, 0)

# Fonts
# small_text = pygame.font.Font('freesansbold.ttf', 32)
small_font = pygame.font.Font("freesansbold.ttf", 20)
medium_font = pygame.font.Font('freesansbold.ttf', 32)
large_font = pygame.font.Font('freesansbold.ttf', 64)


# def show_score(x, y):
#     # For text, render then blit
#     score_text = small_font.render("Score: " + str(score), True, (255, 255, 255))
#     game_display.blit(score_text, (x, y))


# Return x coordinate that make the text centered
def get_x_center(surf):
    size = surf.get_size()
    x = (display_width / 2) - (size[0] / 2)
    return x


# Return y coordinate that make the text centered
def get_y_center(surf):
    size = surf.get_size()
    y = (display_width / 2) - (size[1] / 2)
    return y


def fire_bullet(x, y):
    # global bullet_state
    # bullet_state = "fire"
    game_display.blit(bullet_img, (x + 16, y + 10))
    return "fire"


def show_player(x, y):
    # blit = to draw
    game_display.blit(player_img, (x, y))


def show_enemy(x, y, i, enemy_img):
    # blit = to draw
    game_display.blit(enemy_img[i], (x, y))


# msg: What do you want the button to say on it.
# x: The x location of the top left coordinate of the button box.
# y: The y location of the top left coordinate of the button box.
# w: Button width.
# h: Button height.
# ic: Inactive color (when a mouse is not hovering).
# ac: Active color (when a mouse is hovering).
# action: Function
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if x + w > mouse_pos[0] > x and y + h > mouse_pos[1] > y:
        pygame.draw.rect(game_display, ac, (x, y, w, h))

        if mouse_click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(game_display, ic, (x, y, w, h))

    # textSurf, textRect = text_objects(msg, smallText)
    text_surface = small_font.render(msg, True, black)
    text_rect = text_surface.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    game_display.blit(text_surface, text_rect)


def is_collision(e_x, e_y, b_x, b_y):
    distance = math.sqrt((math.pow(e_x - b_x, 2)) + (math.pow(e_y - b_y, 2)))
    if distance < 27:
        return True
    else:
        return False


def show_explosion(x, y):
    game_display.blit(explosion_img, (x, y))
    game_display.blit(explosion_img, (x - 16, y - 16))
    game_display.blit(explosion_img, (x + 16, y + 16))
    game_display.blit(explosion_img, (x + 16, y - 16))
    game_display.blit(explosion_img, (x - 16, y + 16))


def show_score(score, high_score):
    # For text, render then blit
    if score > high_score:
        high_score = score
    score_text = medium_font.render("Score: " + str(score), True, white)
    high_score_text = medium_font.render("High Score: " + str(high_score), True, white)
    game_display.blit(high_score_text, (display_width - high_score_text.get_width(), 0))
    game_display.blit(score_text, (0, 0))


def get_high_score():
    # Default high score
    high_score = 0

    # Try to read the high score from a file
    try:
        high_score_file = open("high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
        print("The high score is", high_score)
    except IOError:
        # Error reading file, no high score
        print("There is no high score yet.")
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("I'm confused. Starting with no high score.")

    return high_score


def save_high_score(new_high_score):
    try:
        # Write the file to disk
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the high score.")


def game_exit():
    pygame.quit()
    quit()


def game_over():
    # over_text = large_font.render("GAME OVER", True, (255, 255, 255))
    # game_display.blit(over_text, (200, 250))

    # game_display.fill(black)
    pygame.mixer.music.load('game_over.mp3')
    pygame.mixer.music.play(-1)
    while True:
        game_display.blit(background, (0, 0))

        test_text = large_font.render("GAME OVER", True, white)
        game_display.blit(test_text, (get_x_center(test_text), 150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

        button("Retry", 330, 300, 140, 70, green, bright_green, game_loop)
        button("Exit", 330, 400, 140, 70, red, bright_red, game_exit)

        game_cursor()

        pygame.display.update()
        clock.tick(60)


def game_cursor():
    mouse_pos = pygame.mouse.get_pos()
    pygame.mouse.set_visible(False)
    player_img_rotated = pygame.transform.rotate(player_img, 45)
    game_display.blit(player_img_rotated, (mouse_pos[0] - 23, mouse_pos[1] - 23))


def game_pause():
    pygame.mixer.music.pause()
    while pause:
        game_display.blit(background, (0, 0))
        pause_text = large_font.render("PAUSED", True, white)
        game_display.blit(pause_text, (get_x_center(pause_text), 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_unpause()

        button("Resume", 330, 300, 140, 70, green, bright_green, game_unpause)
        button("Reset", 330, 400, 140, 70, yellow, bright_yellow, game_loop)
        button("Exit", 330, 500, 140, 70, red, bright_red, game_exit)

        game_cursor()

        pygame.display.update()
        clock.tick(60)


def game_unpause():
    global pause
    pause = False
    pygame.mixer.music.unpause()


def game_intro():
    intro = True
    high_score = get_high_score()
    while intro:
        game_display.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        title_text = large_font.render("SPACE INVADER (?)", True, white)
        game_display.blit(title_text, (get_x_center(title_text), 150))

        high_text = medium_font.render("High Score: " + str(high_score), True, white)
        game_display.blit(high_text, (get_x_center(high_text), 230))

        button("Start", 330, 300, 140, 70, green, bright_green, game_loop)
        button("Exit", 330, 400, 140, 70, red, bright_red, game_exit)

        game_cursor()

        pygame.display.update()
        clock.tick(60)


def game_loop():
    global pause
    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    high_score = get_high_score()

    player_x = 368
    player_y = 480
    player_x_change = 0

    # Score
    score = 0

    # Enemy (multiple)
    enemy_img = []
    enemy_x = []
    enemy_y = []
    enemy_x_change = []
    enemy_y_change = []
    num_enemies = 5
    for enemy_num in range(num_enemies):
        enemy_img.append(pygame.image.load('enemy.png'))
        enemy_x.append(random.randint(0, 735))
        enemy_y.append(random.randint(50, 150))
        enemy_x_change.append(ENEMY_X_SPEED)
        enemy_y_change.append(40)

    # Bullet
    # Ready: cant see bullet
    # Fire: bullet moving
    bullet_x = 0
    bullet_y = 480
    # bullet_x_change = 0
    bullet_y_change = BULLET_Y_SPEED
    bullet_state = "ready"

    # running = True
    while True:
        game_display.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > high_score:
                    save_high_score(score)
                pygame.quit()
                quit()

            # Keystroke checks
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -PLAYER_X_SPEED
                if event.key == pygame.K_RIGHT:
                    player_x_change = PLAYER_X_SPEED
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        laser_sound = pygame.mixer.Sound('laser.wav')
                        laser_sound.set_volume(0.25)
                        laser_sound.play()
                        bullet_x = player_x
                        bullet_state = fire_bullet(bullet_x, bullet_y)
                if event.key == pygame.K_p:
                    print("pressed")
                    pause = True
                    game_pause()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

        # Boundary checks
        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        # Enemy movement
        for i in range(num_enemies):
            # Game Over
            if enemy_y[i] > 430:
                for j in range(num_enemies):
                    # "remove" the enemy
                    enemy_y[j] = 2000
                if score > high_score:
                    save_high_score(score)
                blast_sound = pygame.mixer.Sound('blast.wav')
                blast_sound.set_volume(0.8)
                blast_sound.play()
                game_over()
                break
            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0:
                enemy_x_change[i] = ENEMY_X_SPEED
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= 736:
                enemy_x_change[i] = -ENEMY_X_SPEED
                enemy_y[i] += enemy_y_change[i]

            # Collision check
            collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if collision:
                blast_sound = pygame.mixer.Sound('blast.wav')
                blast_sound.set_volume(0.8)
                blast_sound.play()

                # Show explosion
                show_explosion(enemy_x[i], enemy_y[i])
                # game_display.fill(white)

                bullet_y = 480
                bullet_state = "ready"
                score += 1
                # Enemy respawn
                enemy_x[i] = random.randint(0, 735)
                enemy_y[i] = random.randint(50, 150)

            show_enemy(enemy_x[i], enemy_y[i], i, enemy_img)

        # Bullet movement
        if bullet_y <= -32:
            bullet_y = 480
            bullet_state = "ready"
        if bullet_state is "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        show_player(player_x, player_y)

        show_score(score, high_score)

        pygame.display.update()
        clock.tick(60)


# Run the game
game_intro()
game_loop()
