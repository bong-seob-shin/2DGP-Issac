import game_framework
from pico2d import *
import title_state
name = "StartState"
image = None
logo_time = 0.0
BackGround_Width = 1280
BackGround_Height = 960


def enter():
    global image,bgm
    image = load_image('resource/start_state.png')
    bgm = load_music('sound/titleScreenJingle.ogg')
    bgm.set_volume(65)
    bgm.repeat_play()

    pass


def exit():
    global image
    del(image)
    global BackGround_Width, BackGround_Height

    pass


def update():
    global logo_time,bgm
    if (logo_time >1.0):
        logo_time  = 0
        game_framework.change_state(title_state)
    delay(0.01)
    logo_time += 0.01

    pass


def draw():
    global image
    clear_canvas()

    image.draw(BackGround_Width//2, BackGround_Height//2)
    update_canvas()
    pass




def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass




