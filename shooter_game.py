from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def fire(self):
        bulets = Bullet(img_pantor_h, self.rect.centerx, self.rect.top, 16, 16, 15)
        patrons.add(bulets)
class Player2(GameSprite):
    def update_evil(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def fire(self):
        bulets2 = Bullet(img_pantor_h, self.rect.centerx, self.rect.top, 16, 16, -15)
        patrons2.add(bulets2)
        
class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 700:
            self.kill()


            
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80)
win = font2.render("YOU WIN!!!", True, (0, 0, 255))
lose = font2.render('YOU LOSE', True, (196, 132, 13))


win_width = 700
win_height = 500

img_back = 'back.png'
img_hero = 'hero.png'
img_pantor_h = 'bullet_h.png'
img_pantor_e = 'bullet_e.png'
img_evil = 'evil.png'
score = 0
lost = 0
goal = 30
life = 3
max_lose = 3

window = display.set_mode((win_width, win_height))
display.set_caption('Team game for Relis')

mixer.init()
mixer.music.load('risk.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

window = display.set_mode((win_width, win_height))
backround = transform.scale(image.load(img_back), (win_width, win_height))

player = Player(img_hero, 5, win_height - 100, 50, 100, 10)
evil = Player2(img_evil, 645, win_height - 100, 50, 100, 10)


patrons = sprite.Group()
patrons2 = sprite.Group()
super_finish = False
run = True
FPS = 60
rel_time = False
num_fire = 0

while run:
    for i in event.get():
        if i.type == QUIT:
            run = False

        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not super_finish:
        window.blit(backround, (0, 0))

        text =  font1.render('Score:' + str(lost) + '/30', 1, (0, 0, 0))
        window.blit(text, (10, 20))

        t_lose = font1.render('Wins:' + str(score), 1, (255, 255, 255))
        window.blit(t_lose, (10, 50))


        player.update()
        evil.update_evil()
        patrons.update()
        evil.reset()
        player.reset()


        patrons.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 2:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        #collides = sprite.groupcollide(cops, patrons, True, True)
        #for i in collides:
        #    score += 1
        #    zluka = Enemy(img_cop, randint(80, win_width - 80), -40, 50, 100, randint(5, 15))
        #    cops.add(zluka)

        #if sprite.spritecollide(car, cops, False): #or sprite.spritecollide(car, asteroids, False)
        #    sprite.spritecollide(car, cops, True)
            #sprite.spritecollide(car, asteroids, True)
        #    life -= 1

        if lost >= goal:
            super_finish = True
            window.blit(win, (200, 200))
            score += 1
            

        if life == 0:# or lost >= max_lose:
            super_finish = True
            window.blit(lose, (200, 200))

        if life == 3:
            life_color = (0, 150, 0)

        if life == 2:
            life_color = (150, 150, 0)

        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        

        display.update() 
    else:
        super_finish = False
        #score = 0
        lost = 0
        num_fire = 0
        life = 3
        for i in patrons:
            i.kill()


        time.delay(FPS)

    time.delay(FPS)
                                      



