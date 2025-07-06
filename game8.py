import pygame
import random

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 420, 620
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Бягай от блоковете!")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Звук при сблъсък
pygame.mixer.init()
import os

base_path = os.path.dirname(__file__)
sound_path = os.path.join(base_path, "glass.wav")
impact_sound = pygame.mixer.Sound(sound_path)

# Начален екран
begin = True
while begin:
    window.fill((15, 15, 30))
    intro = font.render("Натисни бутон за старт", True, (180, 180, 255))
    window.blit(intro, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
    pygame.display.flip()
    for evt in pygame.event.get():
        if evt.type == pygame.KEYDOWN:
            begin = False

# Играч
player = pygame.Rect(SCREEN_WIDTH//2 - 35, SCREEN_HEIGHT - 35, 70, 20)
player_velocity = 6

# Блокове
falling_blocks = [pygame.Rect(random.randint(0, SCREEN_WIDTH - 25), -120 * i, 25, 25) for i in range(3)]
falling_speed = 4

# Специален блок
health_block = pygame.Rect(random.randint(0, SCREEN_WIDTH - 40), -250, 40, 20)
health_speed = 3

lives = 3
points = 0
start_ticks = pygame.time.get_ticks()
time_cap = 60
active = True

while active:
    clock.tick(60)
    window.fill((0, 0, 0))

    # Таймер
    seconds_elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining_secs = max(0, time_cap - seconds_elapsed)
    if remaining_secs == 0:
        active = False

    # Движение на играча
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.left > 0:
        player.x -= player_velocity
    if keys[pygame.K_d] and player.right < SCREEN_WIDTH:
        player.x += player_velocity

    # Блокове
    for blk in falling_blocks:
        blk.y += falling_speed
        if blk.colliderect(player):
            impact_sound.play()
            lives -= 1
            blk.y = -25
            blk.x = random.randint(0, SCREEN_WIDTH - 25)
        elif blk.y > SCREEN_HEIGHT:
            blk.y = -25
            blk.x = random.randint(0, SCREEN_WIDTH - 25)
            points += 1
            falling_speed = min(falling_speed + 0.2, 10)  # динамично ускорение
        pygame.draw.rect(window, (255, 40, 40), blk)

    # Специален блок
    health_block.y += health_speed
    if health_block.colliderect(player):
        lives += 1
        health_block.y = -300
        health_block.x = random.randint(0, SCREEN_WIDTH - 40)
    elif health_block.y > SCREEN_HEIGHT:
        health_block.y = -300
        health_block.x = random.randint(0, SCREEN_WIDTH - 40)

    # Рисуване
    pygame.draw.rect(window, (40, 255, 40), player)
    pygame.draw.rect(window, (0, 150, 255), health_block)

    # Инфо
    score_disp = font.render(f"Точки: {points}", True, (255, 255, 255))
    life_disp = font.render(f"Животи: {lives}", True, (255, 255, 255))
    timer_disp = font.render(f"Време: {remaining_secs}s", True, (255, 255, 255))
    window.blit(score_disp, (10, 10))
    window.blit(life_disp, (10, 40))
    window.blit(timer_disp, (SCREEN_WIDTH - 200, 10))

    pygame.display.flip()

    if lives <= 0:
        end_text = font.render("КРАЙ НА ИГРАТА!", True, (255, 0, 0))
        window.blit(end_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
        pygame.display.flip()
        pygame.time.delay(3000)
        break

    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            active = False

pygame.quit()