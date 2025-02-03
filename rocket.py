import pygame
import math

class Rocket:
    def __init__(self, x, y, width, height, base_surface,
                 safe_angle_threshold=10, thrust=0.5,
                 angular_velocity=2, friction=0.99, gravity=0.2):
        # Posição e dimensões
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Velocidades
        self.vx = 0
        self.vy = 0

        # Ângulo atual (em graus, onde 0° aponta para cima)
        self.angle = 0

        # Configurações do foguete
        self.thrust = thrust
        self.angular_velocity = angular_velocity
        self.friction = friction
        self.gravity = gravity

        # Parâmetro para pouso seguro
        self.safe_angle_threshold = safe_angle_threshold

        # Variáveis de controle de explosão
        self.exploded = False
        self.explosion_timer = 0  # duração da explosão (em frames)

        # Superfície base (imagem) do foguete
        self.base_surface = base_surface

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Controle de rotação: esquerda/A para aumentar o ângulo e direita/D para diminuir
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle += self.angular_velocity
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle -= self.angular_velocity

        # Normaliza o ângulo para ficar entre -180° e 180°
        if self.angle > 180:
            self.angle -= 360
        elif self.angle < -180:
            self.angle += 360

        # Impulso: aplica aceleração na direção apontada pelo foguete
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vx += -self.thrust * math.sin(math.radians(self.angle))
            self.vy += -self.thrust * math.cos(math.radians(self.angle))

    def update(self, ground_level):
        """Atualiza a física e verifica colisões/explosão."""
        if not self.exploded:
            self.handle_input()

            # Aplica a gravidade (sempre puxa para baixo)
            self.vy += self.gravity

            # Atualiza a posição do foguete
            self.x += self.vx
            self.y += self.vy

            # Aplica atrito na velocidade horizontal
            self.vx *= self.friction

            # Verifica colisão com o solo
            if self.y > ground_level:
                self.y = ground_level
                self.vy = 0

                # Se o ângulo de pouso estiver fora do limite seguro, o foguete explode
                if abs(self.angle) > self.safe_angle_threshold:
                    self.exploded = True
                    self.explosion_timer = 60  # por exemplo, 60 frames (~1 segundo)
        else:
            # Se explodiu, atualiza o timer da explosão
            self.explosion_timer -= 1

    def draw(self, surface):
        """Renderiza o foguete (ou a explosão, se for o caso)."""
        if self.exploded:
            # Efeito simples de explosão: um círculo que aumenta de tamanho
            rocket_center_x = int(self.x + self.width / 2)
            rocket_center_y = int(self.y + self.height / 2)
            explosion_radius = 40 - self.explosion_timer  # o círculo cresce com o tempo
            pygame.draw.circle(surface, (255, 255, 0), (rocket_center_x, rocket_center_y), explosion_radius)
        else:
            # Rotaciona a imagem base conforme o ângulo atual
            rotated_surface = pygame.transform.rotate(self.base_surface, self.angle)
            rotated_rect = rotated_surface.get_rect(center=(self.x + self.width / 2,
                                                            self.y + self.height / 2))
            surface.blit(rotated_surface, rotated_rect.topleft)
