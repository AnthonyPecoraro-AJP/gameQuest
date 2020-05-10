# ################################################################
# ########  These files were created by: Anthony Pecoraro ########
# ################################################################
# '''
# Sources:
# '''
# # KidsCanCode - Game Development with Pygame video series
# # Shmup game - part 1
# # Video link: https://www.youtube.com/watch?v=nGufy7weyGY
# # Player movement
# # © 2019 KidsCanCode LLC / All rights reserved.
# # https://stackoverflow.com/questions/15463422/pygame-double-jump

# '''
# Week of march 23rd - Lore
# Modularity, Github, import as,

# '''

# # Allows to call upon 'pygame' as 'pg' 
# import pygame as pg
# from pygame.sprite import Sprite 
# import random
# from os import path
# from pathlib import Path 
# # from pg.sprite import Group
# # from pygame.sprite import Group
# # imports all code (*) from sperate files
# from settings import *
# from sprites import *

# img_folder = Path("img")
# bg_img = imgfolder / "bg.png"
# print(bg_img)

# game_dir = path.join(path.dirname(__file__))
# print(game_dir)

# class Game:
#     def __init__(self):
#         # initialize game window, etc
#         pg.init()
#         pg.mixer.init()
#         self.screen = pg.display.set_mode((WIDTH, HEIGHT))
#         pg.display.set_caption(TITLE)
#         self.clock = pg.time.Clock()
#         self.running = True

#         # Loads all game graphics
#         background = pg.image.load(path.join(game_dir + "/img/bg.png")).convert()
#         background_rect = background.get_rect()
#         player_img = pg.image.load(path.join(game_dir + "/img/player.png")).convert()
#         mob_img = pg.image.load(path.join(game_dir + "/img/mob.png")).convert()
#         lazer_img = pg.image.load(path.join(game_dir + "/img/lazer.png")).convert()
#         #####

#     def draw_text(surf, text, size, x, y):
#         font = pg.Font(font_name, size)
#         text_surface = font.render(text, True, WHITE)
#         text_rect = text_surface.get_rect()
#         text_rect.midtop = (x, y)
#         surf.blit(text_surface, text_rect)

#     def draw__health(surf, x, y, w):
#         outline_rect = pg.Rect(x, y, 100, 20)
#         fill rect = pg.Rect(x, y, w, 20)
#         pg.draw.rect(surf, RED, fill_rect)
#         pg.draw.rect(surf, WHITE, outline_rect, 2)


#     def new(self):
#         # start a new game
#         self.all_sprites = Group()
#         # Adds platforms to sprite group
#         self.platforms = pg.sprite.Group()
#         # Adds player and enemies
#         self.player = Player(self)
#         self.all_sprites.add(self.player)
#         # self.enemies = Enemy(self)
#         # self.all_sprites.add(self.enemies)
#         #-----------------------------------#
#         ground = Platform(0, HEIGHT-10, WIDTH, 40)
#         # Creates platform dimensions 
#         plat1 = Platform(200, 400, 150, 20)
#         plat2 = Platform(50, 200, 150, 20)
#         self.all_sprites.add(ground)
#         # Adds all plats to ground group
#         self.platforms.add(ground)
#         # Adds platforms 
#         self.all_sprites.add(plat1)
#         self.platforms.add(plat1)
#         self.all_sprites.add(plat2)
#         self.platforms.add(plat2)
#         self.run()

#     def run(self):
#         # Game Loop
#         self.playing = True
#         while self.playing:
#             self.clock.tick(FPS)
#             self.events()
#             self.update()
#             self.draw()

#     def update(self):
#         # Game Loop - Update
#         self.all_sprites.update()
#         # Checks for player collision with plat bott and top
#         hits = pg.sprite.spritecollide(self.player, self.platforms, False)
#         if hits:
#             if self.player.rect.top > hits[0].rect.top:
#                 # print("I hit my head!")
#                 self.player.vel.y = 0
#                 self.player.rect.top = hits[0].rect.bottom + 1
#             else:
#                 self.player.vel.y = 0
#                 self.player.pos.y = hits[0].rect.top + 1
#                 # self.player.pos.y = hits[0].rect.bottom
#         if self.player.rect.left <= WIDTH / 4:
#             self.player.pos.x += abs(self.player.vel.x)
#         # elif self.player.rect.right <= WIDTH / 4:
#         #     self.player.pos.x += (self.player.vel.x)
#             for plat in self.platforms:
#                 plat.rect.x += abs(self.player.vel.x)
#                 if plat.rect.left >= WIDTH:
#                     plat.kill()

#     def events(self):
#         # Game Loop - events
#         for event in pg.event.get():
#             # check for closing window
#             if event.type == pg.QUIT:
#                 if self.playing:
#                     self.playing = False
#                 self.running = False

#     def draw(self):
#         # Game Loop - draw
#         self.screen.fill(light_sea_green)
#         self.all_sprites.draw(self.screen)
#         # *after* drawing everything, flip the display (double buffering technique)
#         pg.display.flip()

#     def show_start_screen(self):
#         # game splash/start screen
#         pass

#     def show_go_screen(self):
#         # game over/continue
#         pass

# g = Game()
# g.show_start_screen()
# while g.running:
#     g.new()
#     g.show_go_screen()

# pg.quit()