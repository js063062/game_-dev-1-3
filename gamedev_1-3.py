
import pygame
import random
import os

WIDTH = 800
HEIGHT = 600
FPS = 30

#DEFINE COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#CONSTANTS - PHYSICS
PLAYER_ACC = 0.9
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.9
vec = pygame.math.Vector2

#ASSET FOLDERS
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

#DRAW TEXT FUNCTION
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#SHOW START SCREEN FUNCTION
def show_start_screen():

    #screen.blit(background, background_rect)
    screen.fill(BLACK)
    draw_text(screen, "Jarbear 3892!", 63, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys to move, space to jump, 'S' to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin...", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()

    waiting = True
    while waiting:
        clcok.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                print("Key pressed to start game!")
                waiting = False
                
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        player_img=pygame.image.load(os.path.join(img_folder, "p1_jump.png")).convert()
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT  - 10
        self.speedx = 0 #user-built speed var
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
    def update(self):
        self.speedx = 0 #always stationary unless

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_UP]:
            self.rect.y+= -5
        if keystate[pygame.K_DOWN]:
            self.rect.y+= 5
            
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)


            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img 
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
                                            
#PROJECTILE CLASS
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        #ADD LASER IMAGEs
        self.lasers = [
                       pygame.image.load(os.path.join(img_folder, "sprite_0.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "sprite_1.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "sprite_2.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "sprite_3.png")).convert(),
                       pygame.image.load(os.path.join(img_folder, "sprite_4.png")).convert()
                       ]

        self.laser_count = 0

        self.image = self.lasers[self.laser_count]
        self.image = pygame.transform.scale(self.image, (50, 10))
        self.image.set_colorkey(BLACK)

        #ESTABLISH RECT, STARTING POSITION
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.left = x
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx

        #TRANSITION BTW LASER PNGS
        self.image = self.lasers[self.laser_count]
        self.image = pygame.transform.scale(self.image, (50, 10))
        self.image.set_colorkey(BLACK)

        self.laser_count += 1
        if self.laser_count > 5:
            self.laser_count = 0

        #DELETE LASER ONCE OFF SCREEN
        if self.rect.left > WIDTH:
            self.kill()
                       
#INITALIZE VARIABLES
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MY GAME")

clock = pygame.time.Clock()

#ADD BACKGROUND
bkgr_image = pygame.image.load(os.path.join(img_folder, "background.jpg")).convert()
background = pygame.transform.scale(bkgr_image, (WIDTH, HEIGHT))
background_rect = background.get_rect()

#SPRITE GROUPS
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

def newMob():
    robot = Mob()
    all_sprites.add(robot)
    mobs.add(robot)

#newMob()

# GAME LOOP
#   Process Events
#   Update#CHECK FOR MOUSE EVENTS

running = True
while running:

    clock.tick(FPS)

    #PROCESS EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #UPDATE
    all_sprites.update()

    #DRAW
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

        
    #FLIP AFTER DRAWING
    pygame.display.flip()

pygame.quit()
