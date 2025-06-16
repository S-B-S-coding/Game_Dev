import pygame as pg
import math
from settings import *
import random as rand
# User Character
class Player(pg.sprite.Sprite):
    def __init__(self, img, x, y, game, groups):
        # pass
        super().__init__(groups)
        self.image = pg.transform.scale(img, (TILE_SIZE-5, TILE_SIZE-5))

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

        self.interact = False

        self.dir = "right"

        # create mask for the player
        self.player_mask = pg.mask.from_surface(self.image)
        # self.mask_image = self.player_mask.to_surface() 

        self.velo = 5

    # Die when colliding with enemy
    def enemy_collision(self):
        if pg.sprite.spritecollide(self, self.game.enemies, False):
            
            hits = pg.sprite.spritecollide(self, self.game.enemies, False, pg.sprite.collide_mask)

            if hits:
                # self.x = self.startx
                # self.y = self.starty
                self.game.ending = True

    # collision detection with masks
    def collidables_collision(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.collidables, False)  
            if hits:
                if self.x_change > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.x = hits[0].rect.right
                self.x_change = 0
                self.rect.x = self.x
        
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.collidables, False) 
            if hits:
                if self.y_change > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.y = hits[0].rect.bottom
                self.y_change = 0
                self.rect.y = self.y


    # collect coins
    def coin_collide(self):
        if pg.sprite.spritecollide(self, self.game.coins, False):
            
            hits = pg.sprite.spritecollide(self, self.game.coins, True, pg.sprite.collide_mask)
            if hits:
                self.coin_hit = True
                self.game.balance += 1

    #collect gems
    def gem_collide(self):
        if pg.sprite.spritecollide(self, self.game.gems, False):
            
            hits = pg.sprite.spritecollide(self, self.game.gems, True, pg.sprite.collide_mask)
            if hits:
                self.game.balance += 10

    # npc collision detection
    def npc_interact(self, dir):
        if pg.sprite.spritecollide(self, self.game.npcs, False):
            
            hits = pg.sprite.spritecollide(self, self.game.npcs, False, pg.sprite.collide_mask)
            if hits:
                self.interact = True
            else:
                self.interact = False

        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.npcs, False)  
            if hits:
                if self.x_change > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.x = hits[0].rect.right
                self.x_change = 0
                self.rect.x = self.x
                self.interact = True
            else:
                self.interact = False
                
        
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.npcs, False) 
            if hits:
                if self.y_change > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.y = hits[0].rect.bottom
                self.y_change = 0
                self.rect.y = self.y
                self.interact = True
            else:
                self.interact = False
                

    # movement
    def get_keys(self):
        

        # list of key presses
        keys = pg.key.get_pressed()

        # set velo based on key presses
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.now = pg.time.get_ticks()
            self.dir = "left"
            self.x_change = -1 * self.velo

        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.now = pg.time.get_ticks()
            self.dir = "right"
            self.x_change = self.velo
        
        else:
            self.x_change = 0

        if keys[pg.K_UP] or keys[pg.K_w]:
            self.now = pg.time.get_ticks()
            self.dir = "up"
            self.y_change = -1 * self.velo

        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.now = pg.time.get_ticks()
            self.dir = "down"
            self.y_change = self.velo

        else:
            self.y_change = 0
            

        # if keys[pg.K_LEFT] and keys[pg.K_RIGHT]:
        #     self.x_change = 0
        # if keys[pg.K_UP] and keys[pg.K_DOWN]:
        #     self.y_change = 0

        

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
        
    def update(self):
        self.interact = False
        self.get_keys()

        # update player location
        self.x += self.x_change
        self.y += self.y_change
        
        self.enemy_collision()

        self.coin_collide()
        self.gem_collide()
        
        self.rect.x = self.x
        self.collidables_collision('x')
        self.npc_interact('x')
        self.rect.y = self.y
        self.collidables_collision('y')
        self.npc_interact('y')
        
        
        
