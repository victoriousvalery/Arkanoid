import pygame
import sys
from colours import *
from screen import *


class Button(object):

   def __init__(self, text):
      self.text = text
      self.is_hover = False
      self.default_color = (100,100,100)
      self.hover_color = (255,255,255)
      self.font_color = (0,0,0)
      self.obj = None
      
   def label(self):
      font = pygame.font.SysFont('Helvetica', 25)
      return font.render(self.text, 1, self.font_color)
      
   def color(self):
      if self.is_hover:
         return self.hover_color
      else:
         return self.default_color
         
   def draw(self, screen, rectcoord, labelcoord):
      self.obj  = pygame.draw.rect(screen, self.color(), rectcoord)
      screen.blit(self.label(), labelcoord)
      
      #менять цвет, если навели мышку
      #self.check_hover(mouse)
      
   def check_hover(self):
      if self.obj.collidepoint(mouse):
         self.is_hover = True 
      else:
         self.is_hover = False
