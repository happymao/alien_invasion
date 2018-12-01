class GameStats():
    ''' recode information of game '''

    def __init__(self, ai_settings):
        ''' initialize game's data '''
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        ''' initialize game's data during play game '''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
