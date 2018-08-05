import pygame

class Ship():
    ''' 飞船 '''
    
    def __init__(self, ai_settings, screen):
        ''' 初始化飞船并设置其初始位置 '''
        self.screen = screen
        self.ai_settings = ai_settings
        
        # 加载飞船图像
        self.image = pygame.image.load('images/ship.jpg')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # 飞船初始位置为底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # 在飞船的属性center中是储存小数值
        self.center = float(self.rect.centerx)
        
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.fire = False # 可以改进
    
    def update(self):
        ''' 根据标志移动 '''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        
        # 根据self.center 更新 self.rect.centerx, 只取整数部分
        self.rect.centerx = self.center
    
    def is_fire(self): # 待使用部分 按空格可以一直发子弹用 
        if self.fire:
            return True
        else:
            return False
    def blitem(self):
        ''' 指定位置绘制飞船 '''
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """ 飞船被碰撞到后，重新生成飞船并居中 """
        self.center = self.screen_rect.centerx
