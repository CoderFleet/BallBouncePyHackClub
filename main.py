import pygame
import math
import random

pygame.init()

screen_width, screen_height = 800, 600
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ball Physics Simulator')

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
font = pygame.font.SysFont(None, 36)

class Ball:
    def __init__(self, start_x, start_y, rad, col, elasticity):
        self.x = start_x
        self.y = start_y
        self.radius = rad
        self.color = col
        self.vel_x = 0
        self.vel_y = 0
        self.is_dragging = False
        self.elasticity = elasticity
        self.friction = 0.99
        self.trail = []

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        for point in self.trail:
            pygame.draw.circle(surface, self.color, (int(point[0]), int(point[1])), 2)
        velocity_text = font.render(f"Velocity: {int(math.hypot(self.vel_x, self.vel_y))}", True, black)
        position_text = font.render(f"Position: ({int(self.x)}, {int(self.y)})", True, black)
        elasticity_text = font.render(f"Elasticity: {round(self.elasticity, 2)}", True, black)
        surface.blit(velocity_text, (10, 10))
        surface.blit(position_text, (10, 50))
        surface.blit(elasticity_text, (10, 90))

    def update(self, walls, balls):
        if self.is_dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.x, self.y = mouse_x, mouse_y
            self.radius = 40
        else:
            self.vel_x *= self.friction
            self.vel_y *= self.friction
            self.x += self.vel_x
            self.y += self.vel_y
            self.radius = 30
            self.trail.append((self.x, self.y))
            if len(self.trail) > 20:
                self.trail.pop(0)

            if self.x - self.radius < 0:
                self.x = self.radius
                self.vel_x *= -self.elasticity
                self.change_color()
            elif self.x + self.radius > screen_width:
                self.x = screen_width - self.radius
                self.vel_x *= -self.elasticity
                self.change_color()
            if self.y - self.radius < 0:
                self.y = self.radius
                self.vel_y *= -self.elasticity
                self.change_color()
            elif self.y + self.radius > screen_height:
                self.y = screen_height - self.radius
                self.vel_y *= -self.elasticity
                self.change_color()

            for wall in walls:
                if wall.collide(self.x, self.y, self.radius):
                    if wall.horizontal:
                        if abs(self.y - wall.y) <= self.radius:
                            self.vel_y *= -self.elasticity
                            self.y = wall.y - self.radius if self.vel_y > 0 else wall.y + 10 + self.radius
                            self.change_color()
                    else:
                        if abs(self.x - wall.x) <= self.radius:
                            self.vel_x *= -self.elasticity
                            self.x = wall.x - self.radius if self.vel_x > 0 else wall.x + 10 + self.radius
                            self.change_color()

            for other in balls:
                if other != self and self.check_collision(other):
                    self.resolve_collision(other)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            distance = math.hypot(self.x - pygame.mouse.get_pos()[0], self.y - pygame.mouse.get_pos()[1])
            if distance <= self.radius:
                self.is_dragging = True
                self.vel_x = (self.x - pygame.mouse.get_pos()[0]) * 0.1
                self.vel_y = (self.y - pygame.mouse.get_pos()[1]) * 0.1
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.elasticity = min(1.0, self.elasticity + 0.05)
            elif event.key == pygame.K_DOWN:
                self.elasticity = max(0.0, self.elasticity - 0.05)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.is_dragging:
                new_ball = Ball(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 30, random.choice(colors), self.elasticity)
                balls.append(new_ball)

    def change_color(self):
        self.color = random.choice(colors)

    def check_collision(self, other):
        distance = math.hypot(self.x - other.x, self.y - other.y)
        return distance <= self.radius + other.radius

    def resolve_collision(self, other):
        distance = math.hypot(self.x - other.x, self.y - other.y)
        overlap = 0.5 * (self.radius + other.radius - distance)
        if distance == 0:  # Prevent division by zero
            distance = 1
        self.vel_x, self.vel_y = other.vel_x, other.vel_y
        other.x -= overlap * (self.x - other.x) / distance
        other.y -= overlap * (self.y - other.y) / distance
        self.x += overlap * (self.x - other.x) / distance
        self.y += overlap * (self.y - other.y) / distance
        self.vel_x *= -self.elasticity
        self.vel_y *= -self.elasticity
        other.vel_x *= -other.elasticity
        other.vel_y *= -other.elasticity
        self.change_color()
        other.change_color()

class Wall:
    def __init__(self, x, y, length, horizontal):
        self.x = x
        self.y = y
        self.length = length
        self.horizontal = horizontal

    def draw(self, surface):
        if self.horizontal:
            pygame.draw.rect(surface, black, (self.x, self.y, self.length, 10))
        else:
            pygame.draw.rect(surface, black, (self.x, self.y, 10, self.length))

    def collide(self, bx, by, br):
        if self.horizontal:
            return (self.x <= bx <= self.x + self.length) and (self.y - br <= by <= self.y)
        else:
            return (self.x - br <= bx <= self.x) and (self.y <= by <= self.y + self.length)

ball1 = Ball(screen_width // 2 - 100, screen_height // 2, 30, red, 0.9)
ball2 = Ball(screen_width // 2 + 100, screen_height // 2, 30, red, 0.9)
balls = [ball1, ball2]
walls = [
    Wall(100, 150, 600, True),
    Wall(100, 450, 600, True),
    Wall(100, 150, 10, False),
    Wall(690, 150, 10, False)
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ball1.handle_event(event)
        ball2.handle_event(event)

    ball1.update(walls, balls)
    ball2.update(walls, balls)

    window.fill(white)
    ball1.draw(window)
    ball2.draw(window)
    for wall in walls:
        wall.draw(window)
    pygame.display.flip()

pygame.quit()
