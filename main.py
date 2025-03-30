import pygame
import random
import os
import json

# Inicializa o pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter Demo")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Carrega os assets
player_img = pygame.image.load(os.path.join("assets", "player.png"))
enemy1_img = pygame.image.load(os.path.join("assets", "enemy1.png"))  # Inimigo básico
enemy2_img = pygame.image.load(os.path.join("assets", "enemy2.png"))  # Inimigo que atira
enemy3_img = pygame.image.load(os.path.join("assets", "enemy3.png"))  # Inimigo zigue-zague
boss_img = pygame.image.load(os.path.join("assets", "boss.png"))
bullet_img = pygame.image.load(os.path.join("assets", "bullet.png"))
powerup_img = pygame.image.load(os.path.join("assets", "powerup.png"))
background1_img = pygame.image.load(os.path.join("assets", "background1.png"))
background2_img = pygame.image.load(os.path.join("assets", "background2.png"))
background3_img = pygame.image.load(os.path.join("assets", "background3.png"))
shoot_sound = pygame.mixer.Sound(os.path.join("assets", "shoot.wav"))
explosion_sound = pygame.mixer.Sound(os.path.join("assets", "explosion.wav"))
powerup_sound = pygame.mixer.Sound(os.path.join("assets", "powerup.wav"))

# Clock para controlar o FPS
clock = pygame.time.Clock()

# Fonte para exibir textos
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Variáveis do jogo
score = 0
high_score = 0
level = 1
lives = 3
running = True
game_over = False
paused = False
boss_spawned = False

# Carrega o high score
if os.path.exists("high_score.json"):
    with open("high_score.json", "r") as file:
        high_score = json.load(file)

# Classe do Jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.shoot_delay = 250  # Delay entre tiros
        self.last_shot = pygame.time.get_ticks()
        self.powerup_time = 0
        self.powerup_active = False

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.powerup_active:
                # Tiros triplos
                bullet1 = Bullet(self.rect.centerx - 20, self.rect.top)
                bullet2 = Bullet(self.rect.centerx, self.rect.top)
                bullet3 = Bullet(self.rect.centerx + 20, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
            else:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            shoot_sound.play()

# Classe do Inimigo Básico (Nível 1)
class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy1_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 4)

# Classe do Inimigo que Atira (Nível 2)
class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy2_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(2, 5)
        self.shoot_delay = 1000  # Delay entre tiros
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(2, 5)

        # Atira em direção ao jogador
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
            shoot_sound.play()

# Classe do Inimigo Zigue-Zague (Nível 3)
class Enemy3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy3_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(3, 6)
        self.speed_x = random.choice([-2, 2])  # Movimento lateral

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(3, 6)
            self.speed_x = random.choice([-2, 2])
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x = -self.speed_x  # Inverte a direção ao atingir as bordas

# Classe do Tiro do Inimigo
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed_y = 5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Classe do Tiro do Jogador
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Classe do Chefe
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = boss_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.y = -100
        self.speed_y = 1
        self.health = 50

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT // 4:
            self.speed_y = 0

# Classe do Power-up
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = powerup_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = 2

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.kill()

# Função para exibir mensagem na tela
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Função para reiniciar o jogo
def reset_game():
    global score, level, lives, running, game_over, boss_spawned
    score = 0
    level = 1
    lives = 3
    boss_spawned = False
    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    enemy_bullets.empty()
    powerups.empty()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        enemy = Enemy1()
        all_sprites.add(enemy)
        enemies.add(enemy)
    running = True
    game_over = False

