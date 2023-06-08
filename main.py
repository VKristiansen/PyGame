import pygame
import os

pygame.font.init()  # initialize the font library of pygame
pygame.mixer.init()  # initialize the sound effects of pygame

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceships")

WHITE = (255, 255, 255)  # white color
BLACK = (0, 0, 0)  # back color
RED = (255, 0, 0)  # red color
YELLOW = (255, 255, 0)  # yellow color


FPS = 60  # the FPS that will run

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

VEL = 5

BULLET_VEL = 7  # the bullet velocity is faster than the characters

MAX_BULLETS = 3  # the max number of the bullets that you have


BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# define the font of the health
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
# define the font of the winner
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
# load the yellow spaceship image
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(
    'Assets', 'spaceship_yellow.png'))

# rotate and downscale the yellow spaceship image
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# load the red spaceship image
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(
    'Assets', 'spaceship_red.png'))

# rotate and downscale the red spaceship image
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# define the bullet sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'Gun+Silencer.mp3'))

# load the backround
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# create a custom user event
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # 1st
    # fill the backround (you must to draw a backaround every singe framerate)
    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)  # add the border
    red_health_text = HEALTH_FONT.render("Health:" + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health:" + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    # 2nd
    # add the yellow spaceship
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))  # add the red spaceship

    # draw the red bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    # draw the yellow bullets
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()  # you must always update the display to change color


# Yellow spaceship controls
def yellow_controls(keys_pressed, yellow):
    # note that every image is a rectange
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # Left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # Right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # Up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # Down
        yellow.y += VEL


# Red spaceship controls
def red_controls(keys_pressed, red):
    if keys_pressed[pygame.K_j] and red.x - VEL > BORDER.x + BORDER.width:  # Left
        red.x -= VEL
    if keys_pressed[pygame.K_l] and red.x + VEL + red.width < WIDTH:  # Right
        red.x += VEL
    if keys_pressed[pygame.K_i] and red.y - VEL > 0:  # Up
        red.y -= VEL
    if keys_pressed[pygame.K_k] and red.y + VEL + red.height < HEIGHT - 15:  # Down
        red.y += VEL


# This function handle how the character and the bullets interact
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL  # bullets movement
        # check if the yellow bullet hit the red character
        if red.colliderect(bullet):
            # post on the RED_HIT event
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL  # bullets movement
        # check if the red bullet hit the yellow character
        if yellow.colliderect(bullet):
            # post on the YELLOW_HIT event
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
             2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    # pause the game for 5 seconds to show the winner text
    pygame.time.delay(5000)


def main():
    # define the spaceship positions
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []  # red bullets capacity
    yellow_bullets = []  # yellow bullets capacity

    red_health = 10  # health of the red spaceship
    yellow_health = 10  # health of the yellowq spaceship

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # you must to press the button repeately to fire the bullets
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    # the position that the bullet will spawn
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    # appent them to the yellow bullets list
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    # the position that the bullet will spawn
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    # appent them to the red bullets list
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # add the hit events
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        # define the winner
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        # add the controls
        keys_pressed = pygame.key.get_pressed()

        # call the controls
        yellow_controls(keys_pressed, yellow)
        red_controls(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
