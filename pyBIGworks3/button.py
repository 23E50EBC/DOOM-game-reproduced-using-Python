import pygame
from wheel.macosx_libfile import swap32


class Button:
    """创建按钮的类"""

    def __init__(self,ai_game,msg):
        """初始化"""
        self.screen = ai_game.screen    #得到视窗
        self.screen_rect = self.screen.get_rect()

        #尺寸和其他属性
        self.width ,self.height = 200,50    #这句话是按钮的大小
        self.button_color = (0,157,0)   #这句话是按钮的颜色
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)    #这句话是文本的字体
        #创建rect对象并使之居中
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        #按钮的标签只需要创建一次
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        """将文本渲染为图像并居中"""
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        #上句话是用font把文本变成图像，这里的font由init中的参数指明
        self.msg_image_rect = self.msg_image.get_rect() #先得到rect，再指定rect的位置
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """先绘制按钮，再绘制文本"""
        self.screen.fill(self.button_color,self.rect)       #在screen上，rect的位置填充按钮颜色
        self.screen.blit(self.msg_image,self.msg_image_rect)    #screen上，msg-rect的位置上，绘制msg-image