import game_framework
from pico2d import *
import random

import game_world

# Bird Fly Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
FLY_SPEED_KMPH = 35.0  # Km / Hour
FLY_SPEED_PPS = (FLY_SPEED_KMPH * 1000.0 / 3600.0 * PIXEL_PER_METER)
# 10픽셀당 30cm, 새의 속도는 35 km/h이다.
# 여기서 새의 pixel_per_second 를 구한다.(FLY_SPEED_PPS)
# -> 아래의 update()에서 계속

# Bird Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14  # 전체 프레임 수

class Bird:
    image = None

    def __init__(self):
        if Bird.image == None:
            Bird.image = load_image('bird100x100x14.png')

        self.x = random.randint(50, get_canvas_width() - 50)
        self.y = random.randint(200, get_canvas_height() - 50)
        self.dir = random.choice((-1, 1))
        self.velocity = FLY_SPEED_PPS
        self.frame = random.randint(0, 14)

    def update(self):

        # 새의 움직임은 0.5초에 한 번씩으로 초 당 2번의 움직임을 가진다.
        # 달리 말하면 한 프레임 당 (0.5 / 전체 스프라이트 프레임 수)초에 한 장씩 바뀌어야 한다.
        # 아래 식의 결과는 (0.5 / 14)초에 1씩 증가하는 결과를 가져온다.
        self.frame = (self.frame +
                      FRAMES_PER_ACTION *
                      ACTION_PER_TIME *
                      game_framework.frame_time) % FRAMES_PER_ACTION

        # 새의 속도는 미리 구한 PPS와 방향(1, -1), 프레임당 시간의 곱으로 구할 수 있다.
        self.x += self.velocity * game_framework.frame_time * self.dir

        if self.x < 50:
            self.x = 50
            self.dir *= -1
        elif self.x > get_canvas_width() - 50:
            self.x = get_canvas_width() - 50
            self.dir *= -1

    def draw(self):

        # 새의 크기는 기본 크기인 100x100으로 정했다.
        if self.dir == 1:
            Bird.image.clip_draw(
                int(self.frame) * 100, 0, 100, 100,
                self.x, self.y)

        # clip_composite_draw 의 크기는 기본값이 없기 때문에 직접 지정해준다. (100x100)
        elif self.dir == -1:
            Bird.image.clip_composite_draw(
                int(self.frame) * 100, 0, 100, 100,
                0, 'h',
                self.x, self.y, 100, 100)