# enemy character/s
class Enemy(pg.sprite.Sprite):
    def __init__(self, img, x, y, game, groups):
        # pass
        super().__init__(groups)

        self.image = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        
        self.speed = 3

        self.game = game

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        self.rect.x = x
        self.rect.y = y

        self.enemy_mask = pg.mask.from_surface(self.image)


    # collide with walls, fences, etc.
    def collidables_collision(self, dir):  
        # collision with collidables sprites
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.collidables, False)  
            if hits:
                if self.distance_to_playerx > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    self.speed = 0
                    self.rect.x -= 0.25
                    self.speed = 3
                if self.distance_to_playerx < 0:
                    self.rect.x = hits[0].rect.right
                    self.speed = 0
                    self.rect.x += 0.25
                    self.speed = 3
        
        
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.collidables, False) 
            if hits:
                if self.distance_to_playery > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    self.speed = 0
                    self.rect.y -= 0.25
                    self.speed = 3
                if self.distance_to_playery < 0:
                    self.rect.y = hits[0].rect.bottom
                    self.speed = 0
                    self.rect.y += 0.25
                    self.speed = 3
        
        # collision with Enemy_Wall sprites
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.enemy_walls, False)  
            if hits:
                if self.distance_to_playerx > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    self.speed = 0
                    self.rect.x -= 0.25
                    self.speed = 3
                if self.distance_to_playerx < 0:
                    self.rect.x = hits[0].rect.right
                    self.speed = 0
                    self.rect.x += 0.25
                    self.speed = 3
        
        
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.enemy_walls, False) 
            if hits:
                if self.distance_to_playery > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    self.speed = 0
                    self.rect.y -= 0.25
                    self.speed = 3
                if self.distance_to_playery < 0:
                    self.rect.y = hits[0].rect.bottom
                    self.speed = 0
                    self.rect.y += 0.25
                    self.speed = 3

    # attack the player when within a certain distance
    def follow_player(self):
        self.distance_to_playerx = self.game.player.rect.x - self.rect.x
        self.distance_to_playery = self.game.player.rect.y - self.rect.y

        # find driection vectro (dx, dy) between enemy and player
        self.dirvect = pg.math.Vector2(self.distance_to_playerx, self.distance_to_playery)
        self.dirvect.normalize()
        # Move along normalized vector towards the player at current speed
        self.dirvect.scale_to_length(self.speed)

        self.rect.move_ip((0, self.dirvect[1]))
        self.collidables_collision('y')
        self.rect.move_ip((self.dirvect[0], 0))
        self.collidables_collision('x')

    def keep_enemy_outside_collidables(self):
        if pg.sprite.spritecollide(self, self.game.collidables, False):
            
            hits = pg.sprite.spritecollide(self, self.game.collidables, False, pg.sprite.collide_mask)
            if hits:
                self.rect.x = rand.randrange(int((DISPLAY_WIDTH/3) +20), int(DISPLAY_WIDTH-64))
                self.rect.y = rand.randrange(32, (DISPLAY_HEIGHT - 64))
    
    # keep enemy outside safety wehen respawn
    def keep_enemy_outside_safety(self):
        if pg.sprite.spritecollide(self, self.game.safety, False):
            
            hits = pg.sprite.spritecollide(self, self.game.safety, False, pg.sprite.collide_mask)
            if hits:
                self.rect.x = rand.randrange(int((DISPLAY_WIDTH/3) +20), int(DISPLAY_WIDTH-64))
                self.rect.y = rand.randrange(32, (DISPLAY_HEIGHT - 64))

    def update(self):
        self.follow_player()
        self.keep_enemy_outside_collidables()
        self.keep_enemy_outside_safety()

# all objs that stop movement
class Collidables(pg.sprite.Sprite):
    def __init__(self, img, x, y, width, height, groups):
        super().__init__(groups)
        self.image = pg.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.collidable_mask = pg.mask.from_surface(self.image)

