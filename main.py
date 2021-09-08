import pygame
import random
import math
import sys


from pygame import mixer
from pygame.constants import KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, QUIT

pygame.init()

pygame.display.set_caption("Space Invaders")

screen = pygame.display.set_mode((800, 600))

icon = pygame.image.load("bin/icon.png")
pygame.display.set_icon(icon)

# background
backgroundImg = pygame.image.load("bin/background.png")
mixer.music.load("bin/background.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

header_font = pygame.font.Font(
    "bin/LuckiestGuy.ttf",
    64,
)
sub_header_font = pygame.font.Font(
    "bin/LuckiestGuy.ttf",
    16,
)
btn_font = pygame.font.Font(
    "bin/LuckiestGuy.ttf",
    32,
)
opt_font = pygame.font.Font(
    "bin/LuckiestGuy.ttf",
    36,
)
opt_font_1 = pygame.font.Font(
    "bin/LuckiestGuy.ttf",
    28,
)

bullet_Sound = mixer.Sound(
    "bin/laser.wav"
)

hit_Sound = mixer.Sound(
    "bin/explosion.mp3"
)


def esc():
    esc_text = opt_font_1.render("ESC = Back", True, (242, 242, 242))
    screen.blit(esc_text, (625, 550))


def ver():
    ver_text = sub_header_font.render("V0.8 - ALPHA (EARLY ACCESS)", True, (242, 242, 242))
    screen.blit(ver_text, (575, 10))


logo = pygame.image.load(
    "bin/logo.png"
)
logo = pygame.transform.scale(logo, (350, 125))


def menu():
    while True:

        # screen.fill((0, 0, 0))  # background fill color

        screen.blit(backgroundImg, (0, 0))  # Background Image

        screen.blit(logo, (210, 30))

        # def menu_text():
        #     menu_text = header_font.render("SPACE INVADERS", True, (242, 242, 242))
        #     screen.blit(menu_text, (200, 50))

        def sub_menu_text():
            sub_menu_text = opt_font_1.render("Remastered", True, (242, 242, 242))
            screen.blit(sub_menu_text, (370, 160))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(260, 200, 250, 50)
        button_2 = pygame.Rect(260, 300, 250, 50)
        button_3 = pygame.Rect(260, 400, 250, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        if button_3.collidepoint((mx, my)):
            if click:
                credits()

        pygame.draw.rect(screen, (99, 212, 0), button_1)
        pygame.draw.rect(screen, (255, 50, 134), button_2)
        pygame.draw.rect(screen, (255, 50, 134), button_3)

        def menu_btn_1():
            btn_1_text = btn_font.render("PLAY", True, (242, 242, 242))
            screen.blit(btn_1_text, (340, 210))

        def menu_btn_2():
            btn_2_text = btn_font.render("Options", True, (242, 242, 242))
            screen.blit(btn_2_text, (315, 310))

        def menu_btn_3():
            btn_3_text = btn_font.render("Credits", True, (242, 242, 242))
            screen.blit(btn_3_text, (325, 410))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        ver()
        # menu_text()
        sub_menu_text()
        menu_btn_1()
        menu_btn_2()
        menu_btn_3()
        pygame.display.update()


def game():
    # player
    playerImg = pygame.image.load(
        "bin/player.png"
    )
    playerX = 370
    playerY = 480
    playerX_change = 0

    # enemy
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6

    for i in range(num_of_enemies):
        enemyImg.append(
            pygame.image.load(
                "bin/enemy.png"
            )
        )
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(2)
        enemyY_change.append(40)

    # bullet
    bulletImg = pygame.image.load(
        "bin/bullet.png"
    )
    global bullet_state
    bullet_state = "ready"
    bulletX = 0
    bulletY = 480
    bulletX_change = 2
    bulletY_change = 15
    # "Ready" state means you cant see the bullet on the screen
    # "Fire" state means the bullet is currently moving

    # score
    score_value = 0

    font = pygame.font.Font(
        "bin/LuckiestGuy.ttf",
        32,
    )
    hi_font = pygame.font.Font(
        "bin/LuckiestGuy.ttf",
        16,
    )

    textX = 10
    textY = 10

    # Game Over Text
    over_font = pygame.font.Font(
        "bin/LuckiestGuy.ttf",
        64,
    )

    def show_score(x, y):
        score = font.render("Score :" + str(score_value), True, (242, 242, 242))
        screen.blit(score, (x, y))

    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (242, 242, 242))
        screen.blit(over_text, (250, 250))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(
            (math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2))
        )
        if distance < 27:
            return True
        else:
            return False

    # GAMELOOP
    running = True
    while running:

        screen.blit(backgroundImg, (0, 0))  # Background Image

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            # if keystroke is pressed check whether its righ tor left
            if event.type == pygame.KEYDOWN:
                # print("Keystroke has been pressed")
                if event.key == pygame.K_LEFT:
                    # print("Left arrow is pressed ")
                    playerX_change = -4
                if event.key == pygame.K_RIGHT:
                    # print("Right arrow is pressed ")
                    playerX_change = 4
                if event.key == pygame.K_SPACE:
                    # print("Space bar is pressed ")
                    if bullet_state == "ready":
                        bulletX = playerX
                        bullet_Sound.set_volume(0.8)
                        bullet_Sound.play()
                        fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                    # print("Keystroke has been released")

        with open(
            "bin/hi-score.txt",
            "r",
        ) as f:
            hi_score = f.read()

        def high_score(x, y):
            high_score = hi_font.render(
                "Hi-Score :" + str(hi_score), True, (255, 222, 0)
            )
            screen.blit(high_score, (x, y))

        # setting screen boundries for player
        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        if score_value > int(hi_score):
            hi_score = score_value
            new_hiscore_text()

        def new_hiscore_text():
            option_text = opt_font.render("NEW HI-SCORE!", True, (255, 222, 0))
            screen.blit(option_text, (250, 50))

        # Game Over
        for i in range(num_of_enemies):
            if enemyY[i] > 400:
                with open(
                    "bin/hi-score.txt",
                    "w",
                ) as f:
                    f.write(str(hi_score))
                for j in range(num_of_enemies):
                    enemyY[j] = 2000

                game_over_text()
                break

            # enemy movement
            enemyX[i] += enemyX_change[i]

            if enemyX[i] <= 0:
                enemyX_change[i] = 2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -2
                enemyY[i] += enemyY_change[i]

            # collison
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                hit_Sound.play()
                hit_Sound.set_volume(0.3)
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

            if score_value >= 25:
                if enemyX[i] <= 0:
                    enemyX_change[i] = 2.5
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -2.5
                    enemyY[i] += enemyY_change[i]

            enemy(enemyX[i], enemyY[i], i)

        # bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
        ver()
        esc()
        player(playerX, playerY)
        show_score(textX, textY)
        high_score(textX, textY + 30)
        pygame.display.update()


