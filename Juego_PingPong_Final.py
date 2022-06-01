#----------------------------------------------------------------------------------------------------------
# Libraries
#----------------------------------------------------------------------------------------------------------

#librerías para el videojuego
import time
import random
import pygame, sys
from pygame.locals import *

#librerías para el bitalino
import bitalino
import numpy as np
import time
import random



#Conexión con el bitalino
# Mac OS
# macAddress = "/dev/tty.BITalino-XX-XX-DevB"

# Windows
macAddress = "20:18:06:13:01:82"

device = bitalino.BITalino(macAddress) # se conecta bitalino con python mediante un objeto device
time.sleep(1)

acqChannels = [0, 1] #seleccionando el canal para EMG y el ECG
srate = 1000 #frecuencia de muestreo bitalino
nframes = 100 #cantidad de datos en cada muestra
threshold = 0.200 # umbral de la señal bicep 3 electrodos
threshold2 = 0.07 # umbral de la señal antebrazo 2 electrodos

# ajuste de ganancia de la medición
BITS = 10
VCC = 3.3
GAIN = 1009 #gain EMG
GAINECG = 1100 #gain ECG

device.start(srate, acqChannels) #inicia lectura de datos
print("START")


#----------------------------------------------------------------------------------------------------------
#Código para videojuego
#----------------------------------------------------------------------------------------------------------

pygame.init()
fps = pygame.time.Clock()

#----------------------------------------------------------------------------------------------------------
#     Global variables
#----------------------------------------------------------------------------------------------------------

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 20
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0

#----------------------------------------------------------------------------------------------------------
#          canvas declaration
#----------------------------------------------------------------------------------------------------------
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Juego de Ping Pong - Bitalino')

#----------------------------------------------------------------------------------------------------------
#                  funtions
#----------------------------------------------------------------------------------------------------------
# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH//2,HEIGHT//2]
    horz = random.randrange(2,4)
    vert = random.randrange(1,3)
    
    if right == False:
        horz = - horz
        
    ball_vel = [horz,-vert]

# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT//2]
    paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT//2]
    l_score = 0
    r_score = 0
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)


#draw function of canvas
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score
           
    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0],[WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel
    
    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    #update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    #draw paddles and ball
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    #ball collision check on top and bottom walls
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    #ball collison check on gutters or paddles
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,paddle1_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)
        
    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,paddle2_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        l_score += 1
        ball_init(False)

    #update scores
    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score "+str(l_score), 1, (255,255,0))
    canvas.blit(label1, (50,20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score "+str(r_score), 1, (255,255,0))
    canvas.blit(label2, (470, 20))


# keyP1 handler
def keyP1(event):
    global paddle1_vel, paddle2_vel

    if event == True:
        paddle1_vel = -8
    elif event == False:
        paddle1_vel = 8


# keyP2 handler
def keyP2(event):
    global paddle1_vel, paddle2_vel

    if event == True:
        paddle2_vel = -8
    elif event == False:
        paddle2_vel = 8



# keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel

    if event.key == K_UP:
        paddle2_vel = -8
    elif event.key == K_DOWN:
        paddle2_vel = 8
    elif event.key == K_w:
        paddle1_vel = -8
    elif event.key == K_s:
        paddle1_vel = 8


# keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel

    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0



#Introduction, how to play
def menu(dosa):
    dosa.fill(WHITE)
    #txt, only five seconds to read
    myfont1 = pygame.font.SysFont("Comic Sans MS", 50)
    label1 = myfont1.render("Ping Pong ", 1, (255,124,0))
    dosa.blit(label1, (190,0))
    pygame.display.update()
    
    myfont1 = pygame.font.SysFont("Comic Sans MS", 30)
    label1 = myfont1.render("Para este juego deberas posicionar ", 1, (0,0,0))
    dosa.blit(label1, (40,70))
    pygame.display.update()
    
    myfont1 = pygame.font.SysFont("Comic Sans MS", 30)
    label1 = myfont1.render("el brazo de forma estirada para ", 1, (0,0,0))
    dosa.blit(label1, (55,120))
    pygame.display.update()
    
    
    myfont1 = pygame.font.SysFont("Comic Sans MS", 30)
    label1 = myfont1.render("subir y de forma contraida para bajar", 1, (0,0,0))
    dosa.blit(label1, (20,170))
    pygame.display.update()
    time.sleep(5)
    
    #Start the time line dead
    dosa.fill(WHITE)    
    myfont1 = pygame.font.SysFont("Comic Sans MS", 75)
    label1 = myfont1.render("El juego inicia en:", 1, (0,0,255))
    dosa.blit(label1, (0,100))
    pygame.display.update()
    
    myfont1 = pygame.font.SysFont("Comic Sans MS", 90)
    label1 = myfont1.render("3", 1, (250,0,255))
    dosa.blit(label1, (280,190))
    pygame.display.update()
    time.sleep(1)
    
    dosa.fill(WHITE)    
    myfont1 = pygame.font.SysFont("Comic Sans MS", 75)
    label1 = myfont1.render("El juego inicia en:", 1, (0,0,255))
    dosa.blit(label1, (0,100))
    pygame.display.update()
    
    myfont1 = pygame.font.SysFont("Comic Sans MS", 90)
    label1 = myfont1.render("2", 1, (250,0,255))
    dosa.blit(label1, (280,190))
    pygame.display.update()
    time.sleep(1)
    
    dosa.fill(WHITE)    
    myfont1 = pygame.font.SysFont("Comic Sans MS", 75)
    label1 = myfont1.render("El juego inicia en:", 1, (0,0,255))
    dosa.blit(label1, (0,100))
    pygame.display.update()
    myfont1 = pygame.font.SysFont("Comic Sans MS", 90)
    label1 = myfont1.render("1", 1, (250,0,255))
    dosa.blit(label1, (280,190))
    pygame.display.update()
    time.sleep(1)

#----------------------------------------------------------------------------------------------------------
#                            Her start the main code
#----------------------------------------------------------------------------------------------------------
init()

#game start (Menu)
menu(window)


try:
    #game loop
    while True:

        draw(window)

        for event in pygame.event.get():

            if event.type == KEYDOWN:
                keydown(event)
            elif event.type == KEYUP:
                keyup(event)
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fps.tick(60)

        # actualización de datos de medición bitalino en tiempo real
        data = device.read(nframes)

        #procesamiento de los datos para los resultados del emg
        emg = (((((data[:, 5] / 2 ** BITS) - (1 / 2)) * VCC) / GAIN) * 1000)  # medición（mV）
        emg = np.abs(emg)
        max_value = np.max(emg)

        # procesamiento de los datos para los resultados del ecg
        emg2 = (((((data[:, 6] / 2 ** BITS) - (1 / 2)) * VCC) / GAINECG) * 1000)  # medición（mV）
        emg2 = np.abs(emg2)
        max_value2 = np.max(emg2)

        print('Medición EMG:')
        print(max_value2)
        print('Medición ECG como EMG')
        print(max_value2)


        #Para jugador 1 - movimiento respecto al threshol
        if max_value > threshold:
            keyP1(True)
            #print('Arriba')
        else:
            keyP1(False);
            #print('Abajo')

        #Para jugador 2 - movimiento respecto al threshol
        if max_value2 > threshold2:
            keyP2(True)
            #print('Arriba')
        else:
            keyP2(False);
            #print('Abajo')


//finalización del programa y cierre de la conexión
finally:
    print("STOP")
    device.trigger([0, 0])
    device.stop()
    device.close()