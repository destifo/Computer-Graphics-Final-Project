from operator import index
import pipes
from pprint import pp
import random as random
from sys import flags
from turtle import pos
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from OpenGL.GL.shaders import *
import numpy as np
import os
from PIL import Image
class Start:
    def __init__(self,vertex,fragment):
        
        pygame.init()

        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
        pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        display = (500, 500)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        
        glClearColor(0.30, 0.20, 0.20, 1.0)
        glViewport(0, 0, 500, 500)

        vertex_shader_content = self.getFileContents(vertex)
        fragment_shader_content = self.getFileContents(fragment)

        vertex_shader = compileShader(vertex_shader_content, GL_VERTEX_SHADER)
        fragment_shader = compileShader(
            fragment_shader_content, GL_FRAGMENT_SHADER)

        self.program = glCreateProgram()
        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program)
       
        glUseProgram(self.program)
        
    def getFileContents(self,filename):
        p = os.path.join(os.getcwd(), "shaders", filename)
        return open(p, 'r').read()
class Bird:
     def __init__(self):
        start = Start(vertex="bg.vertex.shader",fragment="bg.fragment.shader")
        self.birdVertexes = np.array([
        # position          # color           # texture s, r
        [-0.6, 0.1, 0,    1.0, 0.20, 0.8, 1.0, 1.0],
        [-0.6, -0.1, 0,   1.0, 1.0, 0.0, 1.0, 0.0],
        [-0.8, 0.1, 0,   0.0, 0.7, 0.2, 0.0, 1.0],

        [-0.6, -0.1, 0,   1.0, 1.0, 0.0, 1.0, 0.0],
        [-0.8, -0.1, 0,  0.0, 0.4, 1.0, 0.0, 0.0],
        [-0.8, 0.1, 0,   0.0, 0.7, 0.2, 0.0, 1.0],

    ], dtype=np.float32)

        self.birdVao = glGenVertexArrays(1)
        self.birdVbo = glGenBuffers(1)
        glBindVertexArray(self.birdVao)

        glBindBuffer(GL_ARRAY_BUFFER, self.birdVbo)

        glBufferData(GL_ARRAY_BUFFER, self.birdVertexes.nbytes, self.birdVertexes, GL_STATIC_DRAW)
        positionLocation = glGetAttribLocation(start.program, "position")
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                            8 * self.birdVertexes.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        colorLocation = glGetAttribLocation(start.program, "color")
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                            8 * self.birdVertexes.itemsize, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        textureLocation = glGetAttribLocation(start.program, "texCoord")
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                            8 * self.birdVertexes.itemsize, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
 
        glBindVertexArray(0)
        self.tex = Texture("textures/bird3.png")
     def update(self,x=0,y=0): 
        self.birdVertexes[0][0]+=x
        self.birdVertexes[1][0]+=x
        self.birdVertexes[2][0]+=x
        self.birdVertexes[3][0]+=x
        self.birdVertexes[4][0]+=x
        self.birdVertexes[5][0]+=x
        self.birdVertexes[0][1]+=y      
        self.birdVertexes[1][1]+=y       
        self.birdVertexes[2][1]+=y       
        self.birdVertexes[3][1]+=y   
        self.birdVertexes[4][1]+=y   
        self.birdVertexes[5][1]+=y   
        glBindBuffer(GL_ARRAY_BUFFER, self.birdVbo)   
        glBufferData(GL_ARRAY_BUFFER, self.birdVertexes.nbytes, self.birdVertexes, GL_STATIC_DRAW)
       
