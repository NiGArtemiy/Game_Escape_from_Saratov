import pygame
import random
import time

# Инициализация pygame
pygame.init()

# Размеры окна
screen = pygame.display.set_mode((800, 600))

# Название окна
pygame.display.set_caption("Самурай")

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)  # Цвет игрока
GREEN = (0, 255, 0)  # Цвет платформ
RED = (255, 0, 0)  # Цвет врагов

class Player:
    def init(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 50
        self.width = 50
        self.height = 50
        self.jumping = False
        self.y_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -15
        self.rectangle_active = False
        self.rectangle_x = self.x
        self.rectangle_y = self.y
        self.rectangle_width = 100
        self.rectangle_height = 15
        self.rectangle_timer = 0

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        if self.rectangle_active:
            pygame.draw.rect(screen, RED, (self.rectangle_x, self.rectangle_y, self.rectangle_width, self.rectangle_height))

    def update(self):
        if self.jumping:
            self.y_velocity += self.gravity
            self.y += self.y_velocity

            # Проверка коллизии с платформами
            platform_y = check_platform_collision(self.x, self.y)
            if platform_y is not None:
                if self.y + self.height > platform_y:
                    self.y = platform_y - self.height
                    self.jumping = False
                    self.y_velocity = 0

            # Проверка на приземление
            if self.y >= HEIGHT - self.height:
                self.y = HEIGHT - self.height
                self.jumping = False
                self.y_velocity = 0

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.y_velocity = self.jump_strength

    def activate_rectangle(self):
        self.rectangle_active = True
        self.rectangle_x = self.x + self.width // 2
        self.rectangle_y = self.y + self.height // 2
        self.rectangle_timer = time.time()

    def update_rectangle(self):
        if self.rectangle_active:
            if time.time() - self.rectangle_timer > 0.1:
                self.rectangle_active = False

class Enemy:
    def init(self):
        self.x = WIDTH
        self.y = HEIGHT - 150
        self.width = 50
        self.height = 50
        self.speed = random.randint(2, 2)

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    def update(self):
        self.x -= self.speed

class Platform:
    def init(self):
        self.x = WIDTH
        self.y = 500
        self.width = 700
        self.height = 20

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

    def update(self):
        self.x -= 5  # Двигаем платформы влево

def check_platform_collision(x, y):
    for plat in platforms:
        if (plat.x < x < plat.x + plat.width) and (plat.y < y + player.height < plat.y + plat.height):
            return plat.y  # Возвращаем y платформы
    return None  # Если нет коллизий

def check_rectangle_collision(rect_x, rect_y, rect_width, rect_height):
    for enemy in enemies[:]:
        if (enemy.x < rect_x + rect_width and
            enemy.x + enemy.width > rect_x and
            enemy.y < rect_y + rect_height and
            enemy.y + enemy.height > rect_y):
            enemies.remove(enemy)  # Удаляем врага при коллизии

def create_platform():
    platforms.append(Platform())

# Основной цикл игры
clock = pygame.time.Clock()
running = True

# Создаем экземпляры классов
player = Player()
enemies = []
platforms = []
last_spawn_time_enemy = time.time()
last_spawn_time_platform = time.time()

while running:
    screen.fill(WHITE)

    # Обновление и рисование платформ
    for plat in platforms[:]:
        plat.update()
        plat.draw()
        if plat.x < -plat.width:
            platforms.remove(plat)


# Обновление и рисование врагов
    for enemy in enemies[:]:
        enemy.update()
        enemy.draw()
        if enemy.x < -enemy.width:
            enemies.remove(enemy)

    # Обновление и рисование игрока
    player.update()
    player.update_rectangle()
    player.draw()

    # Условие для появления врагов
    if time.time() - last_spawn_time_enemy > 1:
        last_spawn_time_enemy = time.time()
        enemies.append(Enemy())

    # Добавление новых платформ каждые 3 секунды
    if time.time() - last_spawn_time_platform > 3:
        create_platform()
        last_spawn_time_platform = time.time()

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.jump()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                player.activate_rectangle()
                check_rectangle_collision(player.rectangle_x, player.rectangle_y, player.rectangle_width, player.rectangle_height)

    # Получение нажатых клавиш для движения влево и вправо
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 3
    if keys[pygame.K_RIGHT]:
        player.x += 3

    # Ограничение движения по горизонтали, чтобы игрок не выходил за границы экрана
    if player.x < 0:
        player.x = 0
    if player.x > WIDTH - player.width:
        player.x = WIDTH - player.width

    # Обновляем экран
    pygame.display.update()

    # Фреймрейт
    clock.tick(60)

# Завершение
pygame.quit()
