import game_functions as gf
class GameStats():
    """ 记录游戏的统计信息 """
    
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False 
        self.high_score_changed = False
        
        self.get_high_score()
    
    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
    
    def get_high_score(self):
        if gf.get_stored_high_score():
            self.high_score = gf.get_stored_high_score()
        else:
            self.high_score = 0
            gf.store_high_score(self.high_score)
                
    def store_high_score(self):
        if self.high_score_changed:
            gf.store_high_score(self.high_score)
