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
          pg.mixer.music.load("/Users/244096/Desktop/Game_Dev/relaxing-guitar-loop-v7-250408.mp3")
          pg.mixer.music.play()
          self.screen = pg.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
          self.clock = pg.time.Clock()
          self.running = True

          


     def new(self):
          '''create all game objects, sprites, and groups"
          call run() method'''
          self.map = pytmx.load_pygame("/Users/244096/Desktop/Game_Dev/Levels/tiny-town.tmx")
          
          self.enemies = pg.sprite.Group()
          self.all_sprites = pg.sprite.Group()
          self.collidables = pg.sprite.Group()
          self.coins = pg.sprite.Group()
          
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
               
               

               # self.camera.follow()
               # self.camera.update()

               # self.game_viewer.update(self.player)

     
     def draw(self):
          '''fill the screen, draw the objects, and flip'''
          # self.screen.fill(WHITE)

          self.all_sprites.draw(self.screen)

          for sprite in self.all_sprites:
               self.screen.blit(sprite.image, self.pov.get_view(sprite))

          

          pg.display.flip()

     def events(self):
          '''game loop events'''
          for event in pg.event.get():
          # events to end the game
               if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    if self.playing:
                         self.playing = False
                         self.running = False
               

     def run(self):
          '''contains the main game loop'''

          self.playing = True
          while self.playing:
               self.show_start_screen()
               self.clock.tick(FPS)
               self.update()
               self.events()
               self.draw()

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

               


               


     def game_over_screen(self):
          '''the game over screen'''
          pass

##########################################
#### PLAY GAME ####
##########################################

game = Game()

game.show_start_screen()

while game.running:
     game.new()
     game.game_over_screen()

pg.quit()
