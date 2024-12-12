import pygame
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
FONT_COLOR = (0, 0, 0)

# Stickman class
class Stickman:
    def __init__(self, x, y):
        self.initial_x = x
        self.initial_y = y
        self.x = x
        self.y = y
        self.width = 20
        self.height = 90
        self.speed = 15

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

    def move(self, dy):
        self.y += dy
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))

    def reset_position(self):
        self.x = self.initial_x
        self.y = self.initial_y

# Shuttlecock class
class Shuttlecock:
    def __init__(self):
        self.reset()

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 10)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off top and bottom
        if self.y <= 0 or self.y >= SCREEN_HEIGHT:
            self.speed_y *= -1

    def reset(self, start_with_player=None):
        if start_with_player == "player1":
            self.x = player1.x + player1.width + 5
            self.y = player1.y + player1.height // 2
            self.speed_x = 10
        elif start_with_player == "player2":
            self.x = player2.x - 5
            self.y = player2.y + player2.height // 2
            self.speed_x = -10
        else:
            self.x = SCREEN_WIDTH // 2
            self.y = SCREEN_HEIGHT // 2
            self.speed_x = 10 * random.choice([-1, 1])
            self.speed_y = random.choice([-8, 8])

# Button class
class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Stickman Badminton")
    clock = pygame.time.Clock()

    global player1, player2
    player1 = Stickman(50, SCREEN_HEIGHT // 2)
    player2 = Stickman(SCREEN_WIDTH - 70, SCREEN_HEIGHT // 2)
    shuttlecock = Shuttlecock()

    start_1p_button = Button("1 Player", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 120, 50)
    start_2p_button = Button("2 Player", SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2 - 50, 120, 50)
    exit_button = Button("Exit", SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 20, 120, 50)

    game_active = False
    countdown = False
    countdown_value = 3
    winner = None
    player1_score = 0
    player2_score = 0
    running = True
    mode = None

    def show_countdown():
        nonlocal countdown_value
        while countdown_value > 0:
            screen.fill(WHITE)
            font = pygame.font.SysFont(None, 72)
            countdown_surface = font.render(str(countdown_value), True, BLACK)
            screen.blit(countdown_surface, (SCREEN_WIDTH // 2 - countdown_surface.get_width() // 2, SCREEN_HEIGHT // 2 - countdown_surface.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(1000)
            countdown_value -= 1
        countdown_value = 3

    def ai_move():
        """Simple AI logic to follow the shuttlecock."""
        if shuttlecock.y < player2.y:
            player2.move(-player2.speed)
        elif shuttlecock.y > player2.y + player2.height:
            player2.move(player2.speed)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if start_1p_button.is_clicked(mouse_pos) and not game_active:
                    game_active = True
                    countdown = True
                    winner = None
                    player1_score = 0
                    player2_score = 0
                    mode = "1p"
                elif start_2p_button.is_clicked(mouse_pos) and not game_active:
                    game_active = True
                    countdown = True
                    winner = None
                    player1_score = 0
                    player2_score = 0
                    mode = "2p"
                elif exit_button.is_clicked(mouse_pos):
                    running = False

        if countdown:
            player1.reset_position()
            player2.reset_position()
            if random.choice([True, False]):
                shuttlecock.reset(start_with_player="player1")
            else:
                shuttlecock.reset(start_with_player="player2")
            show_countdown()
            countdown = False

        if game_active and not countdown:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player1.move(-player1.speed)
            if keys[pygame.K_s]:
                player1.move(player1.speed)

            if mode == "2p":
                if keys[pygame.K_UP]:
                    player2.move(-player2.speed)
                if keys[pygame.K_DOWN]:
                    player2.move(player2.speed)
            elif mode == "1p":
                ai_move()

            shuttlecock.update()

            if (shuttlecock.x <= player1.x + player1.width and player1.y <= shuttlecock.y <= player1.y + player1.height):
                shuttlecock.speed_x *= -1
            if (shuttlecock.x >= player2.x and player2.y <= shuttlecock.y <= player2.y + player2.height):
                shuttlecock.speed_x *= -1

            if shuttlecock.x <= 0:
                player2_score += 1
                if player2_score >= 3:
                    winner = "Player 2 Wins!"
                    game_active = False
                else:
                    countdown = True
            elif shuttlecock.x >= SCREEN_WIDTH:
                player1_score += 1
                if player1_score >= 3:
                    winner = "Player 1 Wins!"
                    game_active = False
                else:
                    countdown = True

            screen.fill(WHITE)
            player1.draw(screen)
            player2.draw(screen)
            shuttlecock.draw(screen)
            font = pygame.font.SysFont(None, 48)
            score_surface = font.render(f"Player 1: {player1_score}  Player 2: {player2_score}", True, BLACK)
            screen.blit(score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, 20))
        else:
            screen.fill(WHITE)
            font = pygame.font.SysFont(None, 48)
            title_surface = font.render("Stickman Badminton", True, FONT_COLOR)
            screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
            start_1p_button.draw(screen)
            start_2p_button.draw(screen)
            exit_button.draw(screen)
            if winner:
                winner_font = pygame.font.SysFont(None, 36)
                winner_surface = winner_font.render(winner, True, FONT_COLOR)
                screen.blit(winner_surface, (SCREEN_WIDTH // 2 - winner_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 150))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()