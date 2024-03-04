import pygame
from pygame.locals import *
import pickle
import os
import time

pygame.init()

screen_width = 1000
screen_hight = 500

screen = pygame.display.set_mode((screen_width, screen_hight))
pygame.display.set_caption("The_Game")

run = True

# tiles:
tile_size = 25



# load images:
size = 1000
path = "data"
back = pygame.image.load(os.path.join(path,"background.png"))
back = pygame.transform.scale(back,(size,size/2))
happy_music = pygame.mixer.Sound(os.path.join(path,"endsong.mp3"))
forest = pygame.image.load(os.path.join(path,"forest.png"))
action_sound = pygame.mixer.Sound(os.path.join(path,"coolaidsound.mp3"))

# class
class Player():
    def __init__(self, x, y):
        img = pygame.image.load(os.path.join(path,"playerp.png"))
        self.img = pygame.transform.scale(img,(tile_size,tile_size))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.vect_y = 0
        self.air = True
    
    def update(self):
        

        dx = 0
        dy = 0
        # get presses
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx -= 1
        if key[pygame.K_RIGHT]:
            dx += 1
        if key[pygame.K_UP] and self.air == False:
            self.vect_y = -8
            self.air = True
        if key[pygame.K_UP] == False:
            self.air = False
        
        # add grav
        self.vect_y += 0.2
        if self.vect_y >4:
            self.vect_y  = 4
        dy += self.vect_y
        # collision
        on_ground = False
        for tile in world.tile_list:
            # x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y ,self.width, self.height):
                dx = 0
            # y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy ,self.width, self.height):
                if self.vect_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vect_y = 0 
                elif self.vect_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vect_y = 0 
                    on_ground = True
        if on_ground:
            self.air = False
        else:
            self.air = True  # If we've not collided with the ground, we're in the air

# Jumping logic - now checks if not in the air before allowing a jump
        if key[pygame.K_UP] and not self.air:
            self.vect_y = -8
            self.air = True



        # coords
        
        self.rect.x += dx
        self.rect.y += dy

        


        #draw player:
        screen.blit(self.img, self.rect)

