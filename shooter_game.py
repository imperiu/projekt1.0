#Создай собственный Шутер!

from pygame import *
from random import randint

lost = 0
score = 0
HP = 2000000

font.init()
font2 = font.Font(None, 36)

window_width = 700
window_height = 500
window = display.set_mode((window_width,window_height))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'),(window_width,window_height))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

font.init()
font2 = font.Font(None,36)

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed,size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global score
        global HP

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > -2:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 654:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx, self.rect.top, -15, 20, 15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

rocket = Player('rocket.png',100, 427, 4,74,70)
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(6):
    monster = Enemy('ufo.png', randint(0,600), 0, randint(1,3),100, 50)
    monsters.add(monster)
for i in range(1):
    asteroid = Enemy("asteroid.png", randint(0,600), 0, randint(1,3), 100,50)
    asteroids.add(asteroid)

finak = True
game = True
clock = time.Clock()
FPS = 60
while game:
    if finak == True:
        window.blit(background,(0,0))
        text_lose = font2.render("Пропущено:" + str(lost),1 , (255, 255, 255))
        window.blit(text_lose, (10,50))
        text = font2.render("Счет:" + str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        text_HP = font2.render("Прочность:" + str(HP),1, (255,0,0))
        window.blit(text_HP, (10,80))
        rocket.update()
        rocket.reset()
        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        if HP == 0 or lost == 10:
            textlose = font2.render("!!YOU LOSE!!", 1 , (255, 20, 20))
            window.blit(textlose, (250, 250))
            finak = False
        if sprite.spritecollide(rocket, monsters, False) :
            sprite.spritecollide(rocket, monsters, False)
            npc.rect.y = 0
            npc.rect.x = randint(0,500)
            npc.speed = randint(1,3)
            HP = HP - 1
            

        if sprite.spritecollide(rocket, asteroids, False) :
            vc.rect.y = 0
            vc.rect.x = randint(0,500)
            vc.speed = randint(1,3)
            HP = HP - 1

        if score == 20:
            textwin = font2.render("!!YOU WIN!!", 1 , (20, 255, 20))
            window.blit(textwin, (250, 250))
            finak = False

        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(0,600), 0, randint(1,3),100, 50)
            monsters.add(monster)

        for npc in monsters:
            npc.update()
            npc.reset()
            if npc.rect.y >= 500:
                npc.rect.y = 0
                npc.rect.x = randint(0,500)
                npc.speed = randint(1,3)
                lost = lost + 1
        for vc in asteroids:
            vc.update()
            vc.reset()
            if vc.rect.y >= 500:
                vc.rect.y = 0
                vc.rect.x = randint(0,500)
                vc.speed = randint(1,3)
    for e in event.get():
        if e.type == QUIT:
            game = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
                fire_sound.play()

    display.update()
    clock.tick(FPS)