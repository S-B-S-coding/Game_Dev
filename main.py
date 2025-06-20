import pygame as pg
from settings import *
import random as rand
import pytmx
from levels import *
from sprites import *
from camera import Camera

class Game:
     def __init__(self):
          pg.init()
          pg.mixer.init()

          self.starting = True
          self.ending = False
          # pg.mixer.music.load("/Users/244096/Desktop/Game_Dev/relaxing-guitar-loop-v7-250408.mp3")
          # pg.mixer.music.play()
          self.screen = pg.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
          self.clock = pg.time.Clock()
          self.balance = 0
          self.best_time = 0
          self.best_time_millisec = 0
          self.best_time_sec = 0
          self.best_time_min = 0
          self.mouse_pos = pg.mouse.get_pos()

          self.side_weapon = "None"

          self.kill_count = 0

          self.current_gun = "Gun 1"

          self.player_interacting = False

          self.running = True

          
     def new(self):
          '''create all game objects, sprites, and groups"
          call run() method'''
          self.map = pytmx.load_pygame("/Users/244096/Desktop/Game_Dev/Levels/tiny-town.tmx")
          self.bullet_img_up = pg.image.load("/Users/244096/Desktop/Game_Dev/bullet.png")
          self.bullet_img_down = pg.transform.rotate(self.bullet_img_up, 180)
          self.bullet_img_left = pg.transform.rotate(self.bullet_img_up, 90)
          self.bullet_img_right = pg.transform.rotate(self.bullet_img_up, -90)

          self.enemies = pg.sprite.Group()
          self.all_sprites = pg.sprite.Group()
          self.collidables = pg.sprite.Group()
          self.coins = pg.sprite.Group()
          self.bullets = pg.sprite.Group()
          self.enemy_walls = pg.sprite.Group()
          self.npcs = pg.sprite.Group()
          self.safety = pg.sprite.Group()
          self.gems = pg.sprite.Group()
          
          
          self.score = 0


          font = pg.font.SysFont('Times New Roman', 50, True, True)
          self.score_text = font.render(f"Score: {self.score}", True, WHITE)
          self.screen.blit(self.score_text, (VIEW_WIDTH/2, 0))

          self.pov = Camera(DISPLAY_WIDTH, DISPLAY_HEIGHT)
          
          
          # drawing all objects from tiled
          for layer in self.map.visible_layers:
               if isinstance(layer, pytmx.TiledTileLayer):
                    # print(dir(layer))
                    # break
                    for x, y, surf in layer.tiles():
                         pos = (x*TILE_SIZE, y*TILE_SIZE)
                         surf = pg.transform.scale(surf, (TILE_SIZE, TILE_SIZE))
                         Tiled_Map(pos, surf, self.all_sprites)

               elif isinstance(layer, pytmx.TiledObjectGroup):
                    # print(layer.name)
                    for obj in layer:
                         # print(dir(layer))
                         if obj.name == 'Player':
                              # print(obj.name)
                              self.player = Player(obj.image, obj.x * 2, obj.y * 2, self, [self.all_sprites])
                              
                         if obj.name == 'Enemy':
                              # print(obj.name)
                              self.enemy = Enemy(obj.image, obj.x * 2, obj.y * 2, self, [self.all_sprites, self.enemies])
                              self.enemy_img = obj.image
                         
                         if obj.name == 'Building' or obj.name == 'Fence' or obj.name == 'Trees' or obj.name == 'Wall':
                              self.collidable = Collidables(obj.image, obj.x * 2, obj.y * 2, obj.width *2, obj.height * 2, [self.collidables])
                         if obj.name == 'Coin' or self.player.coin_hit == True:
                              for i in range(3):
                                   rand_x = rand.randrange(int((DISPLAY_WIDTH/3) +20), int(DISPLAY_WIDTH-64))
                                   rand_y = rand.randrange(32, (DISPLAY_HEIGHT - 64))
                                   self.coin = Coin(obj.image, rand_x, rand_y, self, [self.all_sprites, self.coins])
                              for i in range(3):
                                   rand_x2 = rand.randrange(32, int(DISPLAY_WIDTH-64))
                                   rand_y2 = rand.randrange(int(DISPLAY_HEIGHT*(2/3)), DISPLAY_HEIGHT-64)
                                   self.coins2 = Coin(obj.image, rand_x2, rand_y2, self, [self.all_sprites, self.coins])
                              self.coin_image = obj.image
                              self.coin_x = obj.x * 2
                              self.coin_y = obj.y * 2
                         if obj.name == 'Enemy_Wall':
                              Enemy_Wall(obj.image, obj.x * 2, obj.y * 2, obj.width *2, obj.height * 2, [self.enemy_walls])
                         if obj.name == 'NPC':
                              self.npc = NPC(obj.image, obj.x * 2, obj.y * 2, self, [self.all_sprites, self.npcs])
                         if obj.name == 'Safety':
                              Safety(obj.image, obj.x * 2, obj.y * 2, obj.width * 2, obj.height * 2, [self.safety])
                         if obj.name == 'Gem':
                              self.gem_img = obj.image
                         if obj.name == 'Trap':
                              self.trap_img = obj.image


          

          self.run()
          

     def update(self):
          '''run all updates'''
          self.pov.update(self.player)
          self.all_sprites.update()
          

          if self.player.coin_hit == True:
               rand_x = rand.randrange(int(DISPLAY_WIDTH/3), int(DISPLAY_WIDTH-64))
               rand_y = rand.randrange(32, (DISPLAY_HEIGHT - 64))
               Coin(self.coin_image, rand_x, rand_y, self, [self.all_sprites, self.coins])
               self.player.coin_hit = False

          if self.kill_count >= 5:
               rand_x = rand.randrange(int((DISPLAY_WIDTH/3) +20), int(DISPLAY_WIDTH-64))
               rand_y = rand.randrange(32, (DISPLAY_HEIGHT - 64))
               Enemy(self.enemy_img, rand_x, rand_y, self, [self.all_sprites, self.enemies])
               self.kill_count = 0

     def draw(self):
          '''fill the screen, draw the objects, and flip'''
          self.all_sprites.draw(self.screen)
          for sprite in self.all_sprites:
               self.screen.blit(sprite.image, self.pov.get_view(sprite))
          
          # blit time survived to screen
          self.time = pg.time.get_ticks()
          self.time_millisec = self.time
          self.time_sec = int(self.time_millisec) // 1000
          self.time_min = self.time_sec // 60
          
          font = pg.font.SysFont("Times New Roman", 20, False, False)
          if self.time_sec <= 60:
               time_text = font.render(f"Time: {self.time_sec}.{self.time_millisec-(self.time_sec*1000)}", True, WHITE)
          elif self.time_sec > 60:
               time_text = font.render(f"Time: {self.time_min}:{self.time_sec-(self.time_min * 60)}:{self.time_millisec-(self.time_sec*1000)}", True, WHITE)
          time_text_rect = time_text.get_rect(center = (VIEW_WIDTH // 2, 20))
          self.screen.blit(time_text, time_text_rect)

          # blit current coin balance to screen
          balance_text = font.render(f"{self.balance}", True, WHITE)
          balance_text_rect = balance_text.get_rect(center = (VIEW_WIDTH - 20, 20))
          self.screen.blit(balance_text, balance_text_rect)
          coin_img_rect = self.coin_image.get_rect(center = (VIEW_WIDTH - 40, 20))
          self.screen.blit(self.coin_image, coin_img_rect)

          if self.player_interacting == True:
               self.npc_menu()

          pg.display.flip()

     def events(self): 
          '''game loop events'''
          for event in pg.event.get():
               # events to end the game
               if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    if self.playing:
                         self.playing = False
                         self.running = False

               if event.type == pg.KEYDOWN:
                    # using weapon
                    if event.key == pg.K_SPACE and self.starting == False:     
                         bulletx = self.player.rect.centerx
                         bullety = self.player.rect.centery
                         # firing bullet of gun 1
                         if self.current_gun == "Gun 1":
                              if self.player.dir == "up":
                                   self.bullet = Bullet(self.screen, bulletx, bullety, self.bullet_img_up, self.player.dir, self, [self.bullets, self.all_sprites])
                              elif self.player.dir == "down":
                                   self.bullet = Bullet(self.screen, bulletx, bullety, self.bullet_img_down, self.player.dir, self, [self.bullets, self.all_sprites])
                              elif self.player.dir == "left":
                                   self.bullet = Bullet(self.screen, bulletx, bullety, self.bullet_img_left, self.player.dir, self, [self.bullets, self.all_sprites])
                              elif self.player.dir == "right":
                                   self.bullet = Bullet(self.screen, bulletx, bullety, self.bullet_img_right, self.player.dir, self, [self.bullets, self.all_sprites])
                         # shooting Fireball
                         elif self.current_gun == "Fireball":
                              if self.player.dir == "up":
                                   self.bullet = Fireball(self.screen, bulletx, bullety, self.bullet_img_up, self.player.dir, self, [self.bullets, self.all_sprites])
                              elif self.player.dir == "down":
                                   self.bullet = Fireball(self.screen, bulletx, bullety, self.bullet_img_down, self.player.dir, self, [self.bullets, self.all_sprites])
                              elif self.player.dir == "left":
                                   self.bullet = Fireball(self.screen, bulletx, bullety, self.bullet_img_left, self.player.dir, self, [self.bullets, self.all_sprites])
                              elif self.player.dir == "right":
                                   self.bullet = Fireball(self.screen, bulletx, bullety, self.bullet_img_right, self.player.dir, self, [self.bullets, self.all_sprites])
                    
                    # using traps if they've been purchased
                    if event.key == pg.K_b or event.key == pg.K_e and self.starting == False:     
                         bulletx = self.player.rect.centerx
                         bullety = self.player.rect.centery
                         # leaving traps
                         if self.side_weapon == "TRAPS":
                              self.bullet = Traps(self.screen, bulletx, bullety, self.trap_img, self.player.dir, self, [self.bullets, self.all_sprites])


                    # opening and closing npc menu
                    if self.player.interact == True and event.key == pg.K_e:
                         self.player_interacting = True
                    if event.key == pg.K_q:
                         self.player_interacting = False
               
               # button interact for NPC purchases
               if self.player_interacting == True and event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_pos = pg.mouse.get_pos()
                    if self.mouse_pos[1] >= ((2/3) * VIEW_HEIGHT) and self.mouse_pos[1] <= (((2/3) * VIEW_HEIGHT)+100):
                         if self.mouse_pos[0] >= 100 and self.mouse_pos[0] <= 200  and self.balance >= 100:
                              self.side_weapon = "TRAPS"
                              self.balance -= 100
                         # elif self.mouse_pos[0] >= 300 and self.mouse_pos[0] <= 400:
                         #      self.current_gun = "Gun 3"
                         elif self.mouse_pos[0] >= 500 and self.mouse_pos[0] <= 600 and self.balance >= 200:
                              self.current_gun = "Fireball"
                              self.balance -= 200

                         
     def run(self):
          '''contains the main game loop'''
          self.playing = True
          self.ending = False
          while self.playing and self.ending == False:
               
               self.show_start_screen()
               self.clock.tick(FPS)
               self.update()
               self.events()
               self.draw()
               
               self.game_over_screen()

     # screen which shows only when game begins
     def show_start_screen(self):
          '''the screen to start the game'''
          if self.starting == True:
               self.screen = pg.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
               font = pg.font.SysFont("Times New Roman", 50, False, False)
               start_text = font.render("Click or tap the space bar to start", True, WHITE)
               start_text_rect = start_text.get_rect(center = (VIEW_WIDTH // 2, VIEW_HEIGHT // 2))
               self.screen.fill(BLACK)
               
          while self.starting == True:
               self.screen.blit(start_text, start_text_rect)
               pg.display.flip()

               for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                         if event.key == pg.K_SPACE:
                              self.starting = False
                    elif event.type == pg.MOUSEBUTTONDOWN:
                         self.starting = False
                    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                         if self.playing:
                              self.playing = False
                              self.running = False

     # NPC interact menu for purchases
     def npc_menu(self):
          # menu background/screen
          pg.draw.rect(self.screen, GREY, [(0, VIEW_HEIGHT//2), (VIEW_WIDTH, VIEW_HEIGHT)])
          menu_font = pg.font.SysFont("Times New Roman", 20, False, False)
          menu_text = menu_font.render("Press q to exit", True, WHITE)
          self.screen.blit(menu_text, (0, VIEW_HEIGHT//2))

          # buttons for purchasing from NPC
          pg.draw.rect(self.screen, BLACK, [(100, (2/3) * VIEW_HEIGHT), (100, 100)])
          pg.draw.rect(self.screen, BLACK, [(500, (2/3) * VIEW_HEIGHT), (100, 100)])

          button_font = pg.font.SysFont("Times New Roman", 15, False, False)
          button1_text = button_font.render("TRAPS//100 Coins", True, WHITE)
          button3_text = button_font.render("Fireball//200 Coins", True, WHITE)

          button1_rect = button1_text.get_rect(center = (150, 440))
          button3_rect = button3_text.get_rect(center = (550, 440))

          self.screen.blit(button1_text, button1_rect)
          self.screen.blit(button3_text, button3_rect)
          
     def game_over_screen(self):
          '''the game over screen'''
          if self.ending == True:
               # display game over text
               self.screen = pg.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
               font = pg.font.SysFont("Times New Roman", 50, False, False)
               end_text = font.render("Game Over", True, RED)
               end_text_rect = end_text.get_rect(center = (VIEW_WIDTH // 2, VIEW_HEIGHT // 3))
               
               # show time
               time_font = pg.font.SysFont("Times New Roman", 25, False, False)
               if self.time_sec <= 60:
                    time_text = time_font.render(f"Time: {self.time_sec}.{self.time_millisec-(self.time_sec*1000)} sec/s", True, WHITE)
               elif self.time_sec > 60:
                    time_text = time_font.render(f"Time: {self.time_min}:{self.time_sec-(self.time_min * 60)}:{self.time_millisec-(self.time_sec*1000)} mins", True, WHITE)
               time_text_rect = time_text.get_rect(center = (VIEW_WIDTH // 2, 9*VIEW_HEIGHT//20))
               """
               # find best time from all attempts
               if self.best_time_millisec < self.time_millisec:
                    self.best_time_millisec = self.time_millisec
               if self.best_time_sec < self.time_sec:
                    self.best_time_sec = self.time_sec
               if self.best_time_min < self.time_min:
                    self.best_time_min = self.time_min

               # show best time from all attempts
               if self.best_time_sec <= 60:
                    best_time_text = time_font.render(f"Best Time: {self.best_time_sec}.{self.best_time_millisec-(self.best_time_sec*1000)} sec/s", True, WHITE)
               elif self.best_time_sec > 60:
                    best_time_text = time_font.render(f"Best Time: {self.best_time_min}:{self.best_time_sec-(self.best_time_min * 60)}:{self.best_time_millisec-(self.best_time_sec*1000)} mins", True, WHITE)
               best_time_text_rect = best_time_text.get_rect(center = (VIEW_WIDTH // 2, VIEW_HEIGHT//2))
               
               # explain restart
               # restart_font = pg.font.SysFont("Times New Roman", 25, False, False)
               # restart_text = restart_font.render("Press R to restart", True, WHITE)
               # restart_text_rect = restart_text.get_rect(center = (VIEW_WIDTH // 2, 3*VIEW_HEIGHT//5))
               """
          
               self.screen.fill(BLACK)

          # display ending
          while self.ending == True:
               self.screen.blit(end_text, end_text_rect)
               self.screen.blit(time_text, time_text_rect)
               # self.screen.blit(best_time_text, best_time_text_rect)
               # self.screen.blit(restart_text, restart_text_rect)
               pg.display.flip()

               for event in pg.event.get():

                    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                         if self.playing:
                              self.playing = False
                              self.running = False
                              self.ending = False


##########################################
#### PLAY GAME ####
##########################################

game = Game()

game.show_start_screen()

while game.running:
     game.new()
     game.game_over_screen()

pg.quit()
