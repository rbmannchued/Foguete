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
LANDING_ZONE_X = 300
LANDING_ZONE_WIDTH = 200

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
GRAVITY = 0.2
THRUST = 0.3
ANGULAR_VELOCITY = 2
FRICTION = 0.99
SAFE_ANGLE_THRESHOLD = 10
SAFE_VELOCITY_THRESHOLD = 2
MAX_ALTITUDE = 150  # Altura máxima aceitável para evitar voos infinitos
MAX_FLIGHT_TIME = 400  # Tempo máximo permitido para voar sem descer
DESCENT_THRESHOLD = -0.5  # Velocidade mínima esperada para descer

# Cria uma superfície base para o foguete (com transparência)
base_rocket_surface = pygame.Surface((ROCKET_WIDTH, ROCKET_HEIGHT), pygame.SRCALPHA)
base_rocket_surface.fill(RED)

# Função para avaliar o desempenho de cada genoma
def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        rocket_x = SCREEN_WIDTH // 2 - ROCKET_WIDTH // 2
        rocket_y = SCREEN_HEIGHT - GROUND_HEIGHT - ROCKET_HEIGHT
        rocket_vx = 0
        rocket_vy = 0
        rocket_angle = 0
        exploded = False
        fitness = 0
        flight_time = 0

        net = neat.nn.FeedForwardNetwork.create(genome, config)

        running = True
        while running and not exploded:
            screen.fill(BLACK)
            pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
            pygame.draw.rect(screen, YELLOW, (LANDING_ZONE_X, SCREEN_HEIGHT - GROUND_HEIGHT, LANDING_ZONE_WIDTH, GROUND_HEIGHT))

            inputs = [
                (rocket_x - LANDING_ZONE_X) / SCREEN_WIDTH,
                rocket_y / SCREEN_HEIGHT,
                rocket_vx / 10,
                rocket_vy / 10,
                rocket_angle / 180
            ]

            output = net.activate(inputs)

            if output[0] > 0.5:
                rocket_vx += -THRUST * math.sin(math.radians(rocket_angle))
                rocket_vy += -THRUST * math.cos(math.radians(rocket_angle))
                fitness += 5
            if output[1] > 0.5:
                rocket_angle += ANGULAR_VELOCITY
            if output[2] > 0.5:
                rocket_angle -= ANGULAR_VELOCITY

            rocket_vy += GRAVITY
            rocket_vx *= FRICTION
            rocket_x += rocket_vx
            rocket_y += rocket_vy
            flight_time += 1

            if rocket_x < 0:
                rocket_x = 0
                rocket_vx = 0
            if rocket_x + ROCKET_WIDTH > SCREEN_WIDTH:
                rocket_x = SCREEN_WIDTH - ROCKET_WIDTH
                rocket_vx = 0
            if rocket_y < 0:
                rocket_y = 0
                rocket_vy = 0

            ground_level = SCREEN_HEIGHT - GROUND_HEIGHT - ROCKET_HEIGHT
            if rocket_y > ground_level:
                rocket_y = ground_level
                rocket_vy = 0
                if abs(rocket_angle) > SAFE_ANGLE_THRESHOLD or abs(rocket_vx) > SAFE_VELOCITY_THRESHOLD or abs(rocket_vy) > SAFE_VELOCITY_THRESHOLD:
                    exploded = True
                elif LANDING_ZONE_X <= rocket_x <= LANDING_ZONE_X + LANDING_ZONE_WIDTH:
                    fitness += 2000
                else:
                    fitness += 500
                running = False

            if rocket_y < MAX_ALTITUDE:
                fitness -= 2  # Penaliza ainda mais ficar muito alto sem descer
                if rocket_vy > DESCENT_THRESHOLD:
                    fitness -= 5  # Penaliza fortemente se não estiver descendo

            if flight_time > MAX_FLIGHT_TIME:
                running = False  # Encerra a simulação se ficar tempo demais no ar

            fitness += 0.1

            rotated_rocket = pygame.transform.rotate(base_rocket_surface, rocket_angle)
            rocket_rect = rotated_rocket.get_rect(center=(rocket_x + ROCKET_WIDTH // 2, rocket_y + ROCKET_HEIGHT // 2))
            screen.blit(rotated_rocket, rocket_rect.topleft)

            pygame.display.flip()
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        genome.fitness = fitness

# Função principal para rodar o NEAT
def run_neat(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    winner = population.run(eval_genomes, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run_neat(config_path)
