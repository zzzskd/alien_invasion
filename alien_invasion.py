import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from ship import Ship
from button import Button
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
    ''' 初始化游戏并创建一个屏幕对象 '''
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    
    # 创建存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    
    # 创建积分牌
    sb = Scoreboard(ai_settings, screen, stats)
    
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    
    # 创建一个用于存储子弹的编组
    bullets = Group()
    
    # 创建一个用于存储外星人的编组
    aliens = Group()
    
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                            aliens, bullets)
        if stats.game_active:
            # 更新ship的位置 
            ship.update()
            # 更新子弹位置
            gf.update_bullets(ai_settings, screen, stats, sb, ship,
                                aliens, bullets)
            # 更新外星人位置 
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, 
                                bullets)
        # 重绘画面
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, 
                            bullets, play_button)
        
run_game()

