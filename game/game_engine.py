import pygame
import random
from .paddle import Paddle
from .ball import Ball
from .ball import paddle_sound, wall_sound, score_sound


# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # New: default winning target
        self.target_score = 5


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
    # Move the ball first
        self.ball.move()

        # --- Collision checks ---
        if self.ball.rect().colliderect(self.player.rect()):
            self.ball.x = self.player.x + self.player.width
            self.ball.velocity_x *= -1
            paddle_sound.play()

        elif self.ball.rect().colliderect(self.ai.rect()):
            self.ball.x = self.ai.x - self.ball.width
            self.ball.velocity_x *= -1
            paddle_sound.play()

        # --- Scoring checks ---
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset(direction=1)  # send ball toward player

        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            self.ball.reset(direction=-1)  # send ball toward AI

        # --- AI movement ---
        self.ai.auto_track(self.ball, self.height)




    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        winner_text = None

        if self.player_score >= self.target_score:
            winner_text = "Player Wins!"
        elif self.ai_score >= self.target_score:
            winner_text = "AI Wins!"

        if winner_text:
            # --- Display Winner Message ---
            screen.fill((0, 0, 0))
            win_surface = self.font.render(winner_text, True, (255, 255, 255))
            win_rect = win_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(win_surface, win_rect)

            # --- Display Replay Menu ---
            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]
            for i, opt in enumerate(options):
                text_surface = self.font.render(opt, True, (200, 200, 200))
                text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
                screen.blit(text_surface, text_rect)

            pygame.display.flip()

            # Wait for user input
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        raise SystemExit
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            raise SystemExit
                        elif event.key == pygame.K_3:
                            self.target_score = 2  # Best of 3 → first to 2
                            waiting = False
                        elif event.key == pygame.K_5:
                            self.target_score = 3  # Best of 5 → first to 3
                            waiting = False
                        elif event.key == pygame.K_7:
                            self.target_score = 4  # Best of 7 → first to 4
                            waiting = False

                pygame.time.wait(50)

            # Reset for new match
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset(direction=random.choice([-1, 1]))