class World():
    
    def __init__(self, data):
        self.tile_list = []
        # images for tiles and enemies
        dirt = pygame.image.load(os.path.join(path,"Dirt.png"))
        grass = pygame.image.load(os.path.join(path,"green.png"))
        water = pygame.image.load(os.path.join(path,"water.png"))
        coolade = pygame.image.load(os.path.join(path,"coolade.png"))
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(water,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    img = pygame.transform.scale(coolade,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

world_data1 = [
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[2,0,0,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,0,2,2,2,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,1],
[1,0,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,0,2,2,2,2,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
[1,2,2,2,2,2,2,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,2,2,2,2,2,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,2,1],
[1,1,1,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
[1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,1,0,0,0,0,0,0,1],
[1,1,1,0,0,1,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,2,2,1],
[1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,2,2,2,2,0,1,1,1,0,0,1,0,0,0,2,2,2,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,1,1,1,0,0,1,2,2,2,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
[1,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,1],
]
world_data2= [
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,1],
[1,1,1,0,2,2,2,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
[1,0,0,0,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,0,0,2,2,2,2,1],
[1,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1],
[1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,2,2,0,0,0,0,1],
[1,0,0,0,0,0,2,2,1,1,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,1,1,0,0,0,0,1],
[1,0,0,0,0,0,1,1,1,1,2,2,2,2,2,1,1,0,0,0,0,0,0,0,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,2,2,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1,1,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,1],
[1,0,0,0,0,0,2,2,2,2,2,2,2,2,2,1,1,1,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,1,1,2,2,1],
[1,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]
world_data3=[
[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0],
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0],
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0],
[3,0,0,0,0,0,0,3,3,0,0,0,0,0,3,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,3,3,0,0,3,3],
[3,0,0,0,3,3,3,3,3,0,0,0,0,0,3,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,3,3,3],
[3,0,0,0,0,0,3,3,3,0,0,0,0,0,3,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,3,3,3,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,3,3,0,0,0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,3,3,3,0,0,0,3,3,0,0,0,0,0,0,3,0,0,0,0,3],
[3,0,0,0,0,0,3,3,3,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,0,3,0,0,0,0,3],
[3,0,0,0,0,0,3,3,0,0,0,0,3,3,0,0,0,3,0,0,0,0,3,3,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,3,3,3,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0,3,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,3,3,3,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,3,3,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,3,3,3,0,0,0,3,3,3,3,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,3,3,3,0,0,0,0,3,3,3,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,3,3,3,3,0,0,0,3,3,3,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
]
world_data4 = [
[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3],
[3,0,0,0,0,0,3,0,0,0,3,0,0,0,3,0,0,0,0,0,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,3,3,0,0,3,0,0,0,3,0,0,0,0,0,3,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,0,3,0,0,3,0,0,0,3,0,0,0,0,0,3,0,3,4,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,3],
[3,0,0,0,3,0,3,3,0,0,3,0,0,0,3,0,0,0,0,0,3,0,0,3,4,0,0,0,0,0,3,0,4,4,4,4,0,0,0,3],
[3,0,0,0,3,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,3,4,0,0,0,0,3,0,3,3,3,0,0,0,0,3],
[3,0,3,0,3,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,0,0,0,3,0,0,0,0,0,0,0,0,3],
[3,0,3,0,3,0,3,3,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,3,3,0,0,4,4,3,0,0,0,0,0,0,3,3,3],
[3,0,3,0,0,3,0,3,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,3,3,0,3],
[3,4,3,0,3,3,0,0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,3,3,0,0,3],
[3,3,3,4,3,3,4,4,3,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,0,0,3],
[3,4,4,3,3,3,3,3,3,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,3,0,0,0,3],
[3,3,3,3,3,3,3,3,0,0,0,0,0,3,0,0,3,0,0,0,0,0,0,0,0,0,0,0,3,3,0,0,0,3,3,3,0,0,0,3],
[3,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,3,0,0,3,0,0,0,0,0,3,0,0,0,3,3,0,0,3,0,3,0,0,0,3],
[3,0,0,0,0,0,0,0,0,0,0,3,0,3,0,0,3,0,0,3,0,0,0,0,0,3,0,0,0,0,0,0,0,3,3,3,3,0,0,3],
[3,0,0,0,0,0,0,0,0,0,0,3,0,3,0,0,3,0,0,3,4,4,4,4,4,3,0,0,0,0,0,0,0,0,3,3,0,3,0,3],
[3,0,0,0,0,0,0,0,0,0,0,3,0,3,0,0,3,0,0,3,3,3,3,3,3,0,0,0,0,0,3,0,0,0,3,3,0,3,0,3],
[3,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0,3,0,0,3,3,3,3,3,3,0,0,0,3,0,3,0,3,0,3,3,0,3,0,3],
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,3,3,3,3,3,3,0,0,0,3,0,3,0,3,0,3,3,0,3,0,3],
[3,4,4,4,4,4,3,3,3,3,3,3,4,3,4,4,3,3,3,3,3,3,3,3,3,3,4,4,3,3,3,3,3,3,3,3,3,3,3,3],
]
world_data5 =[
[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0,0,0,0,4,4,0,0,3],
[3,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,4,4,4,4,4,4,3,3,3,4,4,4,4,4,4,4,4,4,4,3,3,0,0,3],
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,3],
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,3],
[3,0,0,0,0,0,0,0,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,3],
[3,0,0,0,4,4,4,4,4,3,3,3,3,3,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,3],
[3,0,0,4,3,3,3,3,3,0,0,0,0,0,0,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,3,4,4,4,4,4,4,0,0,0,4,4,4,4,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,4,4,3,3,3,3,4,4,4,4,4,0,0,0,0,3],
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,0,0,0,0,3],
[3,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,4,4,4,3],
[3,0,0,0,0,0,0,0,0,0,4,4,4,3,3,3,3,3,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3],
[3,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,3],
]

player = Player(100, 450) 
world = World(world_data1)


while run:
    screen.blit(back, (0,0))

    world.draw()
    player.update()
    if player.rect.y<0:
        player = Player(100, 450) 
        world = World(world_data2)
        while run: 
            screen.blit(back, (0,0))
            world.draw()
            player.update()
            if player.rect.y<0:
                happy_music.play()
                pygame.display.set_caption("help me")
                player = Player(100, 450) 
                world = World(world_data3)
                while run:
                    screen.blit(forest, (0,0))
                    world.draw()
                    player.update()
                    if player.rect.y > screen_hight:
                        img = pygame.image.load(os.path.join(path,"maxresdefault.png"))
                        screen.blit(img, (-20,-20))
                        time.sleep(3)
                        screen.blit(img, (-20,-20))
                        run = False
                    if player.rect.y<0:
                        player = Player(100, 450) 
                        world = World(world_data4)
                        while run:
                            screen.blit(forest, (0,0))
                            world.draw()
                            player.update()
                            if player.rect.y < 0:
                                repeat =0
                                while repeat <1:
                                    screen.fill((0,0,0))
                                    img = pygame.image.load(os.path.join(path,"theback.png"))
                                    img = pygame.transform.scale(img,(tile_size*10,tile_size*10))
                                    screen.blit(img, (500, 250))
                                    time.sleep(5)
                                    img = pygame.image.load(os.path.join(path,"thefront.png"))
                                    img = pygame.transform.scale(img,(tile_size*10,tile_size*10))
                                    screen.blit(img, (500, 250))
                                    say = pygame.mixer.Sound(os.path.join(path,"say1.wav"))
                                    say.play()
                                    time.sleep(5)
                                    say = pygame.mixer.Sound(os.path.join(path,"say2.wav"))
                                    say.play()
                                    action_sound.play()
                                    img = pygame.image.load(os.path.join(path,"lastbreath.png"))
                                    img = pygame.transform.scale(img,(tile_size*10,tile_size*10))
                                    screen.blit(img, (500, 250))
                                    say = pygame.mixer.Sound(os.path.join(path,"say3.wav"))
                                    time.sleep(5)
                                    say.play()
                                    img = pygame.image.load(os.path.join(path,"remains.png"))
                                    img = pygame.transform.scale(img,(tile_size*10,tile_size*10))
                                    screen.blit(img, (500, 250))
                                    repeat +=1
                                player = Player(50, 50) 
                                world = World(world_data5)
                                tune = pygame.mixer.Sound(os.path.join(path,"jogging.mp3"))
                                tune.play()
                                while run:
                                    screen.blit(forest, (0,0))
                                    world.draw()
                                    player.update()
                                    end = 0
                                    jump= pygame.mixer.Sound(os.path.join(path,"jumpsxf.wav"))
                                    jump.play()
                                    if player.rect.y > screen_hight:
                                        end = 1
                                    if end ==1:
                                        break
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            run = False
                                    pygame.display.update()
                                if end == 1:
                                    while run:
                                        screen.blit(back, (0,0))
                                        time.sleep(3)
                                        img = pygame.image.load(os.path.join(path,"maxresdefault.png"))
                                        happy_music.play()
                                        time.sleep(5)
                                        say = pygame.mixer.Sound(os.path.join(path,"finalsay.wav"))
                                        say.play()
                                        while run:
                                            screen.blit(img,(-20,-20))
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    run = False
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        run = False
                            pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                    pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()







pygame.quit()
