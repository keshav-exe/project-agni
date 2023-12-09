import random
import math
import sys
import time
import pygame

from pygame import mixer
from pygame.constants import KEYDOWN, K_ESCAPE, K_KP1, MOUSEBUTTONDOWN, NUMEVENTS, QUIT, K_e

pygame.init()

pygame.display.set_caption("Project - Agni")

screen = pygame.display.set_mode((1080, 720))

icon = pygame.image.load("bin/icon.png")
pygame.display.set_icon(icon)

# background
backgroundImg = pygame.image.load("bin/background.png")
menuBackgroundImg = pygame.image.load("bin/menu-background.png")
mixer.music.load("bin/background.mp3")
mixer.music.set_volume(0.25)
mixer.music.play(-1)

header_font = pygame.font.Font(
    "bin/Inconsolata.ttf",
    64,
)
header_font1 = pygame.font.Font(
    "bin/Inconsolata.ttf",
    42,
)
sub_header_font = pygame.font.Font(
    "bin/Inconsolata.ttf",
    16,
)
btn_font = pygame.font.Font(
    "bin/Inconsolata.ttf",
    32,
)
opt_font = pygame.font.Font(
    "bin/Inconsolata.ttf",
    36,
)
opt_font_1 = pygame.font.Font(
    "bin/Inconsolata.ttf",
    28,
)

bullet_Sound = mixer.Sound("bin/bullet.mp3")
upgrade_Sound = mixer.Sound("bin/upgrade.mp3")

def ver():
    ver_text = sub_header_font.render("1.0.1 - Final", True, (31, 31, 31))
    screen.blit(ver_text, (950, 10))


logo = pygame.image.load("bin/logo.png")
logo = pygame.transform.scale(logo, (350, 125))

click = False


def menu():
    while True:

        screen.blit(menuBackgroundImg, (0, 0)) 

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(120, 200, 250, 100)
        button_2 = pygame.Rect(120, 350, 250, 100)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()

        pygame.draw.rect(screen, (99, 212, 0), button_1, 0, 24)
        pygame.draw.rect(screen, (231, 231, 231), button_2, 0, 24)

        def menu_btn_1():
            btn_1_text = btn_font.render("New Game", True, (242, 242, 242))
            screen.blit(btn_1_text, (180, 230))

        def menu_btn_2():
            btn_2_text = btn_font.render("Settings", True, (31, 31, 31))
            screen.blit(btn_2_text, (180, 380))

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
        menu_btn_1()
        menu_btn_2()
        pygame.display.update()
click = False

n =10