def options():
    running = True
    while running:
        screen.fill((0, 0, 0))

        screen.blit(backgroundImg, (0, 0))  # Background Image

        def options_text():
            option_text = header_font.render("OPTIONS", True, (242, 242, 242))
            screen.blit(option_text, (250, 50))

        def music_text():
            option_text = opt_font.render("Music", True, (242, 242, 242))
            screen.blit(option_text, (250, 210))

        def reset_score_text():
            option_text = opt_font.render("Hi-Score", True, (242, 242, 242))
            screen.blit(option_text, (250, 290))

        def on_text():
            option_text = sub_header_font.render("ON", True, (242, 242, 242))
            screen.blit(option_text, (435, 180))

        def off_text():
            option_text = sub_header_font.render("OFF", True, (242, 242, 242))
            screen.blit(option_text, (510, 180))

        def reset_text():
            option_text = opt_font_1.render("RESET", True, (242, 242, 242))
            screen.blit(option_text, (450, 290))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(425, 200, 50, 50)
        button_2 = pygame.Rect(500, 200, 50, 50)

        button_3 = pygame.Rect(425, 275, 125, 50)

        def draw_rect_alpha(surface, color, rect):
            shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
            surface.blit(shape_surf, rect)

        draw_rect_alpha(screen, (0, 0, 255, 127), (0, 40, 800, 70))

        if button_1.collidepoint((mx, my)):
            if click:
                if mixer.music.set_volume(0.5):
                    mixer.music.set_volume(0)

        if button_2.collidepoint((mx, my)):
            if click:
                if mixer.music.set_volume(0):
                    mixer.music.set_volume(0.5)

        if button_3.collidepoint((mx, my)):
            if click:
                with open(
                    "bin/hi-score.txt",
                    "w",
                ) as f:
                    f.write(str(0))

        pygame.draw.rect(screen, (165, 50, 255), button_1)
        pygame.draw.rect(screen, (255, 50, 134), button_2)

        pygame.draw.rect(screen, (255, 50, 134), button_3)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        ver()
        esc()
        options_text()
        music_text()
        reset_score_text()
        reset_text()
        on_text()
        off_text()
        pygame.display.update()


insta = pygame.image.load(
    "bin/insta.png"
)
insta = pygame.transform.scale(insta, (72, 72))


def credits():
    running = True
    while running:
        screen.fill((0, 0, 0))

        screen.blit(backgroundImg, (0, 0))  # Background Image

        def credit():
            btn_3_text = btn_font.render("keshaav.exe", True, (242, 242, 242))
            screen.blit(btn_3_text, (350, 275))

        screen.blit(insta, (250, 250))

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        ver()
        esc()
        credit()
        pygame.display.update()


menu()
