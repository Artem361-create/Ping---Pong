from pygame import *
from random import randint
init()
#* GameSprite - основной класс для спрайтов.
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
# *? Player - класс для игрока
class Player(GameSprite):
    def update_left(self):
        if keys_pressed[K_w]  and self.rect.y > 2:
            self.rect.y -= self.speed
        if keys_pressed[K_s]  and self.rect.y < 635:
            self.rect.y += self.speed
    def update_rigth(self):
        if keys_pressed[K_UP]  and self.rect.y > 2:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN]  and self.rect.y < 635:
            self.rect.y += self.speed
class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height, player_speed_y):
        super().__init__(player_image, player_x, player_y, player_speed, width, height)
        self.speed_y = player_speed_y
    def move(self):
        ball_sound = mixer.Sound('ball_saund.ogg')
        ball_sound.set_volume(0.10)
        self.rect.x += self.speed
        self.rect.y += self.speed_y
        if self.rect.colliderect(hero_right):
            self.speed *= -1
            ball_sound.play()
        if self.rect.colliderect(hero_left):
            self.speed *= -1
            ball_sound.play()
        if self.rect.y <0:
            self.speed_y *= -1
        if  self.rect.y > 400 :
            self.speed_y *= -1
window = display.set_mode((700, 500))
display.set_caption('Ping - pong')
background = transform.scale(image.load('sky.jpg'), (700, 500))
hero_left = Player('Left_racket.png', 30, 50, 4, 45, 110)
hero_right = Player('Right_racket.png', 580, 350, 4, 45, 110)
ball = Ball('tennis_ball.png', randint(30, 450), randint(30, 350), 4, 70, 90, 5)
game = True
FPS = 60
clock = time.Clock()
count_right = 0
count_left = 0
loose_font = font.SysFont('Comic Sans MS', 35)
loose = font.SysFont('Comic Sans MS', 45)
text_win_left = loose_font.render('Счёт: ' + str(count_left), 1, (0, 255, 0))
text_win_right = loose_font.render('Счёт: ' + str(count_right), 1, (0, 0, 255))
win_right = loose.render('You lose ', 1, (255, 0, 0))
win_left = loose.render('Player left  win! ', 1, (0, 255, 0))
finish = False
mixer.music.load('BridesBallad.mp3')
mixer.music.set_volume(0.03)
mixer.music.play()
while game == True:
    if finish != True:
        keys_pressed = key.get_pressed()
        window.blit(background, (0, 0))
        hero_left.reset()
        hero_right.reset()
        hero_left.update_left()
        hero_right.update_rigth()
        ball.reset()
        ball.move()
        if ball.rect.x < -70:
            count_right = count_right + 1
            text_win_right = loose_font.render('Счёт: ' + str(count_right), 1, (0, 0, 255))
            ball.rect.x = randint(30, 450)
            ball.rect.y = randint(30, 350)
        if ball.rect.x > 700:
            count_left = count_left + 1
            text_win_left = loose_font.render('Счёт: ' + str(count_left), 1, (0, 255, 0))
            ball.rect.x = randint(30, 450)
            ball.rect.y = randint(30, 350)
        if count_right == 5:
            win_right = loose.render('Player right  win! ', 1, (0, 0, 255))
            window.blit(win_right, (200, 200))
            finish = True
            mixer.music.stop()
        if count_left == 5:
            win_left = loose.render('Player left  win! ', 1, (0, 255, 0))
            window.blit(win_left, (200, 200))
            finish = True
            mixer.music.stop()
    window.blit(text_win_right, (550, 40))
    window.blit(text_win_left, (50, 40))
    for e in event.get():
        if e.type == QUIT:
            game = False
    display.update()
    clock.tick(FPS)