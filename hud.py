import pygame
import math

class HUD:
    def __init__(self, font):
        self.font = font

    def draw(self, surface, rocket, old_vx, old_vy, fps, screen_height, ground_height):
        # Calcula a aceleração (pixels/s²) a partir da variação de velocidade entre frames
        ax = (rocket.vx - old_vx) * fps
        ay = (rocket.vy - old_vy) * fps
        acceleration = math.sqrt(ax ** 2 + ay ** 2)

        # Calcula a altitude: distância entre a parte inferior do foguete e o topo do solo
        altitude = (screen_height - ground_height) - (rocket.y + rocket.height)

        # Renderiza os textos do HUD
        angle_text = self.font.render(f"Ângulo: {rocket.angle:.1f}°", True, (255, 255, 255))
        accel_text = self.font.render(f"Aceleração: {acceleration:.1f} px/s²", True, (255, 255, 255))
        alt_text = self.font.render(f"Altitude: {altitude:.1f} px", True, (255, 255, 255))

        # Exibe os textos no canto superior esquerdo
        surface.blit(angle_text, (10, 10))
        surface.blit(accel_text, (10, 35))
        surface.blit(alt_text, (10, 60))
