import pygame
import random
import math

WIDTH, HEIGHT = 1200, 700
INITIAL_POINT_RADIUS = 5
CLOSE_DISTANCE = 50
INITIAL_POINT_COUNT = 130
BACKGROUND_COLOR = (0, 0, 20)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Плавающие точки")
clock = pygame.time.Clock()

class Point:
    def __init__(self):
        self.x = random.randint(INITIAL_POINT_RADIUS, WIDTH - INITIAL_POINT_RADIUS)
        self.y = random.randint(INITIAL_POINT_RADIUS, HEIGHT - INITIAL_POINT_RADIUS)
        self.radius = INITIAL_POINT_RADIUS
        self.color = self.generate_gradient_color()
        self.speed_x = random.choice([-1, 1]) * random.random() * 2
        self.speed_y = random.choice([-1, 1]) * random.random() * 2

    def generate_gradient_color(self):
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        return (r, g, b)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x < self.radius or self.x > WIDTH - self.radius:
            self.speed_x *= -1
        if self.y < self.radius or self.y > HEIGHT - self.radius:
            self.speed_y *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))

    def update_color(self):
        speed = math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)
        color_intensity = min(255, int(speed * 100))
        self.color = (color_intensity, 255 - color_intensity, 255)

    def update_radius(self, factor):
        self.radius = max(2, self.radius + factor)

def are_close(point1, point2):
    distance = math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)
    return distance < CLOSE_DISTANCE

def draw_line(surface, point1, point2):
    distance = math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)
    line_width = max(1, int(10 - distance / 5))
    pygame.draw.line(surface, (255, 255, 255), (point1.x, point1.y), (point2.x, point2.y), line_width)

def main():
    points = [Point() for _ in range(INITIAL_POINT_COUNT)]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    points.append(Point()) 
                if event.button == 3:
                    points.clear()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        for point in points:
                            point.update_radius(1)
                    elif event.key == pygame.K_DOWN:
                        for point in points:
                            point.update_radius(-1)

        screen.fill(BACKGROUND_COLOR)

        for point in points:
            point.move()
            point.update_color()
            point.draw(screen)

        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                if are_close(points[i], points[j]):
                    draw_line(screen, points[i], points[j])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
