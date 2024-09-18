import pygame
import random
import os

# 初始化 Pygame
pygame.init()

# 常量定义
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
TILE_SIZE = 80  # 将图案大小缩小
FPS = 30

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 难度配置
difficulty_settings = {
    "easy": {"tile_count": 18, "time_limit": 120},
    "normal": {"tile_count": 36, "time_limit": 90},
    "difficult": {"tile_count": 48, "time_limit": 60}
}

# 每种图案的重复次数
image_repeats = {
    "easy": 2,
    "normal": 4,
    "difficult": 6
}

# 加载图案并缩放
def load_images():
    images = []
    for i in range(1, 10):  # 假设图片命名为1.png到9.png
        image_path = os.path.join('images', f"{i}.png")
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))  # 缩放图像
        images.append(image)
    return images

# 生成图案
def generate_tiles(images, tile_count, repeats):
    tiles = []
    
    # 确保每种图案至少出现两次
    selected_images = random.sample(images, min(len(images), tile_count // (repeats // 2)))

    for img in selected_images:
        tiles.extend([img] * repeats)  # 确保每种图案出现多次

    # 如果图案数量不足，随机补充
    while len(tiles) < tile_count:
        additional_images = random.choices(images, k=tile_count - len(tiles))
        tiles.extend(additional_images)

    random.shuffle(tiles)
    return tiles[:tile_count]  # 返回指定数量的图案

# 随机位置生成，确保不溢出
def generate_positions(tile_count):
    positions = []
    while len(positions) < tile_count:
        x = random.randint(0, SCREEN_WIDTH - TILE_SIZE)
        y = random.randint(0, SCREEN_HEIGHT - TILE_SIZE)
        pos = (x, y)
        if pos not in positions:  # 确保位置不重复
            positions.append(pos)
    return positions

# 显示主菜单
def main_menu(screen):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    title = font.render("chose difficulty", True, (0, 0, 0))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

    button_font = pygame.font.Font(None, 48)
    easy_button = button_font.render("easy", True, (0, 0, 0))
    normal_button = button_font.render("normal", True, (0, 0, 0))
    difficult_button = button_font.render("difficult", True, (0, 0, 0))

    screen.blit(easy_button, (SCREEN_WIDTH // 2 - easy_button.get_width() // 2, 300))
    screen.blit(normal_button, (SCREEN_WIDTH // 2 - normal_button.get_width() // 2, 400))
    screen.blit(difficult_button, (SCREEN_WIDTH // 2 - difficult_button.get_width() // 2, 500))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                if 300 < mouse_y < 350:  # 简单
                    return "easy"
                elif 400 < mouse_y < 450:  # 普通
                    return "normal"
                elif 500 < mouse_y < 550:  # 困难
                    return "difficult"

# 主游戏函数
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("匹配消除游戏")

    difficulty = main_menu(screen)
    tile_count = difficulty_settings[difficulty]["tile_count"]
    time_left = difficulty_settings[difficulty]["time_limit"]
    repeats = image_repeats[difficulty]  # 获取每种图案的重复次数

    clock = pygame.time.Clock()
    images = load_images()
    tiles = generate_tiles(images, tile_count, repeats)

    # 随机生成位置
    positions = generate_positions(tile_count)

    selected_tiles = []
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    mouse_x, mouse_y = event.pos
                    for i, pos in enumerate(positions):
                        rect = pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
                        if rect.collidepoint(mouse_x, mouse_y) and i not in selected_tiles:
                            selected_tiles.append(i)
                            break  # 点击后停止进一步检查

                    # 检查是否选中两个图案
                    if len(selected_tiles) == 2:
                        if tiles[selected_tiles[0]] == tiles[selected_tiles[1]]:
                            # 消除匹配的图案
                            for index in selected_tiles:
                                tiles[index] = None  # 将匹配的图案设置为None
                        pygame.time.delay(500)  # 等待0.5秒
                        selected_tiles.clear()  # 清空选择

        # 渲染图形
        screen.fill(WHITE)
        for index in range(len(tiles)):
            x, y = positions[index]
            if tiles[index]:  # 只绘制非消除的图案
                screen.blit(tiles[index], (x, y))

        # 更新时间
        time_left -= 1 / FPS
        if time_left <= 0:
            game_over = True

        # 绘制倒计时
        font = pygame.font.Font(None, 48)
        time_text = font.render(f"time last: {int(time_left)}", True, BLACK)
        screen.blit(time_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
