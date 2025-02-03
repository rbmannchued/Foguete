import pygame
import sys
import math

# Inicializa o Pygame
pygame.init()

# Dimensões da tela e do solo
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 50

# Dimensões do foguete
ROCKET_WIDTH = 20
ROCKET_HEIGHT = 40

# Cores (RGB)
BLACK  = (0, 0, 0)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)
YELLOW = (255, 255, 0)

# Cria a janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Foguetinho - Decolagem, Rotação e Pouso")

# Define o clock para controlar os FPS
clock = pygame.time.Clock()
FPS = 60

# Posição inicial do foguete: centralizado horizontalmente e sobre o solo
rocket_x = SCREEN_WIDTH // 2 - ROCKET_WIDTH // 2
rocket_y = SCREEN_HEIGHT - GROUND_HEIGHT - ROCKET_HEIGHT

# Velocidades iniciais
rocket_vx = 0
rocket_vy = 0

# Estado do foguete: ângulo em graus (0° aponta para cima)
rocket_angle = 0

# Constantes da simulação
GRAVITY = 0.2         # aceleração gravitacional
THRUST = 0.5          # magnitude do impulso (aplicado na direção do ângulo do foguete)
ANGULAR_VELOCITY = 2  # graus que o foguete rotaciona por frame
FRICTION = 0.99       # atrito que diminui a velocidade horizontal

# Limite para pouso seguro (ângulo absoluto menor ou igual a 10°)
SAFE_ANGLE_THRESHOLD = 10

# Variáveis de controle de explosão
exploded = False
explosion_timer = 0  # contagem regressiva (em frames) para finalizar a explosão

# Cria uma superfície base para o foguete (com transparência)
base_rocket_surface = pygame.Surface((ROCKET_WIDTH, ROCKET_HEIGHT), pygame.SRCALPHA)
base_rocket_surface.fill(RED)

running = True
while running:
    clock.tick(FPS)

    # Processa os eventos (fechar janela, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Se o foguete ainda não explodiu, atualiza controles e física
    if not exploded:
        keys = pygame.key.get_pressed()

        # Controle de rotação: ajusta o ângulo do foguete
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            rocket_angle += ANGULAR_VELOCITY  # rotaciona anti-horário (para a esquerda)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            rocket_angle -= ANGULAR_VELOCITY  # rotaciona horário (para a direita)

        # Normaliza o ângulo para ficar entre -180 e 180 graus
        if rocket_angle > 180:
            rocket_angle -= 360
        elif rocket_angle < -180:
            rocket_angle += 360

        # Impulso: aplica aceleração na direção apontada pelo foguete
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            # Quando o foguete está com 0° o impulso é para cima.
            # Usamos seno e cosseno (convertendo para radianos) para obter os componentes.
            rocket_vx += -THRUST * math.sin(math.radians(rocket_angle))
            rocket_vy += -THRUST * math.cos(math.radians(rocket_angle))

        # Aplica a gravidade (sempre puxa para baixo)
        rocket_vy += GRAVITY

        # Atualiza a posição do foguete
        rocket_x += rocket_vx
        rocket_y += rocket_vy

        # Aplica atrito na velocidade horizontal
        rocket_vx *= FRICTION

        # Impede que o foguete saia da tela horizontalmente
        if rocket_x < 0:
            rocket_x = 0
            rocket_vx = 0
        if rocket_x > SCREEN_WIDTH - ROCKET_WIDTH:
            rocket_x = SCREEN_WIDTH - ROCKET_WIDTH
            rocket_vx = 0

        # Verifica colisão com o solo
        ground_level = SCREEN_HEIGHT - GROUND_HEIGHT - ROCKET_HEIGHT
        if rocket_y > ground_level:
            rocket_y = ground_level
            rocket_vy = 0
            # Se o ângulo de pouso for maior que o permitido, o foguete explode
            if abs(rocket_angle) > SAFE_ANGLE_THRESHOLD:
                exploded = True
                explosion_timer = 60  # duração da explosão (ex.: 60 frames ≈ 1 segundo)

    else:
        # Se explodiu, atualiza o timer da explosão e encerra após a contagem
        explosion_timer -= 1
        if explosion_timer <= 0:
            running = False

    # Desenho da cena
    screen.fill(BLACK)
    # Desenha o solo
    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

    if exploded:
        # Efeito simples de explosão: um círculo que aumenta de tamanho
        rocket_center_x = int(rocket_x + ROCKET_WIDTH / 2)
        rocket_center_y = int(rocket_y + ROCKET_HEIGHT / 2)
        # O raio cresce à medida que o timer diminui
        explosion_radius = 40 - explosion_timer
        pygame.draw.circle(screen, YELLOW, (rocket_center_x, rocket_center_y), explosion_radius)
    else:
        # Rotaciona a imagem do foguete de acordo com o ângulo atual
        rotated_surface = pygame.transform.rotate(base_rocket_surface, rocket_angle)
        # Define o retângulo de forma que o centro fique na posição atual do foguete
        rotated_rect = rotated_surface.get_rect(center=(rocket_x + ROCKET_WIDTH / 2,
                                                        rocket_y + ROCKET_HEIGHT / 2))
        screen.blit(rotated_surface, rotated_rect.topleft)

    # Atualiza a tela
    pygame.display.flip()

# Encerra o Pygame e o programa
pygame.quit()
sys.exit()
