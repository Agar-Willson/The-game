import pygame
from pygame.locals import *
import os

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

# defs



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
        self.air = False
    
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
            self.vect_y = -15
            self.air = True
        if key[pygame.K_UP] == False:
            self.air = False
        
        # add grav
        self.vect_y += 0.5
        if self.vect_y >5:
            self.vect_y  = 5
        dy += self.vect_y
        # collision
        # for tile in world.tile_list:
        #     # x
        #     if tile[1].colliderect(self.rect.x + dx, 10 ,self.width, self.height):
        #         dx = 0
        #     # y
        #     if tile[1].colliderect(self.rect.x, self.rect.y + dy ,self.width, self.height):
        #         if self.vect_y < 0:
        #             dy = tile[1].bottom - self.rect.top
        #             self.vect_y = 0 
        #         elif self.vect_y >= 0:
        #             dy = tile[1].top - self.rect.bottom
        #             self.vect_y = 0 

        tile_rects = [tile[1] for tile in world.tile_list]

        # collision
        # x
        self.rect.x += dx
        x_intersects = [tile for tile in tile_rects if self.rect.colliderect(tile)]
        # if len(x_intersects) != (1 or 0):
        #     raise Exception("what the fuck")
        self.rect.x -= dx
        self.rect.y += dy
        y_intersects = [tile for tile in tile_rects if self.rect.colliderect(tile)]
        # if len(y_intersects) != (1 or 0):
        #     raise Exception("what the fuck 2")
        self.rect.x += dx

        rx = x_intersects[0] if x_intersects else None
        ry = y_intersects[0] if y_intersects else None
        
        if rx:
            if dx < 0:
                self.rect.left = rx.right
            elif dx > 0:
                self.rect.right = rx.left
        # y
        if ry:
            if dy < 0:
                self.rect.top = ry.bottom
                self.vect_y = 0
            elif dy > 0:
                self.rect.bottom = ry.top


        # coords
        
        # self.rect.x += dx
        # self.rect.y += dy

        # if self.rect.bottom > screen_hight:
        #     self.rect.bottom = screen_hight
        #     dy = 0


        #draw player:
        screen.blit(self.img, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


class World():
    
    def __init__(self, data):
        self.tile_list = []

        # images for tiles and enemies
        dirt = pygame.image.load(os.path.join(path,"Dirt.png"))
        grass = pygame.image.load(os.path.join(path,"green.png"))

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
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

world_data = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,2,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,2,0,2,2,2,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,1,1,1,0,2,1],
[1,0,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
[1,2,2,2,2,2,2,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,2,2,2,2,2,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,2,1],
[1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
[1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,1,0,0,0,0,0,0,1],
[1,1,1,1,1,1,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,2,2,1],
[1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,2,2,2,2,0,1,1,1,0,0,1,0,0,0,2,2,2,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,1,1,1,0,0,1,2,2,2,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
[1,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,1],
]


player = Player(100, 450) 
world = World(world_data)

while run:
    screen.blit(back, (0,0))

    world.draw()
    player.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
