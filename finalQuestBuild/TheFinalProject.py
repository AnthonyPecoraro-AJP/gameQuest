# KidsCanCode - Game Development with Pygame video series
# Sources:
# Code based off of: Shmup game - part(s)1-14 (Chris Bradfield)
# Video link: https://www.youtube.com/watch?v=nGufy7weyGY
# Player sprite and movement
# Code also taken and modified from Mr. Cozort's repository (GitHub)
# https://github.com/ccozort/gameQuest

'''imports'''
import pygame as pg
from pygame.sprite import Sprite
import random
from os import path
from pathlib import Path

# global variables
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Creates file path to "img folder" 
img_folder = Path("img")
bg_img = img_folder / "Background.png"
print(bg_img)

# Game directory: Allows to pull from os files
game_dir = path.join(path.dirname(__file__))
print(game_dir)

# initialize pygame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
# Game Title:
pg.display.set_caption("Eye Blaster!")
clock = pg.time.Clock()

# Game Graphics: 
background_image = pg.image.load(game_dir + "/img/BackgroundV2.png")
background_rect = background_image.get_rect()
background_rect2 = background_image.get_rect()
player_image = pg.image.load(game_dir + "/img/Swordfish.png")
mob_img = pg.image.load(game_dir + "/img/Mob.png")
lazer_image = pg.image.load(game_dir + "/img/Lazer.png")
spit_img = pg.image.load(path.join(game_dir + "/img/spit.png")).convert()
powerup_images = {}
powerup_images['shield'] = pg.image.load(path.join(game_dir + "/img/Shield.png")).convert()
powerup_images['bullet'] = pg.image.load(path.join(game_dir + "/img/Bullet.png")).convert()
player_mini_img = pg.transform.scale(player_image, (25, 19))
# Extra green screen to fix logical issue 
player_mini_img.set_colorkey(GREEN)

