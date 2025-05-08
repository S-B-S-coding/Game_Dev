import pygame as pg
import math
from settings import *
import random as rand

class Player(pg.sprite.Sprite):
    def __init__(self, img, x, y, game, groups):
        # pass
        super().__init__(groups)
        self.image = pg.transform.scale(img, (TILE_SIZE-1, TILE_SIZE-1))

        self.game = game

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.startx = x
        self.starty = y

        self.x = self.rect.x
        self.y = self.rect.y

        self.x_change = 0
        self.y_change = 0

        self.coin_hit = False

        # create mask for the player
        self.player_mask = pg.mask.from_surface(self.image)
        # self.mask_image = self.player_mask.to_surface() 

        self.velo = 5

    def enemy_collision(self):
        if pg.sprite.spritecollide(self, self.game.enemies, False):
            
            hits = pg.sprite.spritecollide(self, self.game.enemies, False, pg.sprite.collide_mask)

            if hits:
                self.x = self.startx
                self.y = self.starty

    # collision detection with masks
    def collidables_collision(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.collidables, False)
            
            # hits = pg.sprite.spritecollide(self, self.game.collidables, False, pg.sprite.collide_mask)
        # hits = pg.sprite.spritecollide(self, self.game.collidables, False)
            
            # if dir == 'x':
        if hits:
            if self.x_change > 0:
                # self.x_change = 0
                self.x = hits[0].rect.left - self.rect.width# (self.velo + 1)
            elif self.x_change < 0:
                # self.x_change = 0
                self.x = hits[0].rect.right# (self.velo + 1)
            
        # if dir == 'y':
            # if hits:
            if self.y_change > 0:
                # self.y_change = 0
                self.y = hits[0].rect.top - self.rect.height    #(self.velo + 1)
            elif self.y_change < 0:
                # self.y_change = 0
                self.y = hits[0].rect.bottom  #(self.velo + 1)
            self.y_change = 0
            self.rect.y = self.y
            self.x_change = 0
            self.rect.x = self.x

    def coin_collide(self):
        if pg.sprite.spritecollide(self, self.game.coins, False):
            
            hits = pg.sprite.spritecollide(self, self.game.coins, True, pg.sprite.collide_mask)
            if hits:
                self.coin_hit = True


    def get_keys(self):
        

        # list of key presses
        keys = pg.key.get_pressed()

        # set velo based on key presses
        if keys[pg.K_LEFT]:
            self.now = pg.time.get_ticks()

            self.x_change = -1 * self.velo

        elif keys[pg.K_RIGHT]:
            self.now = pg.time.get_ticks()
            
            self.x_change = self.velo
        
        else:
            self.x_change = 0

        if keys[pg.K_UP]:
            self.now = pg.time.get_ticks()
            
            self.y_change = -1 * self.velo

        elif keys[pg.K_DOWN]:
            self.now = pg.time.get_ticks()
            
            self.y_change = self.velo

        else:
            self.y_change = 0
            

        if keys[pg.K_LEFT] and keys[pg.K_RIGHT]:
            self.x_change = 0
        if keys[pg.K_UP] and keys[pg.K_DOWN]:
            self.y_change = 0

        

        if self.rect.y <= 0:
            self.y_change = 0
            self.y += 0.65
        elif (self.rect.y + self.rect.height) >= DISPLAY_HEIGHT:
            self.y_change = 0
            self.y -= 0.65
        if self.rect.x <= 0:
            self.x_change = 0
            self.x += 0.65
        elif (self.rect.x + self.rect.width) >= DISPLAY_WIDTH:
            self.x_change = 0
            self.x -= 0.65


        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.player_mask = pg.mask.from_surface(self.image)
        self.mask_image = self.player_mask.to_surface()

    # def collision(self):
        
    def update(self):
        self.get_keys()

        # update player location
        self.x += self.x_change
        self.y += self.y_change

        
        self.enemy_collision()

        self.coin_collide()
        self.collidables_collision('y')
        
        self.rect.x = self.x
        # self.collidables_collision('x')
        self.rect.y = self.y
        

        

    
    


class Enemy(pg.sprite.Sprite):
    def __init__(self, img, x, y, game, groups):
        # pass
        super().__init__(groups)

        self.image = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        
        self.speed = 2

        self.game = game

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.enemy_mask = pg.mask.from_surface(self.image)

    def follow_player(self):
        self.distance_to_playerx = self.game.player.rect.x - self.rect.x
        self.distance_to_playery = self.game.player.rect.y - self.rect.y
        # find driection vectro (dx, dy) between enemy and player
        self.dirvect = pg.math.Vector2(self.distance_to_playerx, self.distance_to_playery)
        self.dirvect.normalize()
        # Move along normalized vector towards the player at current speed
        self.dirvect.scale_to_length(self.speed)
        self.rect.move_ip(self.dirvect)

    def collidables_collision(self):  
        hits = pg.sprite.spritecollide(self, self.game.collidables, False)
        collide_r = False
        collide_l = False
        if hits:
            if self.rect.right >= self.game.collidable.rect.left:
                collide_r = True
            elif self.rect.left <= self.game.collidable.rect.right:
                collide_l = True
            if self.rect.top <= self.game.collidable.rect.bottom:
                self.rect.y += 10
            elif self.rect.bottom >= self.game.collidable.rect.top:
                self.rect.y -= 10
        if collide_r:
            self.rect.x -= 10
        elif collide_l:
            self.rect.x += 10

                
    
    def update(self):
        self.follow_player()
        self.collidables_collision()



class Collidables(pg.sprite.Sprite):
    def __init__(self, img, x, y, width, height, groups):
        super().__init__(groups)
        self.image = pg.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.collidable_mask = pg.mask.from_surface(self.image)

class Coin(pg.sprite.Sprite):
    def __init__(self, img, x, y, game, groups):
        super().__init__(groups)
        self.image = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE))

        self.rect = self.image.get_rect()

        self.game = game

        self.rect.x = x
        self.rect.y = y

        self.collidable_mask = pg.mask.from_surface(self.image)