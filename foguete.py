import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Altura do solo (área onde o foguete pousa)
GROUND_HEIGHT = 50

# Dimensões do foguete
ROCKET_WIDTH = 20
ROCKET_HEIGHT = 40

# Cores (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)

# Cria a janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Foguetinho - Decolagem e Pouso")

# Define o clock para controlar os FPS
clock = pygame.time.Clock()
FPS = 60

# Posição inicial do foguete: centralizado horizontalmente e sobre o solo
rocket_x = SCREEN_WIDTH // 2 - ROCKET_WIDTH // 2
# O foguete começa "em cima" do solo (ajustando para a altura do foguete)
rocket_y = SCREEN_HEIGHT - GROUND_HEIGHT - ROCKET_HEIGHT

# Velocidades iniciais
rocket_vx = 0
rocket_vy = 0

# Constantes da simulação
GRAVITY = 0.2         # aceleração gravitacional (para baixo)
THRUST = -0.5         # aceleração do motor (para cima quando ativado)
SIDE_THRUST = 0.3     # aceleração lateral (para movimentos horizontais)
FRICTION = 0.99       # atrito que reduz a velocidade horizontal

# Loop principal do jogo
running = True
while running:
    clock.tick(FPS)
    
    # Eventos (fechar janela, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Verifica quais teclas estão pressionadas (setas e WASD)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        # Ativa o motor: aplica aceleração para cima
        rocket_vy += THRUST
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        # Impulso para a esquerda
        rocket_vx -= SIDE_THRUST
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        # Impulso para a direita
        rocket_vx += SIDE_THRUST

    # Aplica a gravidade (sempre puxa o foguete para baixo)
    rocket_vy += GRAVITY

    # Atualiza a posição do foguete com base nas velocidades
    rocket_x += rocket_vx
    rocket_y += rocket_vy

    # Aplica atrito (diminui lentamente a velocidade horizontal)
    rocket_vx *= FRICTION

    # Define o nível do solo para o foguete (evita que ele desça abaixo)
    ground_level = SCREEN_HEIGHT - GROUND_HEIGHT - ROCKET_HEIGHT
    if rocket_y > ground_level:
        rocket_y = ground_level
        rocket_vy = 0
        # Aqui você pode incluir verificações de velocidade para determinar
        # se o pouso foi seguro ou se ocorreu um "acidente".

    # Impede que o foguete saia para fora da tela horizontalmente
    if rocket_x < 0:
        rocket_x = 0
        rocket_vx = 0
    if rocket_x > SCREEN_WIDTH - ROCKET_WIDTH:
        rocket_x = SCREEN_WIDTH - ROCKET_WIDTH
        rocket_vx = 0

    # Desenha o fundo (preto)
    screen.fill(BLACK)

    # Desenha o solo (um retângulo verde na parte inferior)
    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

    # Desenha o foguete (um retângulo vermelho)
    rocket_rect = pygame.Rect(rocket_x, rocket_y, ROCKET_WIDTH, ROCKET_HEIGHT)
    pygame.draw.rect(screen, RED, rocket_rect)

    # Atualiza a tela
    pygame.display.flip()

# Encerra o Pygame
pygame.quit()
sys.exit()
