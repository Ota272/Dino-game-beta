import pygame as pg
import random

pg.init()
pg.mixer.init()

width, height=900,450
GREEN = (0, 255, 0)
WHITE = (255,255,255)
win=pg.display.set_mode((width, height))
pg.display.set_caption("Dino game")
MIN_OBSTACLE_GAP = 450

dino_img = pg.image.load('dino.png')
obstacle_img = pg.image.load('cactus.png')
ground_img = pg.image.load('ground.png')
bird_img = pg.image.load('bird.png')


dino_img = pg.transform.scale(dino_img,(60,60))
obstacle_img = pg.transform.scale(obstacle_img,(40,60))
ground_img = pg.transform.scale(ground_img,(width,90))
bird_img = pg.transform.scale(bird_img,(50,40))

obstacle_images = [obstacle_img, bird_img]

try:
    jump_sound = pg.mixer.Sound('jump_sound.wav')
    score_sound = pg.mixer.Sound('score_sound.wav')
except pg.error as e:
    print(f"Ошибка загрузки звука: {e}")
    jump_sound = type('Sound', (object,), {'play': lambda: None})()
    score_sound = type('Sound', (object,), {'play': lambda: None})()

class Dino:
    def __init__(self):
        self.image=dino_img
        self.x = 50
        self.y=height-self.image.get_height()-50
        self.vel_y =0
        self.gravity=1.4
        self.jump_height=-20
        self.is_jumping=False
        self.rect=pg.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())

    def update(self):
        if self.is_jumping:
            self.vel_y += self.gravity
            self.y+=self.vel_y
            if self.y>=height-self.image.get_height()-50:
                self.y = height-self.image.get_height()-50
                self.is_jumping = False
        self.rect.topleft=(self.x,self.y)

    def jump(self):
        if not self.is_jumping:
            self.is_jumping=True
            self.vel_y=self.jump_height
            jump_sound.play()

    def draw(self,win):
        win.blit(self.image,(self.x,self.y))


class Obstacle:
    def __init__(self):
        self.image = random.choice(obstacle_images)
        self.x = width
        self.rect = self.image.get_rect()

        if self.image == bird_img:
            self.y = height - self.image.get_height() - 100 
            self.vel = 15 
        else: 
            self.y = height - self.image.get_height() - 50 
            self.vel = 12 
        
        self.rect.topleft = (self.x, self.y)
        self.passed = False
    def update(self):
        self.x -= self.vel
        if self.x < -self.image.get_width():
            self.x = width
            self.rect.topleft = (self.x, self.y)
            return True 
        
        self.rect.topleft = (self.x, self.y)
        return False 
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))

class Ground:
    def __init__(self):
        self.image = ground_img
        self.x = 0
        self.y = height - 100 
        self.vel = 6
        self.rect = pg.Rect(self.x, self.y, width, 50)

    def update(self):
        self.x -= self.vel
        if self.x <= -width:
            self.x = 0
        self.rect.topleft = (self.x, self.y) 

    def draw(self, win):
        win.blit(self.image, (self.x, self.y)) 
        win.blit(self.image, (self.x + width, self.y)) 
def main():
    clock=pg.time.Clock()
    font=pg.font.Font("PressStart2P-Regular.ttf", 30)

    obstacles = [] 
    
    SPAWN_OBSTACLE = pg.USEREVENT + 1
    pg.time.set_timer(SPAWN_OBSTACLE, 5000)

    run = True
    game_active=False
    initial_start=True

    score=0
    record=0

    while run:
        clock.tick(30)
        win.fill(WHITE)

        bg_color = WHITE
        if score >= 100:
            bg_color = GREEN 
            
        win.fill(bg_color)

        for event in pg.event.get():
            if event.type == SPAWN_OBSTACLE and game_active:
                obstacles.append(Obstacle())
            if event.type==pg.QUIT:
                run=False
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_SPACE:
                    if not game_active:
                        dino=Dino()
                        ground=Ground()
                        obstacles = []
                        score=0
                        game_active=True
                        initial_start=False
                    else:
                        dino.jump()
        if game_active:
            dino.update()
            ground.update()

            for obs in obstacles:
                obs.update()
            
                if not obs.passed and obs.x < dino.x:
                    obs.passed = True
                    score += 1
                    score_sound.play()
                    if score > record:
                        record = score 	

                obstacles = [obs for obs in obstacles if obs.x > -obs.image.get_width()]

                if dino.rect.colliderect(obs.rect):
                    game_active = False

                ground.draw(win)
                dino.draw(win)
                obs.draw(win)
                for obs in obstacles:
                    obs.draw(win)

            score_text=font.render("Score:"+str(score),True,(0,0,0))
            record_text=font.render("Record:"+str(record),True,(0,0,0))

            win.blit(score_text,(10,10))
            win.blit(record_text,(width-290,10))
        else:
            if initial_start:
                start_text=font.render("Too Start Press Space",True,(0,0,0))
                win.blit(start_text,(width//2-start_text.get_width()//2,
                                height//2-start_text.get_height()//2))
            else:
                game_over_text=font.render("Wanna try again?", True,(0,0,0))
                game_over_text2=font.render("Press Space to Start again", True,(0,0,0))
                win.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2,
                                        height // 2 - game_over_text.get_height() // 2))
            
                win.blit(game_over_text2, (width // 2 - game_over_text2.get_width() // 2,
                                        height // 2 - game_over_text.get_height() // 2 + 40)) 
                
        pg.display.update()
    pg.quit()

if __name__=="__main__":
    main()