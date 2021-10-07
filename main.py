import pygame
from random import randrange as rnd

pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
sc = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arkanoid")
clock = pygame.time.Clock()
FPS = 80

# Colors
YELLOW = (255, 213, 113)
WHITE = (255, 255, 255)

# Background image settings
img = pygame.image.load("1.png").convert()
img = pygame.transform.scale(img, (1200, 800))
img_y = 0
scroll_value = 1


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


# Paddle Settings
paddle_width = 300
paddle_height = 30
paddle_speed = 15
paddle = pygame.Rect(SCREEN_WIDTH / 2 - paddle_width / 2, SCREEN_HEIGHT - paddle_height - 10, paddle_width,
                     paddle_height)

# Ball Settings
ball_radius = 15
ball_speed = 5
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, SCREEN_WIDTH - ball_rect), SCREEN_HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# Blocks settings
block_list = [pygame.Rect(5 + 120 * i, 5 + 70 * j, 110, 60) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

# Main game loop
active = True
while active:
    # Check for user events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

    # Draw the background on screen
    sc.blit(img, (0, 0 + scroll_value))  # top
    sc.blit(img, (0, -img.get_height() + scroll_value))  # bottom
    scroll_value += 1
    if scroll_value >= SCREEN_HEIGHT:
        scroll_value = 1

    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, YELLOW, paddle)
    pygame.draw.circle(sc, WHITE, ball.center, ball_radius)

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.right += paddle_speed

    # Ball Movement
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    # Ball Collision Left / Right
    if ball.centerx < ball_radius or ball.centerx > SCREEN_WIDTH - ball_radius:
        dx = -dx

    # Ball Collision Top
    if ball.centery < ball_radius:
        dy = -dy

    # Ball Collision Paddle from Top
    if ball.colliderect(paddle) and dy > 0:
        # dx, dy = detect_collision(dx, dy, ball, paddle)
        dx, dy = detect_collision(dx, dy, ball, paddle)

    # Blocks Collision
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        # Effect on collision
        hit_rect.inflate_ip(ball.width * 5, ball.height * 5)
        pygame.draw.rect(sc, hit_color, hit_rect)
        FPS += 2

    pygame.display.update()
    clock.tick(FPS)
