import pygame
import sys
from rocket import Rocket
from hud import HUD

# Dimensões da tela e do solo
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 50

# Dimensões do foguete
ROCKET_WIDTH = 20
ROCKET_HEIGHT = 40

# Cores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Configurações do jogo
FPS = 60

# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Foguetinho com HUD - Decolagem, Rotação e Pouso")
clock = pygame.time.Clock()

# Cria uma fonte para o HUD
font = pygame.font.SysFont("Arial", 20)
hud = HUD(font)

# Cria a superfície base do foguete (com transparência)
base_rocket_surface = pygame.Surface((ROCKET_WIDTH, ROCKET_HEIGHT), pygame.SRCALPHA)
base_rocket_surface.fill(RED)

# Posição inicial do foguete (centralizado horizontalmente e sobre o solo)
rocket_start_x = SCREEN_WIDTH // 2 - ROCKET_WIDTH // 2
rocket_start_y = SCREEN_HEIGHT - GROUND_HEIGHT - ROCKET_HEIGHT

# Cria o objeto Rocket
rocket = Rocket(x=rocket_start_x,
                y=rocket_start_y,
                width=ROCKET_WIDTH,
                height=ROCKET_HEIGHT,
                base_surface=base_rocket_surface,
                safe_angle_threshold=10,
                thrust=0.5,
                angular_velocity=2,
                friction=0.99,
                gravity=0.2)

running = True
while running:
    dt = 1 / FPS
    clock.tick(FPS)

    # Armazena as velocidades anteriores para calcular a aceleração
    old_vx = rocket.vx
    old_vy = rocket.vy

    # Processa eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Define o nível do solo para o foguete
    ground_level = SCREEN_HEIGHT - GROUND_HEIGHT - ROCKET_HEIGHT

    # Atualiza o foguete (fisica, colisão e, se necessário, explosão)
    rocket.update(ground_level)

    # Se o foguete explodiu e o timer terminou, encerra o jogo
    if rocket.exploded and rocket.explosion_timer <= 0:
        running = False

    # Desenha o fundo e o solo
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

    # Desenha o foguete
    rocket.draw(screen)

    # Desenha o HUD
    hud.draw(screen, rocket, old_vx, old_vy, FPS, SCREEN_HEIGHT, GROUND_HEIGHT)

    # Atualiza a tela
    pygame.display.flip()

pygame.quit()
sys.exit()
