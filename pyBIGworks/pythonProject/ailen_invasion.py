import sys
import time

import pygame
from Demos.SystemParametersInfo import new_x
from PIL.ImImagePlugin import number
from fontTools.merge import timer

from settings import Settings
from ship import Ship, Test_ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """"管理游戏行为和资源的类"""
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.setting = Settings()
        if self.setting.fullscreenSetting:
            self.screen =pygame.display.set_mode(
                (0,0),pygame.FULLSCREEN
            )
            self.setting.screen_width = self.screen.get_rect().width
            self.setting.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(
                (self.setting.screen_width,self.setting.screen_height))
        #self.screen = pygame.display.set_mode([1200,800])
        
        pygame.display.set_caption("game0001")

        #self.ship = Ship(self)
        self.ship = Test_ship(self)

        #self.alines = pygame.sprite.Group()
        #self._cearte_fleet()

        self.bullets = pygame.sprite.Group()
        #self.bg_color = (230,230,230)


    def run_game(self):
        while True :
            self._check_events()
            self.ship.update()
            self.bullets.update()
            # for event in pygame.event.get():这部分重构到checkevents里了
            #     if event.type == pygame.QUIT:
            #         sys.exit()

            #pygame.display.set_mode([1200,800]).fill(self.bg_color)
            #被挪到了init里了
            self._update_bullet()
            self._update_screen()
            # self.screen.fill(self.setting.bg_color)这部分就重构到updateScreen里了
            #self.ship.blitem()
            #pygame.display.flip()
            self.clock.tick(60)

    def _check_events(self):
        """"下面这段代码的event对象每次遍历时更新自pygame。event。get以得到每个循环下键的输入
        当pygame。event。get的。type是QUIT时，这对应了用户点击了退出，此时关闭游戏
        当用户输入非退出输入时，检测get的key值，以判断用户输入了什么建，再执行对应的活动"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN :  #get到了一个键被按下
                self._check_keydown_events(event)
                # if event.key == pygame.K_RIGHT :#get说按下的键是右边箭头
                #     #self.ship.rect.x += 1  旧的方式，不能连续移动
                #     self.ship.moving_right = True   #这里是基于ship里给了moveRight的方法，对其他的ship活动需要加方法
                # elif event.key == pygame.K_LEFT :
                #     self.ship.moving_lift = True   #这里不并列if而是elif是因为限制一帧中只能输入一个键

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)#下面的代码被重构到这个方法里了，再增加什么东西只需要更新下面的辅助方法即可
                # if event.key == pygame.K_RIGHT:
                #     self.ship.moving_right = False  #如果松开就会改回去
                # elif event.key == pygame.K_LEFT:
                #     self.ship.moving_lift = False
            # else :这里其实不需要，没有检测到get的键自己就会什么也不做
            #     pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mousedown_events(event)
            else:
                pass
            #elif event.type == pygame.MOUSEBUTTONUP:
            #    self._



    def _check_mousedown_events(self,event) :
        if event.button == 1:
            self._fire_bullet()
        else:
            print("none")



    def _check_keydown_events(self,event):
        if event.key == pygame.K_u:  #这里添加了一个退出的快捷键，由于直接退出了，不需要下面再加对应的快捷键
            sys.exit()
        # elif event.key == pygame.K_SPACE:
        #     self._fire_bullet()

        elif event.key == pygame.K_RIGHT :#get说按下的键是右边箭头
            #self.ship.rect.x += 1  旧的方式，不能连续移动
            self.ship.moving_right = True   #这里是基于ship里给了moveRight的方法，对其他的ship活动需要加方法
        elif event.key == pygame.K_LEFT :
            self.ship.moving_lift = True   #这里不并列if而是elif是因为限制一帧中只能输入一个键
        elif event.key == pygame.K_UP :
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True


    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False  #如果松开就会改回去
        elif event.key == pygame.K_LEFT:
            self.ship.moving_lift = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _update_bullet(self):
        """"更新子弹的位置并删除越界的子弹"""
        self.bullets.update()

        #删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                """在遍历容器时修改其内容可能引发错误，copy() 的作用是创建容器的独立副本，与 range() 的功能完全不同。以下是详细分析：
                
                一、代码逻辑解析
                for bullet in self.bullets.copy():  # 创建 self.bullets 的副本
                    if bullet.rect.bottom <= 0:
                        self.bullets.remove(bullet)  # 操作原容器
                copy() 的作用‌：生成 self.bullets 的独立副本，遍历副本时删除原容器中的元素，避免迭代过程中容器长度变化导致的逻辑错误‌。
                range() 的作用‌：生成整数序列，与容器操作无关（例如 for i in range(5):）‌。
                二、为何必须使用 copy()？
                1. ‌直接遍历原容器的风险‌
                若直接遍历原容器并删除元素：
                for bullet in self.bullets:  # 直接遍历原容器（危险！）
                    if bullet.rect.bottom <= 0:
                        self.bullets.remove(bullet)
                ‌问题‌：删除元素会改变容器长度，导致后续迭代索引错位，可能跳过元素或引发错误"""

    # def _cearte_fleet(self):
    #     """创建外星舰队"""
    #     aline = Alien(self)
    #     #aline_width = aline.rect.width
    #
    #     # current_x = aline_width
    #     # while current_x < (self.setting.screen_width - 2 * aline_width):
    #     #     new_aline = Alien(self)
    #     #     new_aline.x = current_x
    #     #     new_aline.rect.x = new_aline.x
    #     #     self.alines.add(new_aline)
    #     #     current_x += 2 *aline_width
    #     self.alines.add(aline)

    def _update_screen(self):
        self.screen.fill(self.setting.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitem()
        self.alines.draw(self.screen)
        pygame.display.flip()

    def _fire_bullet(self):
        """"创建一颗子弹并将之编入数组bullets"""
        if len(self.bullets) < self.setting.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()