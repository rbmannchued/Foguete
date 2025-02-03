import pygame
import random
import math

class Particle:
    def __init__(self, x, y, base_angle, speed, lifetime, color):
        self.x = x
        self.y = y
        # Adiciona uma variação aleatória ao ângulo base (em graus)
        self.angle = base_angle + random.uniform(-15, 15)
        self.speed = speed * random.uniform(0.8, 1.2)
        self.lifetime = lifetime
        self.color = color
        self.age = 0
        self.radius = random.randint(2, 4)
        
        # Converte o ângulo para radianos para calcular a velocidade
        rad = math.radians(self.angle)
        self.vx = math.cos(rad) * self.speed
        self.vy = math.sin(rad) * self.speed

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.age += 1

    def is_dead(self):
        return self.age >= self.lifetime

    def draw(self, surface):
        # Calcula a opacidade com base na idade da partícula
        alpha = max(255 - int(255 * (self.age / self.lifetime)), 0)
        color = (*self.color, alpha)
        # Cria uma superfície temporária para desenhar a partícula com transparência
        particle_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, color, (self.radius, self.radius), self.radius)
        surface.blit(particle_surface, (self.x - self.radius, self.y - self.radius))