def game():
    # player
    playerImg = pygame.image.load("bin/player.png")
    playerX = 540
    playerY = 630
    playerX_change = 0

    # enemy
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load("bin/enemy.png"))
        enemyX.append(random.randint(120, 900))
        enemyY.append(random.randint(-50, 150))
        enemyX_change.append(4)
        enemyY_change.append(42)

    # obs
    bombImg = []
    bombX = []
    bombY = []
    bombX_change = []
    bombY_change = []
    num_of_bombs = 6

    for i in range(num_of_bombs):
        bombImg.append(pygame.image.load("bin/e_bomb.png"))
        bombX.append(random.randint(120, 900))
        bombY.append(random.randint(-50, 0))
        bombX_change.append(10)
        bombY_change.append(6)

    # bullet
    global bullet_state
    bulletImg = pygame.image.load("bin/p_bullet.png")
    bullet_state = "ready"
    bulletX = 0
    bulletY = 600
    bulletX_change = 4
    bulletY_change = 30
    # "Ready" state means you cant see the bullet on the screen
    # "Fire" state means the bullet is currently moving

    # score
    score_value = 0

    # points
    pts_value = 0

    font = pygame.font.Font(
        "bin/Inconsolata.ttf",
        32,
    )
    hi_font = pygame.font.Font(
        "bin/Inconsolata.ttf",
        16,
    )

    textX = 10
    textY = 10

    # Game Over Text
    over_font = pygame.font.Font(
        "bin/Inconsolata.ttf",
        64,
    )

    def show_score(x, y):
        score = font.render("Score :" + str(score_value), True, (242, 242, 242))
        screen.blit(score, (x, y))

    # economy system
    def show_pts(x, y):
        pts = font.render("Points :" + str(pts_value), True, (242, 242, 242))
        screen.blit(pts, (x, y))

    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (242, 242, 242))
        screen.blit(over_text, (400, 540))

    def upgrade_text():
        upgrade_text = opt_font_1.render("Semi-Auto Mod - 50 pts", True, (242, 242, 0))
        upgrade_text1 = sub_header_font.render("Z to purchase", True, (242, 242, 0))
        screen.blit(upgrade_text, (700, 670))
        screen.blit(upgrade_text1, (700, 700))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    def bomb(x, y, i):
        screen.blit(bombImg[i], (x, y))

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 36, y + -24))

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(
            (math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2))
        )
        if distance < 36:
            return True
        else:
            return False

    def isCollision2(bombX, bombY, playerX, playerY):
        distance = math.sqrt(
            (math.pow(bombX - playerX, 2)) + (math.pow(bombY - playerY, 2))
        )
        if distance < 36:   
            return True
        else:
            return False
        
    clock = pygame.time.Clock()

    num = 10
    # GAMELOOP
    running = True
    while running:

        screen.blit(backgroundImg, (0, 0))  # Background Image

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            timeout = 5
            timeout_start = time.time()


            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == KEYDOWN:
                if event.key == pygame.K_z:
                    if bulletY_change < 60:
                        if(num <= 10):
                            if pts_value >= 50:
                                num +=10
                                pts_value -= 50
                                bulletY_change = 60
                                upgrade_Sound.set_volume(1.5)
                                upgrade_Sound.play()
                                if bulletY_change == 60:
                                    def upgrade_text():
                                        upgrade_text = opt_font_1.render("Semi Auto Mod - Equipped!", True, (242, 242, 0))
                                        screen.blit(upgrade_text, (600, 900))
                            elif pts_value < 50:
                                pass

                            
            
            # if keystroke is pressed check whether its righ tor left
            if event.type == pygame.KEYDOWN:
                # print("Keystroke has been pressed")
                if event.key == pygame.K_LEFT:
                    # print("Left arrow is pressed ")
                    playerX_change = -8
                if event.key == pygame.K_RIGHT:
                    # print("Right arrow is pressed ")
                    playerX_change = 8
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        bullet_Sound.set_volume(0.5)
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

        if playerX <= 120:
            playerX = 120
        elif playerX >= 900:
            playerX = 900

        if score_value > int(hi_score):
            hi_score = score_value
            new_hiscore_text()

        def new_hiscore_text():
            option_text = opt_font.render("NEW HI-SCORE!", True, (255, 222, 0))
            screen.blit(option_text, (250, 50))

        # Game Over
        for i in range(num_of_enemies):
            if enemyY[i] > 500:
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

            if enemyX[i] <= 120:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 900:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            # bomb movement
            bombY[i] += bombY_change[i]

            if score_value >= 25:
                if bombY[i] <= 900:
                    bombY_change[i] = 1
                    bombY[i] += bombY_change[i]
                if bombY[i] >= random.randint(700, 800):
                    bombX[i] = random.randint(120, 900)
                    bombY[i] = random.randint(-50, 0)
                bomb(bombX[i], bombY[i], i)
                collision2 = isCollision2(bombX[i], bombY[i], playerX, playerY)
                if collision2:
                    with open(
                        "bin/hi-score.txt",
                        "w",
                    ) as f:
                        f.write(str(hi_score))
                    for j in range(num_of_enemies):
                        enemyY[j] = 2000
                    game_over_text()
                    break

            # collison
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 600
                bullet_state = "ready"
                score_value += 1
                pts_value += 5 * random.randint(1, 3)
                enemyX[i] = random.randint(120, 900)
                enemyY[i] = random.randint(-50, 150)
                num -= 1
                print (num)

            enemy(enemyX[i], enemyY[i], i)

            

            if score_value >= 25:
                if enemyX[i] <= 120:
                    enemyX_change[i] = 4
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 900:
                    enemyX_change[i] = -4
                    enemyY[i] += enemyY_change[i]

        # bullet movement
        if bulletY <= 0:
            bulletY = 600
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        
        ver()
        upgrade_text()
        player(playerX, playerY)
        show_score(textX, textY)
        show_pts(20, 650)
        high_score(textX, textY + 30)
        pygame.display.update()
        clock.tick(60)


click = False


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


menu()
