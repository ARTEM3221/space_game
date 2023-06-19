import pygame
import pygame_menu
import math
import os

# Путь к папке с изображениями
image_path = os.path.join(os.getcwd(), "images")

# Размер окна
win_width, win_height = 800, 800

# Класс Planet
class Planet:
    def __init__(self, image, orbit, speed):
        self.image = image
        self.orbit = orbit
        self.speed = speed

# Инициализация pygame
pygame.init()

# Установка размера окна
win = pygame.display.set_mode((win_width, win_height))

# Создание меню
menu = pygame_menu.Menu('Add Planet', win_width, win_height, theme=pygame_menu.themes.THEME_DARK)

# Загрузка изображений
background = pygame.image.load(os.path.join(image_path, "background.jpg"))
sun = pygame.image.load(os.path.join(image_path, "Sun.png"))
moon = pygame.image.load(os.path.join(image_path, "Moon.png"))

# Загрузка изображений планет
planet_images = [
    pygame.image.load(os.path.join(image_path, "Mercury.png")),
    pygame.image.load(os.path.join(image_path, "Venus.png")),
    pygame.image.load(os.path.join(image_path, "Earth.png")),
    pygame.image.load(os.path.join(image_path, "Mars.png")),
    pygame.image.load(os.path.join(image_path, "Jupiter.png")),
    pygame.image.load(os.path.join(image_path, "Saturn.png")),
    pygame.image.load(os.path.join(image_path, "Uranus.png")),
    pygame.image.load(os.path.join(image_path, "Neptune.png")),
]

# Настройка орбит и скоростей планет
orbits = [(i * 70, i * 50) for i in range(1, 9)]
speeds = [1 / 87.97, 1 / 224.7, 1 / 365.2, 1 / 687.7, 1 / 4331, 1 / 10747, 1 / 30589, 1 / 59800]

# Создаем планеты
planets = [Planet(image, orbit, speed) for image, orbit, speed in zip(planet_images, orbits, speeds)]

# Функция для добавления планеты
def add_planet(planet_index):
    planets.append(Planet(planet_images[planet_index], orbits[planet_index], speeds[planet_index]))

for i in range(len(planets)):
    menu.add_button('Add Planet ' + str(i+1), add_planet, i)

# Центр солнца
sun_x, sun_y = win_width // 2, win_height // 2

# Начальный масштаб
scale = 1

# Цикл симуляции
running = True
angle = 0
while running:
    if menu.is_enabled():
        menu.update(pygame.event.get())
        menu.draw(win)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # прокрутка вперед
                    scale += 0.1
                elif event.button == 5:  # прокрутка назад
                    scale -= 0.1
                elif event.button == 3:  # правая кнопка мыши
                    menu.enable()

    win.blit(background, (0, 0))  # Закрашиваем экран фоновым изображением

    # Рисуем солнце
    scaled_sun = pygame.transform.scale(sun, (int(100 * scale), int(100 * scale)))
    win.blit(scaled_sun, (sun_x - scaled_sun.get_width() // 2, sun_y - scaled_sun.get_height() // 2))

    # Рисуем орбиты и планеты
    for planet in planets:
        pygame.draw.ellipse(win, (255, 255, 255), (sun_x - planet.orbit[0] * scale, sun_y - planet.orbit[1] * scale, 2 * planet.orbit[0] * scale, 2 * planet.orbit[1] * scale), 1)
        x = sun_x + math.cos(math.radians(angle * planet.speed)) * planet.orbit[0] * scale
        y = sun_y + math.sin(math.radians(angle * planet.speed)) * planet.orbit[1] * scale
        scaled_planet_image = pygame.transform.scale(planet.image, (int(40 * scale), int(40 * scale)))
        win.blit(scaled_planet_image, (x - scaled_planet_image.get_width() // 2, y - scaled_planet_image.get_height() // 2))

    angle += 1  # Увеличиваем угол

    pygame.display.flip()  # Обновляем экран

pygame.quit()
