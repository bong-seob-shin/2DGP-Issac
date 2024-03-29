from pico2d import *
import main_state
import game_framework
from Health import  Health
import game_world
import  random
BackGround_Width = 1280
BackGround_Height = 960


PIXEL_PER_METER = (10.0 / 1.5)
RUN_SPEED_KMPH = 1.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH* 1000.0/ 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/ 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
BODYFRAME_PER_ACTION = 8
HEADFRAME_PER_ACTION = 2

class Isaac:

    def __init__(self):
        self.x, self.y = BackGround_Width//2, BackGround_Height//2
        self.frame = 0
        self.image = load_image('resource/isaac_head.png')
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity = RUN_SPEED_PPS
        self.left = 0
        self.body_x, self.body_y = self.x-5, self.y-50
        self.body_frame = 0
        self.body_image = load_image('resource/isaac_body.png')
        self.body_is_move = False
        self.body_bottom = 90
        self.start_health = 3
        self.now_health = 3
        self.health_index = self.start_health-1
        self.heartArray = [Health(60*(i+1)) for i in range(self.start_health)]
        self.is_death = False
        self.hurt_sound1 = load_wav('sound/hurt1.wav')
        self.hurt_sound1.set_volume(32)
        self.hurt_sound2 = load_wav('sound/hurt2.wav')
        self.hurt_sound2.set_volume(32)
        self.hurt_sound3 = load_wav('sound/hurt3.wav')
        self.hurt_sound3.set_volume(32)
        self.health_item_sound = load_wav('sound/heartIntake.wav')
        self.health_item_sound.set_volume(32)
        self.upgradeBullet_item_sound = load_wav('sound/bulletUpgrade.wav')
        self.upgradeBullet_item_sound.set_volume(32)
    def update(self):

        self.frame = (self.frame+ HEADFRAME_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 2
        if self.x > BackGround_Width-180:
            self.x = BackGround_Width-180
        elif self.x < 180:
            self.x = 180
        else:
            self.x += self.velocity_x
        if self.y > BackGround_Height-150:
            self.y = BackGround_Height-150
        elif self.y < 220:
            self.y = 220
        else:
            self.y += self.velocity_y
        if self.body_is_move:
            self.body_frame = (self.body_frame+BODYFRAME_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 8
        if self.body_x > BackGround_Width-185:
            self.body_x = BackGround_Width-185
        elif self.body_x < 175:
            self.body_x = 175
        else:
            self.body_x += self.velocity_x
        if self.body_y > BackGround_Height-200:
            self.body_y = BackGround_Height-200
        elif self.body_y < 170:
            self.body_y = 170
        else:
            self.body_y += self.velocity_y
        if self.now_health < self.start_health:
            if self.start_health-self.now_health <= 1:
                self.heartArray[self.health_index].heart_state = (self.start_health-self.now_health)*2
            elif self.start_health-self.now_health > 1:
                if self.start_health-self.now_health <= 2:
                    self.heartArray[self.health_index].heart_state = 2
                    self.heartArray[self.health_index-1].heart_state =(self.start_health-self.now_health) * 2 - 2
                else:
                    self.heartArray[self.health_index].heart_state = 2
                    self.heartArray[self.health_index-1].heart_state = 2
                    self.heartArray[self.health_index - 2].heart_state = (self.start_health - self.now_health) * 2 - 4
        if self.now_health == self.start_health:
            self.heartArray[self.health_index].heart_state = 0
            self.heartArray[self.health_index-1].heart_state = 0
            self.heartArray[self.health_index-2].heart_state = 0

        if self.now_health <=0:
            self.is_death = True
        if self.is_death:
            self.image = load_image('resource/isaac_death.png')
    def draw(self):
        if self.is_death:
            self.image.draw(self.x,self.y, 150, 60)
        else:
            self.body_image.clip_draw(105 * int(self.body_frame), self.body_bottom, 60, 60, self.body_x, self.body_y)
            self.image.clip_draw(int(self.frame) * 80 + self.left, 0, 80, 80, self.x, self.y)
        for Health in self.heartArray:
            Health.draw()

    def get_bb(self):
        return self.x - 40, self.y -70, self.x + 40, self.y +40

    def body_get_bb(self):
        return self.body_x-30, self.body_y-20, self.body_x+30, self.body_y+20

    def hurt(self):
        hurt_num = random.randint(1,3)
        if hurt_num == 1:
            self.hurt_sound1.play()
        elif hurt_num == 2:
            self.hurt_sound2.play()
        elif hurt_num == 3:
            self.hurt_sound3.play()
        pass

    def eat_health_item(self):
        self.health_item_sound.play()

    def eat_upgrade_bullet_item(self):
        self.upgradeBullet_item_sound.play()
    pass



