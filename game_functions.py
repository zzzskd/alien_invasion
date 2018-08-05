import sys
import json
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien

def fire_bullet(ai_settings, screen, ship, bullets):
    """ 发射子弹 """
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
def check_keydown_events(event, ai_settings, screen, stats, ship, bullets):
    ''' 响应按键 '''
    if event.key ==pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    if event.key == pygame.K_q:
        stats.store_high_score()
        sys.exit()

def check_keyup_events(event, ship):
    ''' 响应松开 '''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, 
                    bullets):
    ''' 响应键盘和鼠标事件 '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.store_high_score()
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, bullets)
                
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, 
                                ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
                        aliens, bullets, mouse_x, mouse_y):
    """ 单击Button后开始游戏 """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ａi_settings.initialize_dynameic_settings()
        
        # 隐藏光标
        pygame.mouse.set_visible(False)
        
        # 重置游戏状态
        stats.reset_stats()
        stats.game_active = True
        
        # 重置记分牌
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_score()
        
        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()
        
        # 重新产生外星人群 飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
        play_button):
    ''' 更新屏幕并切换到新屏幕上 '''
    
    screen.fill(ai_settings.bg_color)
    # 绘制子弹 
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 绘制飞机
    ship.blitem()
    
    # 绘制外星人
    aliens.draw(screen) # python自动绘制编组的每个元素
    
    # 显示得分
    sb.show_score()
    
    # 绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    
    # show 
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ 更新子弹位置， 删除以消失的子弹 """
    # 更新
    bullets.update() # 会调用bullet.update()

    # 删除出界子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    # 检测碰撞
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                    aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                    aliens, bullets):
    # 删除相遇的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        # 一颗子弹可能射中多个外星人
        for aliens_tmp in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens_tmp)
            sb.prep_score()
        check_high_score(stats, sb)
        
    # 如果外星人全被击落，则重新生成外星人
    if len(aliens) == 0:
        bullets.empty() # 子弹全部清除
        ai_settings.increase_speed() # 速度加快
        
        # 提高等级
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)

def get_number_alines_x(ai_settings, alien_width):
    """ 计算每行可以容纳多少外星人 """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """ 计算可容纳多少行外星人 """
    available_space_y = (ai_settings.screen_height - (3 * alien_height)
                            - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ 在当前行创建一个外星人 """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def create_fleet(ai_settings, screen, ship, aliens):
    """ 创建外星人群 """
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_alines_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, 
                                    alien.rect.height)
    # 创建外星人群（多行外星人）
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                            row_number)

def check_fleet_edges(ai_settings, aliens):
    """ 外星人到达边缘时采取响应措施 """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break;
    
def change_fleet_direction(ai_settings, aliens):
    """ 外星人群下移， 改变左右移动方向 """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """ 响应飞船被碰到 """
    if stats.ships_left >= 1 :
        stats.ships_left -= 1
        
        aliens.empty()
        bullets.empty()
        
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True) # 显示光标

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """ 检查外星人是否到达屏幕低端 """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >=  screen_rect.bottom:
            # 和飞船被撞一样处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break;

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """ 更新外星人位置 """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # 检测外星人和飞船之间的碰撞
    # spritecollideany 检测一个编组内所有成员和一个精灵是否有碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    
    # 检测外星人是否到达低端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_high_score(stats, sb):
    """ 检测是否诞生最高分 """
    
    if stats.high_score < stats.score:
        stats.high_score = stats.score
        stats.high_score_changed = True
        sb.prep_high_score()

def get_stored_high_score():
    filename = "highscore.json"
    try:
        with open(filename) as fp:
            high_score = json.load(fp)
    except FileNotFoundError:
        return None
    else:
        return int(high_score)

def store_high_score(high_score):
    filename = "highscore.json"
    try:
        with open(filename, 'w') as fp:
            json.dump(str(high_score), fp)
    except:
        print("stored Error")
        return ""
    else:
        return int(high_score)
