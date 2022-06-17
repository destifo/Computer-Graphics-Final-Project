import pygame
import random
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import numpy as np


class Backgroundimage:
     def __init__(self):
        start = Start(vertex="bg.vertex.shader",fragment="bg.fragment.shader")
        self.Bgvertexes = np.array([
        # position          # color           # texture s, r
        [1, 1, 0,    1.0, 0.20, 0.8, 1.0, 1.0],
        [1, -1, 0,   1.0, 1.0, 0.0, 1.0, 0.0],
        [-1, 1, 0,   0.0, 0.7, 0.2, 0.0, 1.0],

        [1, -1, 0,   1.0, 1.0, 0.0, 1.0, 0.0],
        [-1, -1, 0,  0.0, 0.4, 1.0, 0.0, 0.0],
        [-1, 1, 0,   0.0, 0.7, 0.2, 0.0, 1.0],

    ], dtype=np.float32)

        self.Bgvao = glGenVertexArrays(1)
        self.Bgvbo = glGenBuffers(1)
        glBindVertexArray(self.Bgvao)

        glBindBuffer(GL_ARRAY_BUFFER, self.Bgvbo)

        glBufferData(GL_ARRAY_BUFFER, self.Bgvertexes.nbytes, self.Bgvertexes, GL_STATIC_DRAW)
        positionLocation = glGetAttribLocation(start.program, "position")
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                            8 * self.Bgvertexes.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        colorLocation = glGetAttribLocation(start.program, "color")
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                            8 * self.Bgvertexes.itemsize, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        textureLocation = glGetAttribLocation(start.program, "texCoord")
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                            8 * self.Bgvertexes.itemsize, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
 
        glBindVertexArray(0)
        self.tex = Texture("textures/bg3.png")
       
        
class Texture:
    def __init__(self,tex):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        image = pygame.image.load(tex).convert_alpha()
        image_width,image_height = image.get_rect().size
        img_data = pygame.image.tostring(image,'RGBA')
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image_width,image_height,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data)
        glGenerateMipmap(GL_TEXTURE_2D)













def init():
    pygame.init()
    display = (500, 750)
    display = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 500,750,0)
    return display


game_over = False
bg_img = pygame.image.load('background.jpg')
# bird_img = pygame.image.load('bird1.png')
# raw_data = bird_img.get_buffer().raw
# data = np.frombuffer(raw_data, np.uint8)

display = init()
clock = pygame.time.Clock()

#Bird Object
def draw_bird(x, y, w, h, img):
    # raw_data = img.get_buffer().raw
    # data = np.fromstring(raw_data, np.uint8)
    Texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, Texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB,GL_UNSIGNED_BYTE, img_data)
    glEnable(GL_TEXTURE_2D)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, Texture)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslate(x, y, 0)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex(0, 0, 0)

    glTexCoord2f(0, 1)
    glVertex(w, 0, 0)

    glTexCoord2f(1, 1)
    glVertex(w, h, 0)

    glTexCoord2f(1, 0)
    glVertex(0, h, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glFlush()


bird_x = 50
bird_y = 300
yint_change = 0
img = Image.open('bird1.png')
img_data = img.tobytes("raw", "RGB", 0, -1)


while not game_over:
    clock.tick(60)
    display.fill((0, 0, 0))

    # display2 = pygame.display.set_mode((500, 750))

    display.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                yint_change = -5
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                yint_change = 3

    bird_y += yint_change
    draw_bird(bird_x, bird_y, img.size[0], img.size[1], img_data)

    pygame.display.flip()


pygame.quit()