# obj that stops movement for only enemies
class Enemy_Wall(pg.sprite.Sprite):
    def __init__(self, img, x, y, width, height, groups):
        super().__init__(groups)
        self.image = pg.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.collidable_mask = pg.mask.from_surface(self.image)

# collectable for building balance
class Coin(pg.sprite.Sprite):
    def __init__(self, img, x, y, game, groups):
        super().__init__(groups)
        self.image = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE))

        self.rect = self.image.get_rect()

        self.game = game

        self.x = x
        self.y = y
        # self.rect.x = x
        # self.rect.y = y

        self.collidable_mask = pg.mask.from_surface(self.image)

    def keep_coin_outside_collidables(self):
        if pg.sprite.spritecollide(self, self.game.collidables, False):
            
            hits = pg.sprite.spritecollide(self, self.game.collidables, False, pg.sprite.collide_mask)
            if hits:
                self.x = rand.randrange(int((DISPLAY_WIDTH/3) +20), int(DISPLAY_WIDTH-64))
                self.y = rand.randrange(32, (DISPLAY_HEIGHT - 64))
    
    def keep_coin_outside_safety(self):
        if pg.sprite.spritecollide(self, self.game.safety, False):
            
            hits = pg.sprite.spritecollide(self, self.game.safety, False, pg.sprite.collide_mask)
            if hits:
                self.x = rand.randrange(int((DISPLAY_WIDTH/3) +20), int(DISPLAY_WIDTH-64))
                self.y = rand.randrange(32, (DISPLAY_HEIGHT - 64))
    
    def update(self):
        self.keep_coin_outside_collidables()
        self.keep_coin_outside_safety()
        self.rect.x = self.x
        self.rect.y = self.y


# used for damage against enemies
class Bullet(pg.sprite.Sprite):
    def __init__(self, screen, x, y, img, dir, game, groups):
        super().__init__(groups)
        self.game = game
        self.x = x
        self.y = y
        self.xvelo = 0
        self.yvelo = 0

        self.dir = dir
        self.image = pg.transform.scale(img, (TILE_SIZE/2, TILE_SIZE/2))
        self.rect = self.image.get_rect()

    # find direction for bullet to shoot
    def shoot(self, dir):
        if dir == "right":
            self.xvelo = 8
        elif dir == "left":
            self.xvelo = -8
        if dir == "down":
            self.yvelo = 8
        elif dir == "up":
            self.yvelo = -8
        self.x += self.xvelo
        self.y += self.yvelo

    # kill bullet when off map
    def stop(self):
        if self.x >= DISPLAY_WIDTH or self.x <= 0 or self.y >= DISPLAY_HEIGHT or self.y <= 0:
            self.kill

    # kill bullet when hitting wall
    def collidables_collision(self):
        hits = pg.sprite.spritecollide(self, self.game.collidables, False)
        if hits:
            self.kill()
    

    # kill enemy & spawn gem
    def enemy_collision(self):
        hits = pg.sprite.spritecollide(self, self.game.enemies, True)
        if hits:
            self.kill()
            self.gem = Gem(self.game.gem_img, self.x, self.y, self.game, [self.game.gems, self.game.all_sprites])
            
            rand_x = rand.randrange(int((DISPLAY_WIDTH/3) +20), int(DISPLAY_WIDTH-64))
            rand_y = rand.randrange(32, (DISPLAY_HEIGHT - 64))
            Enemy(self.game.enemy_img, rand_x, rand_y, self.game, [self.game.all_sprites, self.game.enemies])

            self.game.kill_count += 1

    def update(self):
        self.shoot(self.dir)
        self.stop()
        self.collidables_collision()
        self.enemy_collision()
        self.rect.centerx = self.x
        self.rect.centery = self.y

