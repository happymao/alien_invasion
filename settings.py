class Settings():
    ''' all module setting is in this class'''

    def __init__(self):
        ''' initialize game setting '''

        # screen setting
        self.screen_width = 1200
        self.screen_height = 640
        self.bg_color = (230, 230, 230)

        # ship setting
        # self.ship_speed_factor = 1.5
        self.ship_limit = 2

        # bullet settings
        # self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 6

        # alien settings
        # self.alien_speed_factor = 1
        self.fleet_drop_speed = 30

        # game rhytem
        self.speedup_scale = 1.1
        # alien point value increase scale
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        ''' initalize variable data '''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # score
        self.alien_points = 50

        # fleet_direction  1 is move to right  -1 is move to left
        self.fleet_direction = 1

    def increase_speed(self):
        ''' speed more quickly '''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)