class Pipe:
    def __init__(self,translate=(0,0)):
        start = Start(vertex="bg.vertex.shader",fragment="bg.fragment.shader")
        self.translate = translate
        self.pipeVertex = np.array([
        [1.0, 0.2, 0.0, 0.0, 1.0, 0.0,0,0],
        [1.0, 2.0, 0.0, 0.0, 1.0,0.0,0,1],
        [1.2, 2.0, 0.0, 0.0, 1.0, 0.0,1,1],
        [1.2, 0.2, 0.0, 0.0, 1.0, 0.0,1,0],], dtype=np.float32)
       
        self.pipeVertex =  np.array([
        [1.0+translate[0], 0.2+translate[1], 0.3, 0.0, 1.0, 0.5,0.0,0.0],
        [1.0+translate[0], 2.0+translate[1], 0.3, 0.0, 1.0,0.5,0.0,1.0    ],
        [1.2+translate[0], 2.0+translate[1], 0.3, 0.0, 1.0, 0.5,1.0,1.0 ],
        [1.2+translate[0], 0.2+translate[1], 0.3, 0.0, 1.0, 0.5,1.0,0.0],], dtype=np.float32)
        self.pipeIndices=np.array([0,1,2,
                       0,3,2 ],dtype=np.int32)
        self.pipeVAO = glGenVertexArrays(1)

        glBindVertexArray(self.pipeVAO)
    
        self.pipeVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.pipeVBO)
        glBufferData(GL_ARRAY_BUFFER, self.pipeVertex.nbytes, self.pipeVertex, GL_STATIC_DRAW)
   

        self.indexVBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indexVBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.pipeIndices.nbytes, self.pipeIndices, GL_STATIC_DRAW)
    
        positionLocation = glGetAttribLocation(start.program, "position")
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                            8 * self.pipeVertex.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
 
        colorLocation = glGetAttribLocation(start.program, "color")
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                            8 * self.pipeVertex.itemsize, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        textureLocation = glGetAttribLocation(start.program, "texCoord")
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                            8 * self.pipeVertex.itemsize, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
 
        glBindVertexArray(0)
        self.tex = Texture("textures/pipe.jpg")
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
    def update(self,x=0,y=0):
        self.pipeVertex[0][0]+=x
        self.pipeVertex[1][0]+=x
        self.pipeVertex[2][0]+=x
        self.pipeVertex[3][0]+=x
        self.pipeVertex[0][1]+=y      
        self.pipeVertex[1][1]+=y       
        self.pipeVertex[2][1]+=y       
        self.pipeVertex[3][1]+=y   
        glBindBuffer(GL_ARRAY_BUFFER, self.pipeVBO)   
        glBufferData(GL_ARRAY_BUFFER, self.pipeVertex.nbytes, self.pipeVertex, GL_STATIC_DRAW)




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


prev_block_pos = 0
y=round(random.uniform(-0.60, 0.60), 2)
pipe = Pipe(translate=(-0.5,0.05+y))
pipe2= Pipe(translate=(-0.5,-2.25+y))
pipes = [pipe,pipe2]

def check_collision(bird_pos, x, blocks_y_pos):
    left_x = x[0]
    right_x = x[1]
    upper_y_limit = blocks_y_pos[0]
    lower_y_limit = blocks_y_pos[1]
    bird_left_x = bird_pos[0][0]
    bird_right_x = bird_pos[0][1]
    bird_up_y = bird_pos[1][0]
    bird_down_y = bird_pos[1][1]
    print(bird_right_x)
    print(bird_left_x, left_x, right_x)
    if (bird_right_x >= left_x and bird_right_x <= right_x) or (bird_left_x >= left_x and bird_left_x <= right_x):
        print(bird_up_y, upper_y_limit)
        print(bird_down_y, lower_y_limit)
        if (bird_down_y <= lower_y_limit):
            print('lower check works')
            return True
        if (bird_up_y >= upper_y_limit):
            print('upper check works')
            return True
        
    return False
    
pipe_len = 2

def main():
    global prev_block_pos, pipe_len
    a=-0.005
    b=-0.006
    bg = Backgroundimage()
    bird = Bird()
    while True:
        y=round(random.uniform(-0.60, 0.60), 2)
        prev_block_pos += 2
        if (prev_block_pos % 500 == 0):
            pipe = Pipe(translate=(-0.5,0.05+y))
            pipe2= Pipe(translate=(-0.5,-2.25+y))
            pipes.append(pipe)
            pipes.append(pipe2)  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.update(0,0.15)
                    pass
        glClear(GL_COLOR_BUFFER_BIT)
        start = Start(vertex="bg.vertex.shader",fragment="bg.fragment.shader")
        glBindVertexArray(bg.Bgvao)
        glBindTexture(GL_TEXTURE_2D, bg.tex.texture)

        glDrawArrays(GL_TRIANGLES, 0, 6)

        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)
        glBindVertexArray(bird.birdVao)
        glBindTexture(GL_TEXTURE_2D, bird.tex.texture)
        bird.update(0,b)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)
        
        
        # start = Start(vertex="triangle.vertex.shader",fragment="triangle.fragment.shader")
        for i in pipes:
            glBindVertexArray(i.pipeVAO)
            glBindTexture(GL_TEXTURE_2D, i.tex.texture)
            i.update(a,0)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)



