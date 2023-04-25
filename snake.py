from asyncio.windows_events import NULL
from cmath import pi
from turtle import width
import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

class Grid():
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
    
    def draw(self):
        x = 0
        y = 0
        for i in range(self.width // self.snake.unit_Size + 1):
            pygame.draw.line(self.window, (150, 150, 150), (0, y), (self.width, y))
            pygame.draw.line(self.window, (150, 150, 150), (x, 0), (y, self.height))
            x = x + self.snake.unit_Size
            y = y + self.snake.unit_Size

class Snake():
    unit_Size = 30
    x = 0
    y = 0
    direction_x = 1
    direction_y = 0
    speed = 1
    size = 1
    head_color = (80, 0, 160)
    body_color = (140, 0, 220)
    list_head = []
    list_body = []
    is_Dead = False

    def draw(self, window):
         return pygame.draw.rect(window, self.head_color, (self.x, self.y, self.unit_Size, self.unit_Size))

    def add_Body_Positions(self):
        self.list_head = []
        self.list_head.append(self.x)
        self.list_head.append(self.y)
        self.list_body.append(self.list_head)

    def grow(self, window):
        if len(self.list_body) > self.size:
            self.list_body.pop(0)       

        for i in range(len(self.list_body) - 1):
            pygame.draw.rect(window, self.body_color, (self.list_body[i][0], self.list_body[i][1], self.unit_Size, self.unit_Size))

class Food():
    unit_Size = 30
    color = (200, 0, 0)
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        return pygame.draw.rect(window, self.color, (self.x, self.y, self.unit_Size, self.unit_Size))

class Menu():
    font = pygame.font.SysFont("Gabriola", 40, True, False)
    texts = []
    texts.append(font.render("SNAKE", True, (0, 0, 0)))
    texts.append(font.render("1 - NEW GAME", True, (0, 0, 0)))
    texts.append(font.render("2 - CONTINUE GAME", True, (0, 0, 0)))
    texts.append(font.render("M - MUSIC ON/OFF", True, (0, 0, 0)))
    texts.append(font.render("Q - QUIT", True, (0, 0, 0)))    

    def draw(self, window):
        y = 180
        rect_text = self.texts[0].get_rect()
        rect_text.center = (400, y)
        window.blit(self.texts[0], rect_text)
        y = y + 80
        for i in range(1, len(self.texts)):
            rect_text = self.texts[i].get_rect()
            rect_text.center = (400, y)
            window.blit(self.texts[i], rect_text)
            y = y + 40

class Game_Controler():
    score = 0
    width = 780
    height = 600
    fps = 5
    font = NULL
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    snake = NULL
    food = NULL
    colided = NULL
    soundtrack = NULL
    menu = NULL
    in_Menu = True
    
    def player_Input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if (event.key == K_w or event.key == K_UP) and self.snake.direction_y != 1:
                    self.snake.direction_x = 0
                    self.snake.direction_y = -1
                    break
                if (event.key == K_a or event.key == K_LEFT) and self.snake.direction_x != 1:
                    self.snake.direction_x = -1
                    self.snake.direction_y = 0
                    break
                if (event.key == K_s or event.key == K_DOWN) and self.snake.direction_y != -1:
                    self.snake.direction_x = 0
                    self.snake.direction_y = 1
                    break
                if (event.key == K_d or event.key == K_RIGHT) and self.snake.direction_x != -1:
                    self.snake.direction_x = 1
                    self.snake.direction_y = 0
                    break
                if event.key == K_m:
                    if pygame.mixer.music.get_volume() == 0:
                        pygame.mixer.music.set_volume(0.5)
                    else:
                        pygame.mixer.music.set_volume(0)
                if event.key == K_ESCAPE:
                    self.in_Menu = True
                    self.call_Menu()
                if event.key == K_q:
                    pygame.quit()
                    exit()
    
    def draw_Grid(self):
        x = 0
        y = 0
        for i in range(self.width // self.snake.unit_Size + 1):
            pygame.draw.line(self.window, (150, 150, 150), (0, y), (self.width, y))
            pygame.draw.line(self.window, (150, 150, 150), (x, 0), (y, self.height))
            x = x + self.snake.unit_Size
            y = y + self.snake.unit_Size

    def create_Elements(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("Gabriola", 40, True, False)

        self.soundtrack = pygame.mixer.music.load('sounds/Mendelssohn_Lost_Illusions.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.colided = pygame.mixer.Sound('sounds/menu_open.wav')
        self.colided.set_volume(0.4)

        self.menu = Menu()

        self.snake = Snake()
        self.food = Food(randint(0, (self.width//self.snake.unit_Size)-1) * 30, randint(0, (self.height//self.snake.unit_Size)-1) * 30)
        

    def check_Collision(self):
        if self.snake.draw(self.window).colliderect(self.food.draw(self.window)):
            self.food.x = randint(0, (self.width//self.food.unit_Size)-1) * 30
            self.food.y = randint(0, (self.height//self.food.unit_Size)-1) * 30
            self.score = self.score + 1
            self.colided.play()
            self.snake.size = self.snake.size + 1
            self.fps = self.fps + (self.snake.size/50)

    def check_Borders(self):
        if self.snake.x > self.width - self.snake.unit_Size:
            self.snake.x = 0
        if self.snake.x < 0:
            self.snake.x = self.width - self.snake.unit_Size
        if self.snake.y > self.height - self.snake.unit_Size:
            self.snake.y = 0
        if self.snake.y < 0:
            self.snake.y = self.height - self.snake.unit_Size

    def check_Death(self):
        if self.snake.list_body.count(self.snake.list_head) > 1:
            self.snake.is_Dead = True

            while self.snake.is_Dead:
                self.window.fill((255, 255, 255))
                texts = []
                texts.append(self.font.render("YOU DIED!", True, (0, 0, 0)))
                texts.append(self.font.render("PRESS 'Esc' TO GO BACK TO MENU", True, (0, 0, 0)))
                y = 260
                for text in texts:
                    rect_text = text.get_rect()
                    rect_text.center = (400, y)
                    y = y + 40
                    self.window.blit(text, rect_text)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.in_Menu = True
                            self.call_Menu()
                        if event.key == K_q:
                            pygame.quit()
                            exit()
                pygame.display.update()
        
    def call_Menu(self):
        while self.in_Menu:
            self.window.fill((255, 255, 255))
            self.menu.draw(self.window)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        self.reset_Game()
                        self.in_Menu = False
                    if event.key == K_2 or event.key == K_ESCAPE:
                        self.in_Menu = False
                    if event.key == K_m:
                        if pygame.mixer.music.get_volume() == 0:
                            pygame.mixer.music.set_volume(0.5)
                        else:
                            pygame.mixer.music.set_volume(0)
                    if event.key == K_q:
                        pygame.quit()
                        exit()
            pygame.display.update()

    def reset_Game(self):
        self.score = 0
        self.snake.size = 1
        self.snake.x = self.width // 2
        self.snake.y = self.height // 2
        self.food.x = randint(0, (self.width//self.food.unit_Size)-1) * 30
        self.food.y = randint(0, (self.height//self.food.unit_Size)-1) * 30
        self.snake.list_head = []
        self.snake.list_body = []
        self.snake.speed = 1
        self.fps = 5
        self.snake.is_Dead = False

    def game_Loop(self):
        while True:
            self.clock.tick(self.fps)
            self.window.fill((255, 255, 255))

            print(self.fps)

            self.call_Menu()

            self.window.blit(self.font.render("Score: {}".format(self.score), True, (0, 0, 0)), (630, 10))
            self.draw_Grid()

            self.player_Input()

            self.check_Death()            

            self.snake.x = self.snake.x + (self.snake.direction_x * self.snake.unit_Size)
            self.snake.y = self.snake.y + (self.snake.direction_y * self.snake.unit_Size)

            self.check_Borders()

            self.snake.add_Body_Positions()

            self.snake.draw(self.window)
            self.food.draw(self.window)
            
            
            
            self.check_Collision()
            
            self.snake.grow(self.window)

            pygame.display.update()


    def play(self):
        self.create_Elements()
        self.game_Loop()

game = Game_Controler()
game.play()