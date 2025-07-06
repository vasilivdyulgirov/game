import pygame
import random

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Избягай от блоковете")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Играч
player = pygame.Rect(WIDTH//2 - 40, HEIGHT - 30, 80, 20)
player_speed = 7

# Падащи блокове
blocks = [pygame.Rect(random.randint(0, WIDTH - 20), -100 * i, 20, 20) for i in range(3)]
block_speed = 5

lives = 3
score = 0
running = True

while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    # Движение на играча
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed

    # Движение на блоковете
    for block in blocks:
        block.y += block_speed
        if block.colliderect(player):
            lives -= 1
            block.y = -20
            block.x = random.randint(0, WIDTH - 20)
        elif block.y > HEIGHT:
            block.y = -20
            block.x = random.randint(0, WIDTH - 20)
            score += 1

        pygame.draw.rect(screen, (255, 0, 0), block)

    # Рисуване на играча
    pygame.draw.rect(screen, (0, 255, 0), player)

    # Точки и животи
    score_text = font.render(f"Точки: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Животи: {lives}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

    pygame.display.flip()

    if lives <= 0:
        end_text = font.render("Край на играта!", True, (255, 0, 0))
        screen.blit(end_text, (WIDTH//2 - 100, HEIGHT//2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
