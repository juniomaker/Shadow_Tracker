
from curses.ascii import ctrl
from email import message
import math
from numpy import true_divide
import pygame
from pygame.locals import *
from sys import exit
from shadow_plot import positions, location
import time

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN_DARK = (0, 127, 0)
BLUE = (0, 0, 255)
BLUE_DARK = (0, 0, 127)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
GRAY_DARK = (32, 32, 32)

SCALE = 60
obj_obstacle = {"width":1000, "height" :1000}
v_simulation = 0.02

w_screen = 720
h_screen = 600

pygame.init()

# seta os parametros da tela
screen = pygame.display.set_mode((w_screen, h_screen))
pygame.display.set_caption("Shadow Tracker")

# configura a fonte dos textos
font_h1 = pygame.font.SysFont('arial', 20, True, False)
font_h2 = pygame.font.SysFont('arial', 10, True, False)

def cartesian_absolut(coordinate_x, coordinate_y, w=0, h=0):
    zero_x = w_screen / 2 + 1 - w/2
    zero_y = h_screen / 2 +1 - h/2
    return round(coordinate_x * SCALE + zero_x), round(coordinate_y * SCALE + zero_y)

def cartesian_relative(coordinate_x, coordinate_y, referential_x, referential_y, flag_round=False):
    x_scaled = coordinate_x * SCALE
    y_scaled = coordinate_y * SCALE
    
    if flag_round:
        x_scaled = round(x_scaled)
        y_scaled = round(y_scaled)
        
    x_abs =  x_scaled + referential_x
    y_abs = y_scaled + referential_y
    
    if x_abs > w_screen:
        x_abs = w_screen
    if y_abs > h_screen:
        y_abs = h_screen
        
    return  x_abs, y_abs

def grid(color, scale):
    for row in range(0, h_screen, scale):
        pygame.draw.line(screen, color, (0, row), (w_screen, row), 1)

    for column in range(0, w_screen, scale):
        pygame.draw.line(screen, color, (column, 0), (column, h_screen), 1)

    return 

def border(list_of_dot: list(), dot_zero: list()):
    x_0, y_0 = dot_zero
    result = list()
    for dot in list_of_dot:

        x, y = dot

        if x < x_0:
            x = x -1
        elif x == x_0:
            x = x
        else:
            x = x + 1

        if y < y_0:
            y = y - 1
        elif y == y_0:
            y = y
        else:
            y = y + 1

        result.append((x,y))

    return result
        

def shift(x, y, x_shift, y_shift):
    return x + x_shift, y + y_shift

def get_zero():
   return w_screen / 2, h_screen / 2



fps = 0
trajectory = list()
trajectorys = list()
shadow = list()
shadows = list()
limiter = list()
limiters = list()
i_counter = 0
old_month = positions[0]['month']
dot = ()
controller = True

