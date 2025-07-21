import pygame
from joblib.disk import delete_folder


class Ship :
    """管理飞船的类"""
    def __init__(self,ai_game):
        """"初始化飞船,并设置位置"""
        self.screen = ai_game.screen
        self.settings = ai_game.setting
        self.screen_rect = ai_game.screen.get_rect()

        #加载飞船对象并获得外接矩形
        self.image = pygame.image.load('images\ceshifeichuan2.bmp')
        self.rect = self.image.get_rect()

        #每个新飞船都在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        #在飞船的属性值里存一个浮点数
        self.x = float(self.rect.x)

        #移动标志，一开始设置为不移动
        self.moving_right = False
        self.moving_lift = False

        #

    def update(self):
        """"根据移动标志调整飞船的位置"""
        #if self.moving_right:  #这里理应是moving——right == Ture，但是注意到，python的if可以判断后面的值是不是真，所以不需要布尔表达式
        if self.moving_right and self.rect.right < self.screen_rect.right:
            #self.rect.x += 1
            self.x += self.settings.ship_speed
        if self.moving_lift and self.rect.left > 0:
            #self.rect.x -= 1
            self.x -= self.settings.ship_speed

        #根据self。x以更新rect对象
        self.rect.x = self.x

    def blitem(self):
        """"在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)

class Test_ship(Ship):
    def __init__(self, ai_game):
        # 在飞船的属性值里存一个浮点数
        super().__init__(ai_game)
        self.y = float(self.rect.y)

        #移动标志，一开始设置为不移动
        self.moving_up = False
        self.moving_down = False

    def  update(self):
        """"根据移动标志调整飞船的位置"""
        #if self.moving_right:  #这里理应是moving——right == Ture，但是注意到，python的if可以判断后面的值是不是真，所以不需要布尔表达式
        if self.moving_right and self.rect.right < self.screen_rect.right:
            #self.rect.x += 1
            self.x += self.settings.ship_speed
        if self.moving_lift and self.rect.left > 0:
            #self.rect.x -= 1
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        #根据self。x以更新rect对象
        self.rect.x = self.x
        self.rect.y = self.y