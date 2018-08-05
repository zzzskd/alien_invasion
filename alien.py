import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ 外星人类 """
    
    def __init__(self, ai_settings, screen):
        """ 初始化外星人 """
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        
        # 加载外星人图像，并设置rect属性
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()
        
        # 初始位置为屏幕左上方"附近"
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # 准确位置
        self.x = float(self.rect.x)
        
        
    def blitme(self):
        """ 绘制外星人 """
        self.screen.blit(self.image, self.rect)
    
    def check_edges(self):
        """ 处于边缘则返回True """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        else:
            return False
            
    def update(self):
        """ 右移外星人 """
        self.x += (self.ai_settings.alien_speed_factor *
                        self.ai_settings.fleet_direction)
        self.rect.x = self.x
