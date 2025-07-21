import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import *


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        #self.screen = pygame.display.set_mode(RES)
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.game_active = False

        #添加play按钮
        self.play_button = Button(self,"play")


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        """玩家点击这个键的时候开始游戏"""
        botton_checked = self.play_button.rect.collidepoint(mouse_pos)
        if botton_checked and not self.game_active:
            #重置玩家生命
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.game_active = True


            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship._center_ship()

            pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()            

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        #检查是否有子弹击中了外星人，若是就删除那个外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,True
        )       #这里的两个实参true会同时删掉外星人和子弹

        # 删除现有的舰队并创建一个新的
        if not self.aliens:
            self.bullets.empty()        #这个方法会删掉全部的子弹
            self._create_fleet()
            self.settings.increase_speed()


    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        #检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):#这个同样检测碰撞，但是是检测
            print("hit")
            self._ship_hit()

        #外星人和边缘的碰撞
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)         #创建一个起始外星人
        alien_width, alien_height = alien.rect.size     #根据这个外星人判定的大小得到这个外星人的位置信息

        current_x, current_y = alien_width, alien_height        #克隆一份作为遍历变量
        while current_y < (self.settings.screen_height - 10 * alien_height):    #若当前的位置以下还能塞10个外星人
            while current_x < (self.settings.screen_width - 2 * alien_width):   #若当前的位置以右还能塞2个外星人
                self._create_alien(current_x, current_y)        #在这块塞一个外星人
                current_x += 2 * alien_width        #改位置，下一个外星人与这个外星人中间隔一个外星人的大小

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width     #当我完成了一行的外星人放置后，重置行的位置
            current_y += 2 * alien_height       #在下一列放置新的外星人

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)     #创建外星人，根据传入的位置创建
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():     #调用检查边缘方法，看看有没有抵达边缘
                self._change_fleet_direction()      #如果抵达边缘了就用这个方法修改方向
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens:#.sprites():     #前面的地方我们直接for in self.aliens，但是实际上他还是调用这个方法，一样的
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)        #屏幕背景
        for bullet in self.bullets.sprites():       #渲染每个子弹
            bullet.draw_bullet()        #画出来
        self.ship.blitme()      #画船
        self.aliens.draw(self.screen)       #画外星人

        if not self.game_active :
            self.play_button.draw_button()

        pygame.display.flip()

    def _ship_hit(self):
        """响应外星人对飞船的碰撞"""
        if self.stats.ship_left > 0:
            #飞船生命-1
            self.stats.ship_left -= 1

            #清屏
            self.bullets.empty()
            self.aliens.empty()

            #创建新的舰队
            self._create_fleet()
            self.ship._center_ship()

            #暂停
            sleep(0.5)

        else :
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """检查有无外星人抵达下边缘"""
        for aline in self.aliens.sprites():
            if aline.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()