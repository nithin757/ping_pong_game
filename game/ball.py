import pygame
import random

pygame.mixer.init()


paddle_sound = pygame.mixer.Sound("sounds/paddle_hit.wav")
wall_sound = pygame.mixer.Sound("sounds/wall_bounce.wav")
score_sound = pygame.mixer.Sound("sounds/score.wav")


class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.original_x = x
        self.original_y = y
        self.velocity_x = 5
        self.velocity_y = 3

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            wall_sound.play()

    def reset(self, direction=None):
        self.x = self.original_x
        self.y = self.original_y

        if direction is not None:
            self.velocity_x = 5 * direction
        else:
            self.velocity_x *= -1

        self.velocity_y = random.choice([-3, 3])
        
        score_sound.play()



    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
