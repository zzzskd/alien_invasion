class Settings():
    ''' 储存所有设置的类 '''
    
    def __init__(self):
        ''' 初始化游戏的设置 '''
        
        # 屏幕设置
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        
        # 飞船的设置
        self.ship_limit = 3
        
        # 子弹的设置
        self.bullet_width = 3
        self.bullet_height = 30
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        
        # 外星人的设置
        self.fleet_drop_speed = 10
        
        # 加快游戏的节奏的速度
        self.speedup_scale = 1.1
        # 分数提高的速度
        self.score_scale = 1.5
        
        self.initialize_dynameic_settings()
    def initialize_dynameic_settings(self):
        """ 动态设置　"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 1
        
        # direction = 1 时 右移， direction  = -1 时 左移
        self.fleet_direction = 1
        
        # 计分
        self.alien_points = 50
        
    def increase_speed(self):
        """ 提高速度　"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