while controller:

    w_rect = obj_obstacle["width"] * SCALE  / 1000
    h_rect = obj_obstacle["height"] * SCALE / 1000
    x, y = cartesian_absolut(0, 0, w_rect, h_rect)

    obj_rect = [
        (x + w_rect, y), 
        (x, y), 
        (x, y + h_rect), 
        (x + w_rect, y + h_rect)
        ]
    coordinates_of_borde = border(obj_rect, cartesian_absolut(0,0))

    tmp_x = 0
    tmp_y = 0
    aux_x = 0
    aux_y = 0

    tmp_x = positions[i_counter]['coord_x_azimuth_shadow']
    tmp_y = positions[i_counter]['coord_y_azimuth_shadow']

    coordinates_cartesian = []
    
    # Quando for quadrante  Sudoeste
    if tmp_y < 0 and tmp_x < 0:
        
        aux_x, aux_y = coordinates_of_borde[0]
        aux_x = aux_x - 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_of_borde[1]
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_of_borde[2]
        aux_y = aux_y - 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[2]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)

        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[1]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)
        
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[0]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)
        
        coordinates_cartesian.append((aux_x, aux_y))
        
        # determina os pontos da trajetoria 
        aux_x, aux_y = coordinates_cartesian[4]
        aux_y = aux_y + h_rect / 2
        if aux_y < 0:
            aux_y = 0
        aux_x = aux_x  + w_rect / 2
        if aux_x < 0:
            aux_x = 0
        dot = (aux_x, aux_y)
            
    # Quando for quadrante Suldeste
    if  tmp_y > 0 and tmp_x < 0:
        aux_x, aux_y = coordinates_of_borde[1]
        aux_y = aux_y + 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_of_borde[2]
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_of_borde[3]
        aux_x = aux_x - 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[2]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)

        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[1]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)
        
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[0]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)
        
        coordinates_cartesian.append((aux_x, aux_y))
        
        # determina os pontos da trajetoria 
        aux_x, aux_y = coordinates_cartesian[5]
        aux_y = aux_y + h_rect / 2
        if aux_y > h_screen:
            aux_y = h_screen
        aux_x = aux_x  + w_rect / 2
        if aux_x < 0:
            aux_x = 0
        dot = (aux_x, aux_y)

    #Quando for quadrante Noroeste
    if tmp_x > 0 and tmp_y < 0:
        aux_x, aux_y = coordinates_of_borde[1]
        aux_x = aux_x + 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_of_borde[0]
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_of_borde[3]
        aux_y = aux_y - 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[2]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)

        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[1]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)
        
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[0]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)
        
        coordinates_cartesian.append((aux_x, aux_y))
        
        # determina os pontos da trajetoria 
        aux_x, aux_y = coordinates_cartesian[4]
        aux_y = aux_y + h_rect / 2
        if aux_y < 0:
            aux_y = 0
        aux_x = aux_x  - w_rect / 2
        if aux_x > w_screen:
            aux_x = w_screen
        dot = (aux_x, aux_y)
        
    # Quand for quadrante Nordeste
    if tmp_x > 0 and tmp_y > 0:
        aux_x, aux_y = coordinates_of_borde[0]
        aux_y= aux_y + 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_of_borde[3]
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_of_borde[2]
        aux_x = aux_x + 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[2]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)

        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[1]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)
        
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[0]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)
        
        coordinates_cartesian.append((aux_x, aux_y))
        
        # determina os pontos da trajetoria 
        aux_x, aux_y = coordinates_cartesian[5]
        aux_y = aux_y +  h_rect / 2
        if aux_y > h_screen:
            aux_y = h_screen
        aux_x = aux_x  - w_rect / 2
        if aux_x > w_screen:
            aux_x = w_screen
        dot = (aux_x, aux_y)
        
    #Quando for Sul
    if tmp_y == 0 and tmp_x < 0 :
        aux_x, aux_y = coordinates_of_borde[1]
        aux_y = aux_y + 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_of_borde[2]
        aux_y = aux_y - 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[1]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)

        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[0]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)
        
        coordinates_cartesian.append((aux_x, aux_y))
        
        # determina os pontos da trajetoria 
        aux_x, aux_y = coordinates_cartesian[3]
        aux_y = aux_y + h_rect / 2
        aux_x = aux_x  + w_rect / 2
        if aux_x < 0:
            aux_x = 0
        dot = (aux_x, aux_y)
            
   #Quando for Norte      
    if tmp_y == 0 and tmp_x > 0:
        aux_x, aux_y = coordinates_of_borde[0]
        aux_y = aux_y + 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_of_borde[3]
        aux_y = aux_y - 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[1]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)
        
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[0]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)
        
        coordinates_cartesian.append((aux_x, aux_y))
       
        # determina os pontos da trajetoria  
        aux_x, aux_y = coordinates_cartesian[3]
        aux_y = aux_y + h_rect / 2
        aux_x = aux_x  - w_rect / 2
        if aux_x > w_screen:
            aux_x = w_screen
        dot = (aux_x, aux_y)
        
            
   #Quando for Leste
    if tmp_x == 0 and tmp_y > 0:
        aux_x, aux_y = coordinates_of_borde[3]
        aux_x = aux_x - 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_of_borde[2]
        aux_x = aux_x + 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[1]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)

        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[0]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)
        
        coordinates_cartesian.append((aux_x, aux_y))
        
        # determina os pontos da trajetoria    
        aux_x, aux_y = coordinates_cartesian[2]
        aux_y = aux_y -  h_rect / 2
        aux_x = aux_x  + w_rect / 2
        dot = (aux_x, aux_y)
          
    #Quando for Oeste      
    if tmp_x == 0 and  tmp_y < 0:
        aux_x, aux_y = coordinates_of_borde[0]
        aux_x = aux_x - 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_of_borde[1]
        aux_x = aux_x + 1
        coordinates_cartesian.append((aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[1]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)

        coordinates_cartesian.append( (aux_x, aux_y))

        aux_x, aux_y = coordinates_cartesian[0]
        aux_x, aux_y = cartesian_relative(tmp_x, tmp_y, aux_x, aux_y)
        
        coordinates_cartesian.append((aux_x, aux_y))
        
        # determina os pontos da trajetoria     
        aux_x, aux_y = coordinates_cartesian[2]
        aux_y = aux_y + h_rect / 2
        aux_x = aux_x  + w_rect / 2
        dot = (aux_x, aux_y)   
            
    #Quando estiver à pino
    if tmp_x == 0 and tmp_y == 0:
       coordinates_cartesian = coordinates_of_borde

    

    #if tmp_y < 0:
        # aux_x, aux_y = coordinates_cartesian[3]
        # limiter.append((aux_x, aux_y))
        #aux_x, aux_y = coordinates_cartesian[4]
        #limiter.append((aux_x, aux_y))
   # else:
        # aux_x, aux_y = coordinates_cartesian[4]
        # limiter.append((aux_x, aux_y))
        #aux_x, aux_y = coordinates_cartesian[5]
        #limiter.append((aux_x, aux_y)) 
  
    

    # # texto
    month = positions[i_counter]['month']
    # day = positions[i_counter]['day']
    # h, m, s = positions[i_counter]['time']

    # la, lo = location
    # msg_1 = f'Local: (la: {la}), (lo: {lo})'
    # msg_2 = f'Mês: {month} / Dia: {day} / Hora: {h}:{m}:{s}'
    

    # text_formated = font_h2.render(msg_1, True, WHITE)
    # screen.blit(text_formated, (25, 10))

    # text_formated = font_h1.render(msg_2, True, WHITE)
    # screen.blit(text_formated, (25, 25))

    # pygame.display.update()

    # # Set a velocidade da simulação
    # time.sleep(v_simulation)
    # # Limpa as matrizes de dados
    # coordinates_cartesian = []
    # coordinates_of_borde = []

    trajectory.append(dot)
    shadow.append(coordinates_cartesian)

    if month == 1 or month == 7:
        limiter.append(dot)

    if i_counter < (len(positions)-1):
        i_counter = i_counter + 1

        month = positions[i_counter]['month']

        if old_month != month:
            trajectorys.append(trajectory)
            limiters.append(limiter)
            shadows.append(shadow)
            trajectory = []
            limiter = []
            shadow = []

        old_month = month

    else:
        trajectorys.append(trajectory)
        controller = False

while True:

    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    grid(GRAY_DARK, int(SCALE / 10))
    grid(GRAY, SCALE)

    pygame.draw.rect(screen, RED, (x, y, w_rect, h_rect))

    # for shadow in shadows:
    #     for coord in shadow:
    #         pygame.draw.polygon(screen, BLUE_DARK, coord)

    # Cria os pontos da trajetória
    w_elipse = 4
    h_elipse = 4
    for trajectory in trajectorys:
        for dot in trajectory:
            aux_x, aux_y = dot
            pygame.draw.ellipse(screen, BLUE, (aux_x - w_elipse / 2, aux_y - h_elipse / 2, w_elipse, h_elipse))


    controller = False
    dot_last = ()

    for limiter in limiters:
        for dot in limiter:
            aux_x, aux_y = dot
            pygame.draw.ellipse(screen, GREEN, (aux_x - w_elipse / 2, aux_y - h_elipse / 2, w_elipse, h_elipse))    

            if controller:
                pygame.draw.line(screen, GREEN_DARK, dot_last, dot, 1)
                dot_last = dot

            else:
                dot_last = dot
                controller = True

        controller = False

    pygame.display.update()