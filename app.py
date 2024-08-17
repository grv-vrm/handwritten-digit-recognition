import pygame, sys
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2

BOUNDARYINC = 5
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

IMAGESAVE = False

MODEL = load_model("bestmodel.keras")

LABELS = {0:"zero",1:"one", 2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine"}

# initialize our pygame
pygame.init()

FONT = pygame.font.Font("FreeSansBold.ttf",18)
DISPLAYSURF=pygame.display.set_mode((300,400))

pygame.display.set_caption("Digit Board")

iswriting = False
number_xcord = []
number_ycord = []
imag_cnt=1
predict=True

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION and iswriting:
            xcord,ycord = event.pos
            pygame.draw.circle(DISPLAYSURF, WHITE,(xcord, ycord), 4, 0)
            number_xcord.append(xcord)
            number_ycord.append(ycord)
        if event.type == MOUSEBUTTONDOWN:
            iswriting = True
        if event.type == MOUSEBUTTONUP:
            iswriting = False
            number_xcord= sorted(number_xcord)
            number_ycord = sorted(number_ycord)
            rect_min_x, rect_max_x = max(number_xcord[0]-BOUNDARYINC, 0), min(300, number_xcord[-1]+BOUNDARYINC)
            rect_min_y, rect_max_y = max(number_ycord[0]-BOUNDARYINC, 0), min(number_ycord[-1]+BOUNDARYINC,400)
            number_xcord =[]
            number_ycord =[]
            img_arr = np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)
            if IMAGESAVE:
                cv2.imwrite("image.png")
                imag_cnt +=1
            if predict:
                image = cv2.resize(img_arr, (28,28))
                image = np.pad(image, (10,10), 'constant', constant_values = 0)
                image = cv2.resize(image, (28,28))/255
                label = str(LABELS[np.argmax(MODEL.predict(image.reshape(1,28,28,1)))])
                textSurface = FONT.render(label, True, RED, WHITE)
                textRecObj = textSurface.get_rect()
                textRecObj.midtop = (rect_min_x + (rect_max_x-rect_min_x)//2, rect_min_y - 30)
                DISPLAYSURF.blit(textSurface, textRecObj)
                pygame.draw.rect(DISPLAYSURF, RED, (rect_min_x, rect_min_y, rect_max_x-rect_min_x, rect_max_y-rect_min_y), 2)
        if event.type == KEYDOWN:
            if event.unicode =="n":
                DISPLAYSURF.fill(BLACK)
    pygame.display.update()