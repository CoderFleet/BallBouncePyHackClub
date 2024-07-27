import pygame
import math

pygame.init()

screen_width, screen_height = 800, 600
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ball Physics Simulator')

white = (255, 255, 255)
red = (255, 0, 0)

class Ball:
    def __init__(self, start_x, start_y, rad, col):
        self.x = start_x
        self.y = start_y
        self.radius = rad
        self.color = col
        self.vel_x = 0
        self.vel_y = 0
        self.is_dragging = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        if self.is_dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.x, self.y = mouse_x, mouse_y

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            distance = math.hypot(self.x - pygame.mouse.get_pos()[0], self.y - pygame.mouse.get_pos()[1])
            if distance <= self.radius:
                self.is_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False

ball = Ball(screen_width // 2, screen_height // 2, 30, red)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ball.handle_event(event)

    ball.update()

    window.fill(white)
    ball.draw(window)
    pygame.display.flip()

pygame.quit()
