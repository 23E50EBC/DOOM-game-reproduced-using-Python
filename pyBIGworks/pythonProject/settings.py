class Settings :
    """"存设置的类"""
    def __init__(self):
        """"初始化设置"""
        #屏幕设置
        self.fullscreenSetting = False
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,255,255)
        self.bullet_allowed = 3

        #飞船的设置
        self.ship_speed = 10.5

        #子弹的设置
        self.bullet_speed = 10
        self.bullet_width = 3
        self.bullet_height = 20
        self.bullet_color = (60,60,60)