# purchasable form of damaging enemies
class Traps(pg.sprite.Sprite):
    def __init__(self, screen, x, y, img, dir, game, groups):
        super().__init__(groups)
        self.game = game
        self.x = x
        self.y = y
        self.speed = 8

        self.dir = dir
        self.image = pg.transform.scale(img, (TILE_SIZE/2, TILE_SIZE/2))
        self.rect = self.image.get_rect()


    # kill enemy & spawn gem
    def enemy_collision(self):
        hits = pg.sprite.spritecollide(self, self.game.enemies, True)
        if hits:
            self.kill()
            self.gem = Gem(self.game.gem_img, self.x, self.y, self.game, [self.game.gems, self.game.all_sprites])
            
            rand_x = rand.randrange(int((DISPLAY_WIDTH/3) +20), int(DISPLAY_WIDTH-64))
            rand_y = rand.randrange(32, (DISPLAY_HEIGHT - 64))
            Enemy(self.game.enemy_img, rand_x, rand_y, self.game, [self.game.all_sprites, self.game.enemies])
            self.game.kill_count += 1

    def update(self):
        # self.collidables_collision()
        self.enemy_collision()
        self.rect.centerx = self.x
        self.rect.centery = self.y

# easier form of damaging enemies
class Fireball(pg.sprite.Sprite):
    def __init__(self, screen, x, y, img, dir, game, groups):
        super().__init__(groups)
        self.game = game
        self.x = x
        self.y = y
        self.xvelo = 0
        self.yvelo = 0

        self.dir = dir
        self.image = pg.transform.scale(img, (TILE_SIZE*2, TILE_SIZE*2))
        self.rect = self.image.get_rect()

    # find direction for bullet to shoot
    def shoot(self, dir):
        if dir == "right":
            self.xvelo = 8
        elif dir == "left":
            self.xvelo = -8
        if dir == "down":
            self.yvelo = 8
        elif dir == "up":
            self.yvelo = -8
        self.x += self.xvelo
        self.y += self.yvelo

    # kill bullet when off map
    def stop(self):
        if self.x >= DISPLAY_WIDTH or self.x <= 0 or self.y >= DISPLAY_HEIGHT or self.y <= 0:
            self.kill

    # kill bullet when hitting wall
    def collidables_collision(self):
        hits = pg.sprite.spritecollide(self, self.game.collidables, False)
        if hits:
            self.kill()
    

    # kill enemy & spawn gem
    def enemy_collision(self):
        hits = pg.sprite.spritecollide(self, self.game.enemies, True)
        if hits:
            self.kill()
            self.gem = Gem(self.game.gem_img, self.x, self.y, self.game, [self.game.gems, self.game.all_sprites])
            
            rand_x = rand.randrange(int((DISPLAY_WIDTH/3) +20), int(DISPLAY_WIDTH-64))
            rand_y = rand.randrange(32, (DISPLAY_HEIGHT - 64))
            Enemy(self.game.enemy_img, rand_x, rand_y, self.game, [self.game.all_sprites, self.game.enemies])
            self.game.kill_count += 1

    def update(self):
        self.shoot(self.dir)
        self.stop()
        self.collidables_collision()
        self.enemy_collision()
        self.rect.centerx = self.x
        self.rect.centery = self.y

# interactive NPC
class NPC(pg.sprite.Sprite):
    def __init__(self, img, x, y, game, groups):
        super().__init__(groups)
        self.game = game

        self.image = pg.transform.scale(img, (TILE_SIZE-1, TILE_SIZE-1))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.npc_mask = pg.mask.from_surface(self.image)

# safety space away from enemies for player
class Safety(pg.sprite.Sprite):
    def __init__(self, img, x, y, width, height, groups):
        super().__init__(groups)
        self.image = pg.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.safety_mask = pg.mask.from_surface(self.image)

# collectable that drops from killing enemies
class Gem(pg.sprite.Sprite):
    def __init__(self, img, x, y, game, groups):
        super().__init__(groups)
        self.image = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE))

        self.rect = self.image.get_rect()

        self.game = game

        self.x = x
        self.y = y

        self.collidable_mask = pg.mask.from_surface(self.image)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

