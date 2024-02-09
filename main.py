import pygame
import sys
import random

N = 25  # 方块单位值
X, Y = 600, 600  # 窗口范围值（长宽）
L, U = [pygame.K_LEFT, pygame.K_RIGHT], [pygame.K_UP, pygame.K_DOWN]  # 方向值列表（左右，上下）
S = [i for i in range(N, X - N, N)]  # 食物随机位置集合
pygame.init()  # 初始 化
screen = pygame.display.set_mode((X, Y))  # 初始化  窗口
clock = pygame.time.Clock()  # 帧数率


class Snake(object):  # 蛇类
    def __init__(self):
        self.isdead = False  # 默认蛇状态，生存
        self.dir = pygame.K_RIGHT  # 爬行方向，默认向右
        self.body = [pygame.Rect(0, 0, N, N)]  # 蛇身，默认左上角第一格

    def add_node(self):  # 增加方块（蛇首前）
        left, top = self.body[0].left, self.body[0].top  # 蛇首位置
        if self.dir in L:  # 取值
            left += (L.index(self.dir) * 2 - 1) * N
        elif self.dir in U:
            top += (U.index(self.dir) * 2 - 1) * N
        self.body.insert(0, pygame.Rect(left, top, N, N))  # 增加

    def change_dir(self, key):  # 改变方向
        if self.dir in L and key in U:
            self.dir = key
        elif self.dir in U and key in L:
            self.dir = key

    def test_dead(self):  # 死亡，撞墙或撞自己
        left, top = self.body[0].left, self.body[0].top
        if left not in range(0, X, N):
            self.isdead = True
        elif top not in range(0, Y, N):
            self.isdead = True
        elif self.body[0] in self.body[1:]:
            self.isdead = True
        if self.isdead:
            cur_font = pygame.font.SysFont('SimHei', 30)
            text_fmt = cur_font.render("游戏结束!!!", True, (227, 29, 18))
            screen.blit(text_fmt, (2 * X / 5, 2 * Y / 5))


class Food:  # 食物类
    def __init__(self):
        self.body = pygame.Rect(-N, -N, N, N)
        self.body.left = random.choice(S)
        self.body.top = random.choice(S)

    def eaten_body(self):  # 被吃
        self.body.left = random.choice(S)
        self.body.top = random.choice(S)


if __name__ == '__main__':
    snake = Snake()  # 实例化蛇
    food = Food()  # 实例化食物
    while True:
        for i in pygame.event.get():  # 处理事件
            if i.type == pygame.QUIT:  # 窗口×
                sys.exit()
            if i.type == pygame.KEYDOWN:
                snake.change_dir(i.key)  # 改变方向
        screen.fill((255, 255, 255))  # 填充背景
        snake.test_dead()  # 死亡判断
        if not snake.isdead:  # 爬行
            snake.add_node()  # 增加
            snake.body.pop()  # 删除
        if food.body == snake.body[0]:  # 吃食物
            snake.add_node()  # 蛇吃
            food.eaten_body()  # 食物被吃
        pygame.draw.rect(screen, (255, 0, 0), food.body, 0)  # 绘制食物
        for i in snake.body:  # 绘制蛇
            pygame.draw.rect(screen, (20, 220, 39), i, 0)
        pygame.display.update()  # 更新
        clock.tick(8)  # 帧数率