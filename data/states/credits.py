import copy
import pygame as pg
from .. import tools, setup
from .. import constants as c


class CreditEntry(object):
    """
    The text for each credit for the game.
    게임 엔딩 시 나오는 크레딧 텍스트를 설정할 수 있다.
    """
    def __init__(self, level):#해당 객체에 대한 인스턴스를 생성한다.
        self.alpha = 0
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.credit_sprites = self.make_credits()
        self.index = 0
        self.current_credit = self.credit_sprites[self.index]
        self.state_dict = self.make_state_dict()
        self.state = c.TRANSITION_IN
        self.timer = 0.0
        self.level = level

    def make_credits(self):
        """
        Make a list of lists for all the credit surfaces.
        크레딧 텍스트를 여기서 정할 수 있다.
        """
        credits = [['THE STOLEN CROWN', 'A Fantasy RPG'],
                   ['PROGRAMMING AND GAME DESIGN', 'Justin Armstrong'],
                   ['ART', 'JPhilipp', 
                           'Reemax', 
                           'Lanea Zimmerman', 
                           'Redshrike', 
                           'StumpyStrust', 
                           'Benjamin Larsson', 
                           'russpuppy', 
                           'hc',
                           'Iron Star Media'],
                   ['MUSIC', 'Telaron: The King\'s Theme', 
                             'Mekathratos: Forest Dance (Town Theme)', 
                             'bart: Adventure Begins (Overworld Theme)', 
                             '8th Mode Music: High Action (Battle Theme)', 
                             'Arron Krogh: Coastal Town (Shop Theme)', 
                             'Arron Krogh: My Enemy (Dungeon Theme)', 
                             'Matthew Pablo: Enchanted Festival (Victory Theme)', 
                             'Matthew Pablo: Pleasant Creek (Brother Theme)'],
                   ['SOUND EFFECTS', 'Kenney',
                                     'Nic3_one',
                                     'Ekokubza123',
                                     'kuzyaburst',
                                     'audione'],
                   ['SPECIAL THANKS', '/r/pygame', 
                                      'Leif Theden', 
                                      'Stacey Hunniford']]
        
        credit_sprites = []

        for credit in credits:
            subcredit_list = []
            for i, subcredit in enumerate(credit):
                text_sprite = pg.sprite.Sprite()
                text_sprite.text_image = self.font.render(subcredit, True, c.WHITE)
                text_sprite.rect = text_sprite.text_image.get_rect(centerx = 400,
                                                                   y=100+(i*40))
                text_sprite.image = pg.Surface(text_sprite.rect.size).convert()
                text_sprite.image.set_colorkey(c.BLACK)
                text_sprite.image.set_alpha(self.alpha)
                subcredit_list.append(text_sprite)
            credit_sprites.append(subcredit_list)
        
        return credit_sprites

    def make_state_dict(self):
        """
        Make the dictionary of state methods used to update credit.
        엔딩 크레딧으로 바꾸기 위한 상태를 저장할 딕셔너리를 만든다.
        """
        state_dict = {c.TRANSITION_IN: self.transition_in, 
                      c.TRANSITION_OUT: self.transition_out,
                      c.NORMAL: self.normal_update}

        return state_dict

    def transition_in(self):#엔딩 크레딧이 나올 때 페이드 인 처리를 한다.
        for credit in self.current_credit:
            credit.image = pg.Surface(credit.rect.size).convert()
            credit.image.set_colorkey(c.BLACK)
            credit.image.set_alpha(self.alpha)
            credit.image.blit(credit.text_image, (0, 0))

        self.alpha += 5
        if self.alpha >= 255:
            self.alpha = 255
            self.state = c.NORMAL
            self.timer = self.current_time

    def transition_out(self):#엔딩 크레딧이 나올 때 페이드 아웃 처리를 한다.
        for credit in self.current_credit:
            credit.image = pg.Surface(credit.rect.size).convert()
            credit.image.set_colorkey(c.BLACK)
            credit.image.set_alpha(self.alpha)
            credit.image.blit(credit.text_image, (0, 0))
           
        self.alpha -= 5
        if self.alpha <= 0:
            self.alpha = 0
            if self.index < len(self.credit_sprites) - 1:
                self.index += 1
            else:
                self.level.done = True
                self.level.next = c.MAIN_MENU
            self.current_credit = self.credit_sprites[self.index]
            self.state = c.TRANSITION_IN

    def normal_update(self): #만약 타이머와 현재 시간의 차가 4500이면 상태를 바꾼다.
        if (self.current_time - self.timer) > 4500:
            self.state = c.TRANSITION_OUT

    def update(self, current_time): #장면을 업데이트한다.
        self.current_time = current_time
        update_method = self.state_dict[self.state]
        update_method()

    def draw(self, surface):
        """
        Draw the current credit to main surface.
        메인 표면에 크레딧 화면을 그린다
        """
        for credit_sprite in self.current_credit:
            surface.blit(credit_sprite.image, credit_sprite.rect)


class Credits(tools._State):
    """
    End Credits Scene.
    """
    def __init__(self):#해당 객체에 대한 인스턴스를 생성한다.
        super(Credits, self).__init__()
        self.name = c.CREDITS
        self.music_title = None
        self.previous_music = None
        self.music = None
        self.volume = None
        self.credit = None
    
    def startup(self, current_time, game_data):
        """
        Initialize data at scene start. 
        엔딩 크레딧이 나올 때 데이터를 초기화한다.
        """
        self.game_data = game_data
        self.music = setup.MUSIC['overworld']
        self.volume = 0.4
        self.current_time = current_time
        self.background = pg.Surface(setup.SCREEN_RECT.size)
        self.background.fill(c.BLACK_BLUE)
        self.credit = CreditEntry(self)

    def update(self, surface, keys, current_time):
        """
        Update scene.
        장면을 업데이트한다.
        """
        self.credit.update(current_time)
        self.draw_scene(surface)

    def draw_scene(self, surface):
        """
        Draw all graphics to the window surface..
        엔딩 크레딧을 그린다.
        """
        surface.blit(self.background, (0, 0))
        self.credit.draw(surface)
        
    

