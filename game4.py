import pygame
import random

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Хвани блока")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

player = pygame.Rect(WIDTH//2 - 40, HEIGHT - 30, 80, 20)
player_speed = 8

block = pygame.Rect(random.randint(0, WIDTH - 20), 0, 20, 20)
block_speed = 5

# Импортирайте и заредете звук:
pygame.mixer.init()
catch_sound = pygame.mixer.Sound("glass.wav")


missed = 0

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

    # Движение на блока
    block.y += block_speed
    if block.colliderect(player):
        score += 1
        block_speed += 2

        catch_sound.play()

        block.y = 0
        block.x = random.randint(0, WIDTH - 20)
    elif block.y > HEIGHT:
        block.y = 0
        block.x = random.randint(0, WIDTH - 20)

        missed += 1
        if missed >= 5:
            running = False

    # Рисуване
    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (0, 255, 0), block)

    text = font.render(f"Точки: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    m = font.render(f"<пропуснати>: {missed}", True, (255, 255, 255))
    screen.blit(m, (10, 40))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()



