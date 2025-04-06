from pygame import *
from random import randint

class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, player_x, player_y, player_speed, sixe_x = 65, sixe_y = 65):
        
        super().__init__()

        self.image = transform.scale(image.load(player_image), (sixe_x, sixe_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite): #класс для  игрока
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed

class Enemy(GameSprite): #класс для врага

    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 600)
            self.speed = randint(1, 3)
            lost+=1

class Bullet(GameSprite): #класс для пулек
    def update(self):
        self.rect.y -= self.speed




lost = 0 #счетчик пропущенных нлошек
score = 0 #счетчик сбитых нлошек
font.init()
font1 = font.SysFont('Arial', 36)
text_lose = font1.render(
    "Пропущено: " + str(lost), 1, (0, 0, 0)
    )
    
win_width = 800 #ширина экрана
win_height = 490 #высота экрана

window = display.set_mode((win_width, win_height)) #создание игрового окна
display.set_caption('стрелялки') #название для окна
background = transform.scale(image.load("partiya.jpg"), (win_width, win_height)) #подгон заднего фона под размеры экрана
window.blit(background, (0, 0)) #фон на экран

#подключение музыки в игру
mixer.init()
mixer.music.load('redsun.mp3')
#mixer.music.play()

player = Player('chinacat.png', 350, 400, 7) #спрайт игрока
bullets = sprite.Group() #группа для пулек
monsters = sprite.Group() #группа для нлошек
for i in range(3):
    monsters.add(Enemy('burger.png', randint(0, 600), randint(-200, 0), randint(1, 3)))


clock = time.Clock()
FPS = 60


game = True
finish = False

#игровой цикл
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
            
    if finish == False:

        window.blit(background, (0, 0))
   
        player.update() #обновление игрока в игре
        player.reset()

        monsters.draw(window) #обновление нлошек в игре
        monsters.update()

        #чтобы пульки стреляли
        if key.get_pressed()[K_SPACE]:
                bullets.add(Bullet('bullet.png', player.rect.x - 15, player.rect.y, 10, 30, 60))
                timeout = 0
        bullets.update()
        bullets.draw(window)

        if sprite.spritecollide(player, monsters,False) or lost == 3:
            lose = font1.render('ВЫ РАЗОЧАРОВАТЬ ПАРТИЯ КИТАЙ!!! -9999 SOCIAL CREDIT', 610, (0, 238, 255))
            window.blit(lose, (10, 200))
            finish = True

        if score == 10:
            win = font1.render('ВЫ ВЫИГРАТЬ!!! +9999 SOCIAL CREDIT!!!', 60, (0, 255, 149))
            window.blit(win, (200, 200))
            finish = True

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monsters.add(Enemy("burger.png", randint(80, win_width - 80), -40, randint(1, 5)))



        text_lose = font1.render(
        "Пропущено: " + str(lost), 1, (0, 0, 0)
        )
        window.blit(text_lose, (0, 20))

        text_score = font1.render(
        "Счет: " + str(score), 1, (0, 0, 0)
        )
        window.blit(text_score, (0, 60))

    else:
        if key.get_pressed()[K_r]:
            finish = False
            score = 0
            lost = 0

    display.update()
    clock.tick(FPS)