# Função para mostrar a tela de pausa
def show_pause_menu():
    screen.fill(BLACK)
    draw_text("Pausado", large_font, WHITE, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
    draw_text("Pressione P para continuar", font, WHITE, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()

# Função para mostrar a tela de instruções
def show_instructions():
    screen.fill(BLACK)
    draw_text("Space Shooter", large_font, WHITE, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 200)
    draw_text("Instruções:", font, WHITE, screen, SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 100)
    draw_text("Mova a nave com as setas <- e ->", font, WHITE, screen, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50)
    draw_text("Atire com a tecla ESPAÇO", font, WHITE, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)
    draw_text("Destrua os inimigos e marque pontos!", font, WHITE, screen, SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 + 50)
    draw_text("Pressione P dentro do jogo para pausar", font, WHITE, screen, SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT // 2 + 100)
    draw_text("Pressione ENTER para começar", font, WHITE, screen, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 150)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Tecla Enter para começar
                    return True

# Função para mostrar a animação de transição entre níveis
def show_level_transition(new_level):
    screen.fill(BLACK)
    draw_text(f"Nível {new_level}", large_font, WHITE, screen, SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 50)
    pygame.display.flip()
    pygame.time.delay(1000)  # Pausa de 1 segundo

    # Contagem regressiva
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        draw_text(f"{i}", large_font, WHITE, screen, SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 50)
        pygame.display.flip()
        pygame.time.delay(1000)  # Pausa de 1 segundo entre os números

# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    enemy = Enemy1()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Mostra as instruções antes de começar
if not show_instructions():
    running = False

# Loop do jogo
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Tecla Espaço para atirar
                player.shoot()
            if event.key == pygame.K_p:  # Tecla P para pausar
                paused = not paused

    if not game_over and not paused:
        # Atualiza
        all_sprites.update()

        # Colisões entre tiros e inimigos
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            explosion_sound.play()
            score += 10  # Incrementa a pontuação
            if random.random() > 0.9:  # 10% de chance de spawnar um power-up
                powerup = PowerUp()
                all_sprites.add(powerup)
                powerups.add(powerup)
            if level == 1:
                enemy = Enemy1()
            elif level == 2:
                enemy = Enemy2()
            elif level == 3:
                enemy = Enemy3()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Colisões entre jogador e inimigos
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            lives -= 1
            if lives == 0:
                game_over = True
            else:
                player.rect.centerx = SCREEN_WIDTH // 2
                player.rect.bottom = SCREEN_HEIGHT - 10

        # Colisões entre jogador e tiros dos inimigos
        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if hits:
            lives -= 1
            if lives == 0:
                game_over = True
            else:
                player.rect.centerx = SCREEN_WIDTH // 2
                player.rect.bottom = SCREEN_HEIGHT - 10

        # Colisões entre jogador e power-ups
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            powerup_sound.play()
            player.powerup_time = pygame.time.get_ticks() + 5000  # Power-up dura 5 segundos
            player.powerup_active = True

        # Verifica se o power-up acabou
        if player.powerup_active and pygame.time.get_ticks() > player.powerup_time:
            player.powerup_active = False

        # Spawn do chefe aos 1000 pontos
        if score >= 1000 and not boss_spawned:
            boss = Boss()
            all_sprites.add(boss)
            enemies.add(boss)
            boss_spawned = True

        # Aumenta a dificuldade conforme a pontuação
        if score >= 500 and level == 1:
            level = 2
            show_level_transition(level)
            for enemy in enemies:
                enemy.kill()
            for i in range(8):
                enemy = Enemy2()
                all_sprites.add(enemy)
                enemies.add(enemy)
        elif score >= 1000 and level == 2:
            level = 3
            show_level_transition(level)
            for enemy in enemies:
                enemy.kill()
            for i in range(8):
                enemy = Enemy3()
                all_sprites.add(enemy)
                enemies.add(enemy)

        # Desenha o fundo conforme o nível
        if level == 1:
            screen.blit(background1_img, (0, 0))
        elif level == 2:
            screen.blit(background2_img, (0, 0))
        elif level == 3:
            screen.blit(background3_img, (0, 0))

        all_sprites.draw(screen)

        # Exibe a pontuação, nível e vidas na tela
        draw_text(f"Pontuação: {score}", font, WHITE, screen, 10, 10)
        draw_text(f"Nível: {level}", font, WHITE, screen, 10, 50)
        draw_text(f"vidas: {lives}", font, WHITE, screen, 10, 90)

    elif paused:
        show_pause_menu()

    else:
        # Tela de Game Over
        if score > high_score:
            high_score = score
            with open("high_score.json", "w") as file:
                json.dump(high_score, file)
        draw_text("Game Over", large_font, RED, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
        draw_text(f"Pontuação Final: {score}", font, WHITE, screen, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2)
        draw_text(f"Pontuação Máxima: {high_score}", font, WHITE, screen, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 50)
        draw_text("Pressione R para Reiniciar ou Q para sair", font, WHITE, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100)
        pygame.display.flip()

        # Espera a decisão do jogador
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Reiniciar
                        reset_game()
                        waiting = False
                    if event.key == pygame.K_q:  # Sair
                        running = False
                        waiting = False

    pygame.display.flip()

pygame.quit()