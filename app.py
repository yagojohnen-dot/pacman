import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações de Tela e Grade
TILE_SIZE = 24
MAZE = [
    "----------------------------",
    "|............||............|",
    "|.----.-----.||.-----.----.|",
    "|o|  |.|   |.||.|   |.|  |o|",
    "|.----.-----.||.-----.----.|",
    "|..........................|",
    "|.----.--.--------.--.----.|",
    "|.----.|.|--------.|.|----.|",
    "|......||....||....||......|",
    "------.|.--- || ---.|.------",
    "     |.|.--- || ---.|.|     ",
    "     |.||          ||.|     ",
    "     |.|| ---  --- ||.|     ",
    "------.|| -      - ||.------",
    "      .   -      -   .      ",
    "------.|| -------- ||.------",
    "     |.|| -------- ||.|     ",
    "     |.||          ||.|     ",
    "     |.|| -------- ||.|     ",
    "------.|.--------.|.------",
    "|............||............|",
    "|.----.-----.||.-----.----.|",
    "|o..||.......  .......||..o|",
    "---.||.|.--------.|.||.---",
    "---.||.|.--------.|.||.---",
    "|......||....||....||......|",
    "|.----------.||.----------.|",
    "|..........................|",
    "----------------------------"
]

WIDTH = len(MAZE[0]) * TILE_SIZE
HEIGHT = len(MAZE) * TILE_SIZE

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Python")
CLOCK = pygame.time.Clock()

# Cores (RGB)
BLACK = (0, 0, 0)
BLUE = (25, 25, 166)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.dir_x = 0
        self.dir_y = 0
        self.next_dir_x = 0
        self.next_dir_y = 0
        self.radius = TILE_SIZE // 2 - 2

    def move(self, walls):
        # Tenta mudar de direção se a nova direção não colidir com paredes
        if self.next_dir_x != 0 or self.next_dir_y != 0:
            if not self.check_collision(self.next_dir_x, self.next_dir_y, walls):
                self.dir_x = self.next_dir_x
                self.dir_y = self.next_dir_y

        # Move na direção atual se não houver parede
        if not self.check_collision(self.dir_x, self.dir_y, walls):
            self.x += self.dir_x * self.speed
            self.y += self.dir_y * self.speed

    def check_collision(self, dx, dy, walls):
        next_rect = pygame.Rect(
            self.x + dx * self.speed - self.radius,
            self.y + dy * self.speed - self.radius,
            self.radius * 2,
            self.radius * 2
        )
        for wall in walls:
            if next_rect.colliderect(wall):
                return True
        return False

    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), self.radius)

def build_map():
    walls = []
    dots = []
    power_pellets = []

    for row_idx, row in enumerate(MAZE):
        for col_idx, char in enumerate(row):
            x = col_idx * TILE_SIZE
            y = row_idx * TILE_SIZE
            if char in ["-", "|"]:
                walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif char == ".":
                dots.append(pygame.Rect(x + TILE_SIZE // 2 - 2, y + TILE_SIZE // 2 - 2, 4, 4))
            elif char == "o":
                power_pellets.append(pygame.Rect(x + TILE_SIZE // 2 - 6, y + TILE_SIZE // 2 - 6, 12, 12))

    return walls, dots, power_pellets

def main():
    walls, dots, power_pellets = build_map()
    pacman = Pacman(13.5 * TILE_SIZE, 22.5 * TILE_SIZE)
    score = 0

    running = True
    while running:
        CLOCK.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.next_dir_x, pacman.next_dir_y = 0, -1
                elif event.key == pygame.K_DOWN:
                    pacman.next_dir_x, pacman.next_dir_y = 0, 1
                elif event.key == pygame.K_LEFT:
                    pacman.next_dir_x, pacman.next_dir_y = -1, 0
                elif event.key == pygame.K_RIGHT:
                    pacman.next_dir_x, pacman.next_dir_y = 1, 0

        # Atualizações
        pacman.move(walls)

        # Colisão com bolinhas
        pacman_rect = pygame.Rect(pacman.x - pacman.radius, pacman.y - pacman.radius, pacman.radius * 2, pacman.radius * 2)
        
        for dot in dots[:]:
            if pacman_rect.colliderect(dot):
                dots.remove(dot)
                score += 10

        for pellet in power_pellets[:]:
            if pacman_rect.colliderect(pellet):
                power_pellets.remove(pellet)
                score += 50

        # Renderização
        SCREEN.fill(BLACK)

        for wall in walls:
            pygame.draw.rect(SCREEN, BLUE, wall)

        for dot in dots:
            pygame.draw.rect(SCREEN, WHITE, dot)

        for pellet in power_pellets:
            pygame.draw.ellipse(SCREEN, WHITE, pellet)

        pacman.draw(SCREEN)

        # Mostrar pontuação
        font = pygame.font.SysFont(None, 28)
        score_surface = font.render(f"Score: {score}", True, WHITE)
        SCREEN.blit(score_surface, (10, 5))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
