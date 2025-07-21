class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1400
        self.screen_height = 875
        self.bg_color = (230, 230, 230)

        # Ship settings.
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 5
        self.bullet_width = 3000
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        # Alien settings.
        self.alien_speed = 5.0
        self.fleet_drop_speed = 50
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        #难度系数
        self.speed_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化游戏随进行变化的设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 5
        self.alien_speed = 5

        #
        self.fleet_direction = 1

    def increase_speed(self):
        """提高难度"""
        self.ship_speed *= self.speed_scale
        self.alien_speed *= self.speed_scale
        self.bullet_speed *= self.speed_scale

