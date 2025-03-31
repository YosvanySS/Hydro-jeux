#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 18:04:19 2023

@author: yosvany
"""

import pygame
from sys import exit
from random import randint, choice

class Hydrogen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        player_image = pygame.image.load('graphics/Player/hydrogen.png').convert_alpha()
        scale = 1/10
        self.image = pygame.transform.scale(player_image, (player_image.get_width() * scale, player_image.get_height() * scale))

        self.xpos = 80
        self.ypos = 400
        self.speed = 5
        self.slab_speed = 20  # In pixels units
        self.rect = self.image.get_rect(midleft = (self.xpos,self.ypos))
        
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(1)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        
        # if left arrow key is pressed, move to left
        if keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.rect.x -= self.speed
            self.jump_sound.play()
        
        # if right arrow key is pressed, move to right
        if keys[pygame.K_RIGHT] and self.rect.right <= 1400:
            self.rect.x += self.speed
            self.jump_sound.play()
        
        # if up arrow key is pressed, move to up
        if keys[pygame.K_UP] and self.rect.top >= 0:
            self.rect.y -= self.speed
            self.jump_sound.play()
            
        # if down arrow key is pressed, move to up
        if keys[pygame.K_DOWN] and self.rect.bottom <= 800:
            self.rect.y += self.speed
            self.jump_sound.play()           
    
    def apply_speed(self):
        # If in the W_part, decreases the speed
        if self.rect.top < self.ypos - self.slab_speed:
            self.speed = 7
        
        # If in the Cu_part, increases the speed
        if self.rect.bottom > self.ypos + self.slab_speed:
            self.speed = 7
            
        # If in the middle_part, keeps the same speed
        if self.rect.bottom >= self.ypos - self.slab_speed and self.rect.top <= self.ypos + self.slab_speed:
            self.speed = 4
    
    def update(self):
        self.apply_speed()
        self.player_input()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
		
        if type == 'tungsten':
            scale = 1/7
            w_1 = pygame.image.load('graphics/Player/tungsten.png').convert_alpha()
            w_1 = pygame.transform.scale(w_1, (w_1.get_width() * scale, w_1.get_height() * scale))
            self.frames = w_1
            y_pos  = randint(0, 400)
        
        if type == 'copper':
            scale = 1/7
            cu_1 = pygame.image.load('graphics/Player/copper.png').convert_alpha()
            cu_1 = pygame.transform.scale(cu_1, (cu_1.get_width() * scale, cu_1.get_height() * scale))
            self.frames = cu_1
            y_pos  = randint(400, 800)
        
        if type == 'interstitial':
            scale = 1/25
            h_1 = pygame.image.load('graphics/Player/interstitial.png').convert_alpha()
            h_1 = pygame.transform.scale(h_1, (h_1.get_width() * scale, h_1.get_height() * scale))
            self.frames = h_1
            y_pos  = randint(0, 800)

        self.image = self.frames
        self.rect = self.image.get_rect(midleft = (randint(1300,1400),y_pos))

    def update(self):
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100: 
            self.kill()

def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (100,50))
	screen.blit(score_surf,score_rect)
    
	#score_surf = test_font.render(f'Lives: ',False,(64,64,64))
	#score_rect = score_surf.get_rect(center = (300,50))
	screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else:
		return True


#===========================================================================#

pygame.init()
x_screen = 1400
y_screen = 800
screen = pygame.display.set_mode((x_screen,y_screen))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)
bg_music.set_volume(0.2)

list_with_scores = []

# List of colors
aquamarine = (118,238,198)
brown      = (255,64,64)
cadetblue  = (152,245,255)
orange     = (255,97,3)
crimson    = (220,20,60)
violet     = (191,62,255)
pink       = (255,52,179)
grey       = (244,244,244)
blue       = (0,0,255)
black      = (255, 255, 255)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Hydrogen())

obstacle_group = pygame.sprite.Group()

# Loading environmments
w_surface = pygame.image.load('graphics/W_part.png').convert()
w_surface = pygame.transform.scale(w_surface, (w_surface.get_width(), w_surface.get_height() * x_screen/2/788))
cu_surface = pygame.image.load('graphics/Cu_part.png').convert()
cu_surface = pygame.transform.scale(cu_surface, (cu_surface.get_width(), cu_surface.get_height() * x_screen/2/788))

# Intro screen
scale = 1/15
player_stand = pygame.image.load('graphics/Player/hydrogen.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand = pygame.transform.scale(player_stand, (player_stand.get_width() * scale, player_stand.get_height() * scale))
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Diffusion game',False,black)
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer
dificulty = 1200  # Number between 1000 and 1400
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500 - dificulty)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['tungsten','copper','tungsten','copper','tungsten','copper','interstitial'])))

		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:
		screen.blit(w_surface,(0,0))
		screen.blit(cu_surface,(0,y_screen/2))
		score = display_score()
		list_with_scores.append(score)
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()

	if game_active == False:
		screen.fill((0,0,0))
		screen.blit(player_stand,player_stand_rect)

		score_message = test_font.render(f'Your score: {score}',False,black)
		score_message_rect = score_message.get_rect(center = (400,330))
        
		#record_message = test_font.render(f'Best score: {list_with_scores.max()}',False,black)
		#record_message_rect = score_message.get_rect(center = (400,500))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)

