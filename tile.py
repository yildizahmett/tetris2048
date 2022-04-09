import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
import random # random is used to generate random numbers
import numpy as np # numpy is used to generate arrays
from lib.color import Color  # used for coloring the tile and the number on it
from utils import TILE_COLORS # used for the tile colors

# Class used for modeling numbered tiles as in 2048
class Tile: 
   # Class attributes shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.004
   # font family and size used for displaying the tile number
   font_family, font_size = "Arial", 14

   # Constructor that creates a tile with 2 as the number on it
   def __init__(self):
      random_numbers = [2, 4]
      # set the number on the tile
      self.number = random_numbers[random.randint(0, len(random_numbers) - 1)]
      # set the boundary color of the tile
      self.box_color = Color(132, 122, 113) # box (boundary) color
      # set the colors of the tile
      self.update_color()

      #  Method for updating the number on the tile according to the number
   def update_color(self):
      self.background_color = TILE_COLORS[self.number]['background_color']
      self.foreground_color = TILE_COLORS[self.number]['foreground_color']

   # Method for drawing the tile
   def draw(self, position, length = 1, is_ghost = False):
      # draw the ghost tile
      if is_ghost:
         stddraw.setPenColor(Color(167, 160, 151))
         stddraw.filledSquare(position.x, position.y, length / 2)
         stddraw.setPenColor(self.background_color)
         stddraw.setPenRadius(Tile.boundary_thickness)
         stddraw.square(position.x, position.y, length / 2)
         stddraw.setPenRadius()  # reset the pen radius to its default value
         # draw the number on the tile
         stddraw.setPenColor(Color(255, 255, 255))
         stddraw.setFontFamily(Tile.font_family)
         stddraw.setFontSize(Tile.font_size)
         stddraw.text(position.x, position.y, str(self.number))
      # draw the tile
      else:
         stddraw.setPenColor(self.background_color)
         stddraw.filledSquare(position.x, position.y, length / 2)
         stddraw.setPenColor(self.box_color)
         stddraw.setPenRadius(Tile.boundary_thickness)
         stddraw.square(position.x, position.y, length / 2)
         stddraw.setPenRadius()  # reset the pen radius to its default value
         # draw the number on the tile
         stddraw.setPenColor(self.foreground_color)
         stddraw.setFontFamily(Tile.font_family)
         stddraw.setFontSize(Tile.font_size)
         stddraw.text(position.x, position.y, str(self.number))

   # Method for checking two tiles for merging
   def merge_matches(self, tile):
   # if the number on the tile is equal to the number on the current tile
      if self.number == tile.number and self.number < 2048:
         # set the number on the current tile to the sum of the two numbers
         self.number = self.number * 2
         # increase the score by the value of the number on the current tile
         # Remove the tile and update the color of the current tile
         tile.number = None

         # Update the color of the current tile
         self.update_color()
         # return True to indicate that the tiles were matched
         return self.number
      # return False to indicate that the tiles were not matched
      else:
         return 0

   # match the tiles if the number is equal
   def merge_matches(self, tile):
      # if the number on the tile is equal to the number on the current tile
      if self.number == tile.number:
         # set the number on the current tile to the sum of the two numbers
         self.number *= 2
         # set the number on the tile to None
         tile.number = None
         # return True to indicate that the tiles were matched
         return True
      # return False to indicate that the tiles were not matched
      return False