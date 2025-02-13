import pygame
import sys
import math
import neat
import os

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
WHITE  = (255, 255, 255)

# Cria a janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Foguetinho com NEAT - Decolagem e Pouso")

# Define o clock para controlar os FPS
clock = pygame.time.Clock()
FPS = 60

# Constantes da simulação
GRAVITY = 0.2         # aceleração gravitacional
THRUST = 0.5          # magnitude do impulso aplicado
ANGULAR_VELOCITY = 2  # graus que o foguete rotaciona por frame
FRICTION = 0.99       # atrito que diminui a velocidade horizontal
SAFE_ANGLE_THRESHOLD = 10  # limite para pouso seguro

# Cria uma superfície base para o foguete (com transparência)
base_rocket_surface = pygame.Surface((ROCKET_WIDTH, ROCKET_HEIGHT), pygame.SRCALPHA)
base_rocket_surface.fill(RED)

# Cria uma fonte para o HUD
font = pygame.font.SysFont("Arial", 20)

# Função para avaliar o desempenho de cada genoma
def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        # Inicializa o foguete
        rocket_x = SCREEN_WIDTH // 2 - ROCKET_WIDTH // 2
        rocket_y = SCREEN_HEIGHT - GROUND_HEIGHT - ROCKET_HEIGHT
        rocket_vx = 0
        rocket_vy = 0
        rocket_angle = 0
        exploded = False
        fitness = 0

        # Cria a rede neural
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        running = True
        while running and not exploded:
            screen.fill(BLACK)  # Limpa a tela a cada frame

            # Desenha o chão
            pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

            # Entradas da rede neural
            inputs = [
                rocket_x / SCREEN_WIDTH,  # Posição X normalizada
                rocket_y / SCREEN_HEIGHT,  # Posição Y normalizada
                rocket_vx / 10,  # Velocidade X normalizada
                rocket_vy / 10,  # Velocidade Y normalizada
                rocket_angle / 180  # Ângulo normalizado
            ]

            # Saída da rede neural
            output = net.activate(inputs)
            print(f"Saída da rede: {output}")  # Depuração

            # Controle do foguete com base na saída da rede
            if len(output) > 0 and output[0] > 0.5:  # Impulso
                rocket_vx += -THRUST * math.sin(math.radians(rocket_angle))
                rocket_vy += -THRUST * math.cos(math.radians(rocket_angle))
                fitness += 5  # Recompensa por tentar voar

            if len(output) > 1 and output[1] > 0.5:  # Rotacionar para a esquerda
                rocket_angle += ANGULAR_VELOCITY
            if len(output) > 2 and output[2] > 0.5:  # Rotacionar para a direita
                rocket_angle -= ANGULAR_VELOCITY

            # Aplica a gravidade
            rocket_vy += GRAVITY

            # Aplica atrito horizontal
            rocket_vx *= FRICTION

            # Atualiza a posição do foguete
            # Atualiza a posição do foguete
            rocket_x += rocket_vx
            rocket_y += rocket_vy

            # Impede que o foguete saia pelas laterais
            if rocket_x < 0:
                rocket_x = 0
                rocket_vx = 0  # Para evitar que continue tentando sair
            if rocket_x + ROCKET_WIDTH > SCREEN_WIDTH:
                rocket_x = SCREEN_WIDTH - ROCKET_WIDTH
                rocket_vx = 0

                # Impede que o foguete saia pelo topo
            if rocket_y < 0:
                rocket_y = 0
                rocket_vy = 0

            # Verifica se o foguete bateu no chão
            ground_level = SCREEN_HEIGHT - GROUND_HEIGHT - ROCKET_HEIGHT
            if rocket_y > ground_level:
                rocket_y = ground_level
                rocket_vy = 0
                if abs(rocket_angle) > SAFE_ANGLE_THRESHOLD:
                    exploded = True
                else:
                    fitness += 1000  # Recompensa por pousar corretamente
                running = False  # Sai do loop quando o foguete pousar

            # Atualiza o fitness por tempo de sobrevivência
            fitness += 0.1  

            # Desenha o foguete (com rotação)
            rotated_rocket = pygame.transform.rotate(base_rocket_surface, rocket_angle)
            rocket_rect = rotated_rocket.get_rect(center=(rocket_x + ROCKET_WIDTH // 2, rocket_y + ROCKET_HEIGHT // 2))
            screen.blit(rotated_rocket, rocket_rect.topleft)

            # Atualiza a tela
            pygame.display.flip()
            clock.tick(FPS)

            # Verifica eventos do Pygame para permitir fechar a janela
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        # Define o fitness do genoma
        genome.fitness = fitness

# Função principal para rodar o NEAT
def run_neat(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Cria a população
    population = neat.Population(config)

    # Adiciona relatórios de progresso
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Executa o NEAT
    winner = population.run(eval_genomes, 50)  # 50 gerações

# Ponto de entrada do programa
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run_neat(config_path)
    
    