# Sets font
font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Draws health
def draw__health(surf, x, y, w):
    outline_rect = pg.Rect(x, y, 100, 20)
    fill_rect = pg.Rect(x, y, w, 20)
    # Fills red and white
    pg.draw.rect(surf, RED, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

# Draws Sheild Bar
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    # Length and height
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    # Fills bar 
    fill = (pct / 100) * BAR_LENGTH
    # Outlines bar
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    # Colors: Yellow (fill) and White (outline)
    pg.draw.rect(surf, YELLOW, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

# Draws lives
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        # Adds (#) of lives to screen 
        img_rect = img.get_rect()
        img_rect.x = x - 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # self.image = pg.Surface((50,40))
        self.image = pg.transform.scale(player_image, (100, 100))
        # Green Screen effect (cuts out green from png img)
        self.image.set_colorkey(GREEN)
        # self.image = player_img
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT -10
        # Player movement
        self.speedx = 0
        # Allows for constant player movement on y axis and controls scrolling background speed
        self.speedy = 15
        # Player health, powerup set, an lives
        self.power = 1
        # Health and total lives
        self.shield = 100
        self.lives = 3
    def update(self):
        # self.speedy = 60
        self.speedx = 0
        # self.speedy = 0
        # KEY BINDS:
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a]:
            self.speedx = -8
        if keystate[pg.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx

        # If this is not commented out this breaks scrolling background
        # # Does this because you don't want to update y speed. 
        # self.rect.y += self.speedy 

    # Taken and modified from Bradfield - power up method
    def powerup(self):
        self.power += 1
        self.power_time = pg.time.get_ticks()
    # Triple bullet powerup
    def pew(self):
        lazer = Lazer(self.rect.centerx, self.rect.top)
        all_sprites.add(lazer)
        lazers.add(lazer)
        # print('trying to shoot..')
        if self.power >= 2:
            # Adds extra lazer on the left side of player
            lazer1 = Lazer(self.rect.left, self.rect.centery)
            # Adds extra lazer on the right side of player
            lazer2 = Lazer(self.rect.right, self.rect.centery)
            # Adds 2 new sprites to group
            all_sprites.add(lazer1)
            all_sprites.add(lazer2)


# POWERUPS!
class Pow(Sprite):
    def __init__(self, center):
        Sprite.__init__(self)
        # Random choice between shield pow an bullet pow
        self.type = random.choice(['shield', 'bullet'])
        # Scaling of powerups
        self.image = pg.transform.scale(powerup_images[self.type], (50, 40))
        
        # Green screen
        self.image.set_colorkey(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = center
        # Powerup fall speed
        self.speedy = 5
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

class Mob(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # self.image = pg.Surface((30,30))
        self.image = pg.transform.scale(mob_img, (50, 40))
        self.image.set_colorkey(GREEN)
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        # Random spawn points:
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(0, 250)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(1, 8)
        # Mob health
        self.hitpoints = 20
    # Mob ability to shoot back at player  
    def pew(self):
        spit = Spit(self.rect.centerx, self.rect.top)
        all_sprites.add(spit)
        spits.add(spit)
        # print('trying to shoot..')
    def update(self):
        # self.health_image = pg.Surface(int(self.hitpoints), int(10))
        # self.health_rect.x = self.x
        # self.health_rect.y = self.y
        self.rect.x += self.speedx
        # Random shooting
        if random.random() > 0.99:
            self.pew()
        # self.rect.y += self.speedy
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speedx*=-1
            self.rect.y += random.randrange(5,25)
        if self.rect.top > HEIGHT + 10:
            self.rect.y = 0
        # Kills mob (erases from memory to minimize lag)
        if self.hitpoints <= 0:
            self.kill()   

class Lazer(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        # Sizeing
        self.image = pg.transform.scale(lazer_image, (25, 20))
        # Green screen
        self.image.set_colorkey(GREEN)
        # self.image = pg.Surface((5,10))
        # self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        # Controls lazer projectile speed
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        # Limits Lag
        if self.rect.y < 0:
            self.kill()
            # print(len(lazers))

# MOB lazers 
class Spit(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        # Scaling
        self.image = pg.transform.scale(spit_img, (25, 20))
        self.image.set_colorkey(GREEN)
        # self.image = pg.Surface((5,10))
        # self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        # Bullet speed (Mob only)
        self.speedy = 8
    # Minimize lag
    def update(self):
        self.rect.y += self.speedy
        if self.rect.y < 0:
            self.kill()
            # print(len(lazers))

# Adds all sprites and entities to sprite groups
all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
lazers = pg.sprite.Group()
spits = pg.sprite.Group()
powerups = pg.sprite.Group()
player = Player()
all_sprites.add(player)
# Makes sure there are always 8 mobs (only if mobs <=0)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# game loop
running = True
while running:
    # do stuff over and over
    clock.tick(FPS)

    for event in pg.event.get():
        # check for window close
        if event.type == pg.QUIT:
            running = False
        # Limits player shoot speed (and sets it up)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.pew()

    # Update the sprites in the game
    all_sprites.update()

    # Checks if mobs run into player 
    hits = pg.sprite.spritecollide(player, mobs, False)

    # If hit by mob, game stops running (aka game over bucko)
    if hits:
        running = False 

    # Checks for collision with player and mob lazers
    hits = pg.sprite.spritecollide(player, spits, False)

    # If player is hit, lower health
    if hits:
        player.shield -= 1

    # Controls powerup spawns
    hits = pg.sprite.groupcollide(mobs, lazers, True, True)
    for hit in hits:
        # When mob killed spawn power up randomly 
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

    # If mob # = 0, spawn more
    if len(mobs) == 0:
        for i in range(8):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

    # check to see if player hit a powerup
    hits = pg.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            # shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'bullet':
            player.powerup()
            # power_sound.play()

    # # Scrolling background
    background_rect2.y = background_rect.y - 600
    background_rect.y+= player.speedy
    background_rect2.y+= player.speedy

    # Resets background (for scrolling)
    if background_rect2.y >- 0:
        background_rect.y = background_rect.y -600

    # Draw or render
    screen.fill(BLUE)
    screen.blit(background_image, background_rect)
    screen.blit(background_image, background_rect2)
    all_sprites.draw(screen)
    # Draws player bar in top left of screen
    draw_shield_bar(screen, 5, 5, player.shield)
    # Draws player lives in top right of screen
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # All sprites are rendered 
    all_sprites.draw(screen)
    # Double buffering method
    pg.display.flip()

pg.quit()