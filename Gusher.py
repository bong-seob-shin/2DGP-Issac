from pico2d import *
import random
from BehaviorTree import SelectorNode, SequenceNode, Node, LeafNode, BehaviorTree
import game_framework

BackGround_Width = 1280
BackGround_Height = 960

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 2.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH* 1000.0/ 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/ 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION = 2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Gusher:
    image = None

    def __init__(self):
        if Gusher.image == None:
            Gusher.image = load_image('resource/Gusher_leg.png')
        self.x = random.randint(200, 1000)
        if self.x > (BackGround_Width//2)-80 and self.x < (BackGround_Width//2)+80:
            self.x = self.x - 150
        self.y = random.randint(200, 750)
        if self.y > (BackGround_Height//2)-80 and self.y < (BackGround_Height//2)+80:
            self.y = self.y - 150

        self.dir = 1
        self.timer = 1
        self.health = 3
        self.frame = 0
        self.bottom = 0
        self.build_behavior_tree()
        self.speed = RUN_SPEED_PPS
        self.velocity = self.speed * math.cos(self.dir) * game_framework.frame_time

    def draw(self):
        self.image.clip_draw(int(self.frame) * 83, self.bottom, 80, 60, self.x, self.y)
    def get_bb(self):
        return self.x - 30, self.y -30, self.x + 20, self.y +20

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.velocity = self.speed * math.cos(self.dir) * game_framework.frame_time
        self.x += self.velocity
        self.y += self.velocity
        self.x = clamp(150, self.x, 1280 - 150)
        self.y = clamp(150, self.y, 900 - 150)

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.random()*2*math.pi
            if math.cos(self.dir) > 0:
                self.bottom = 65
            elif math.cos(self.dir)< 0:
                self.bottom = 0
            return BehaviorTree.SUCCESS
        pass

    def build_behavior_tree(self):
        wander_node = LeafNode("Wander", self.wander)
        self.bt = BehaviorTree(wander_node)
        pass

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.bt.run()


    pass
