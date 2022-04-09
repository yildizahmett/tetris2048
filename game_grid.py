import os
import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
import numpy as np  # fundamental Python module for scientific computing
import copy as cp  # the copy module is used for copying tetrominos
from tile import Tile  # the class for modeling the tiles
from lib.picture import Picture  # used for displaying images
from lib.color import Color # used for coloring the game grid
from point import Point  # used for tile positions
from utils import get_next_display_dict
from tetromino import Tetromino  # the class for modeling the tetrominos

# Class used for modelling the game grid
class GameGrid:
	# Constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w, info_w, game_speed, best_score, game_type):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      self.info_width = info_w
      self.game_width = self.grid_width + self.info_width
      # set the game type as the given argument
      self.game_type = game_type
      # set the game speed as the given argument
      self.game_speed = game_speed
      # set the best score as the given argument
      self.best_score = best_score
      # create a tile matrix to store the tiles landed onto the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # create the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      #create the next tetromino that is to be moved on the game grid
      self.next_tetromino = None
      # the game_over flag shows whether the game is over or not
      self.game_over = False
      # set the color used for the empty grid cells
      self.empty_cell_color = Color(206, 195, 181)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(185, 171, 158) 
      self.boundary_color = Color(132, 122, 113)
      # thickness values used for the grid lines and the boundaries
      self.line_thickness = 0.005
      self.box_thickness = 2.5 * self.line_thickness
      self.info_line_thickness = 3 * self.line_thickness
      # set the score to 0
      self.score = 0

   # Method used for displaying the game grid
   def display(self):
      # clear the background to empty_cell_color
      stddraw.clear(self.empty_cell_color)
      # draw the game grid
      self.draw_grid()
      # draw the current/active tetromino if it is not None (the case when the 
      # game grid is updated)
      if self.current_tetromino is not None:
         self.current_tetromino.draw()
         # ghost tetromino for help the user in game modes easy and medium
         if self.game_type != "hard":
            self.ghost_tetromino() 
      self.score = Tile.merge_tiles(self.tile_matrix, self.score)
      # draw the score and the next tetromino
      self.draw_info()
      # draw a box around the game grid 
      self.draw_boundaries()
      # show the resulting drawing with a pause duration = 250 ms
      stddraw.show(self.game_speed)
         
   # Method for drawing the cells and the lines of the game grid
   def draw_grid(self):
      # for each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            # draw the tile if the grid cell is occupied by a tile
            if self.tile_matrix[row][col] is not None:
               self.tile_matrix[row][col].draw(Point(col, row))
      # draw the inner lines of the grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()  # reset the pen radius to its default value            
      
   # Method for drawing the boundaries around the game grid 
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible 
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness)
      # the coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      # set pen radius for info box boundaries
      stddraw.setPenRadius(self.info_line_thickness)
      stddraw.rectangle(self.grid_width - 0.5, pos_y, self.info_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value
   
   # Method for drawing the score and the next tetromino
   def draw_info(self):
      # info grid settings
      stddraw.setPenColor(Color(167, 160, 151))
      stddraw.filledRectangle(self.grid_width - 0.5, -0.5, self.info_width, self.grid_height)
      info_center_x_scale = (self.grid_width + self.info_width / 2) - 0.5
      info_score_y_scale = (self.grid_height - 2)
      # draw the score
      stddraw.setPenColor(Color(255, 255, 255))
      stddraw.setFontFamily("Arial")
      stddraw.setFontSize(25)
      stddraw.boldText(info_center_x_scale, info_score_y_scale, "Score")
      stddraw.boldText(info_center_x_scale, info_score_y_scale - 0.75, str(self.score))
      # draw the best score
      stddraw.setFontSize(15)
      stddraw.boldText(info_center_x_scale, info_score_y_scale - 2, "Best Score")
      stddraw.boldText(info_center_x_scale, info_score_y_scale - 2.50, str(self.best_score))
      # draw the next tetromino
      stddraw.boldText(info_center_x_scale, 5, "Next")
      if self.next_tetromino is not None:
         next_display = cp.deepcopy(self.next_tetromino)
         next_display.bottom_left_cell = Point()
         tile_next_display = get_next_display_dict(self.grid_width)
         next_display.bottom_left_cell.x  = tile_next_display[next_display.type]['x']
         next_display.bottom_left_cell.y  = tile_next_display[next_display.type]['y']
         next_display.draw()

      # Stop Game button
      stddraw.setPenColor(self.boundary_color)
      stddraw.filledRectangle(self.grid_width + 0.5, self.grid_height / 2 + 1, self.info_width - 2, 1)
      stddraw.setPenColor(Color(255, 255, 255))
      stddraw.setFontFamily("Arial")
      stddraw.setFontSize(20)
      stddraw.boldText(self.grid_width + 2, self.grid_height / 2 + 1.5, "Stop")
      # Pause Game button
      stddraw.setPenColor(self.boundary_color)
      stddraw.filledRectangle(self.grid_width + 0.5, self.grid_height / 2 - 0.25, self.info_width - 2, 1)
      stddraw.setPenColor(Color(255, 255, 255))
      stddraw.setFontFamily("Arial")
      stddraw.setFontSize(20)
      stddraw.boldText(self.grid_width + 2, self.grid_height / 2 + 0.25, "Pause")

      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has 
         # most recently been left-clicked  
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the stop button
         if mouse_x >= self.grid_width + 0.5 and mouse_x <= self.grid_width + self.info_width - 1.5:
            if mouse_y >= self.grid_height / 2 + 1 and mouse_y <= self.grid_height / 2 + 2:
               self.game_over = True
         # check if these coordinates are inside the pause button
         if mouse_x >= self.grid_width + 0.5 and mouse_x <= self.grid_width + self.info_width - 1.5:
            if mouse_y >= self.grid_height / 2 - 0.25 and mouse_y <= self.grid_height / 2 + 0.75:
               self.pause_game_screen()

   # Method used for checking whether the grid cell with given row and column 
   # indexes is occupied by a tile or empty
   def is_occupied(self, row, col):
      # considering newly entered tetrominoes to the game grid that may have 
      # tiles with position.y >= grid_height
      if not self.is_inside(row, col):
         return False
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] is not None
      
   # Method used for checking whether the cell with given row and column indexes 
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   # Method that locks the tiles of the landed tetromino on the game grid while
   # checking if the game is over due to having tiles above the topmost grid row.
   # The method returns True when the game is over and False otherwise.
   def update_grid(self, tiles_to_lock, blc_position):
      # necessary for the display method to stop displaying the tetromino
      self.current_tetromino = None
      # lock the tiles of the current tetromino (tiles_to_lock) on the game grid 
      n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
      for col in range(n_cols):
         for row in range(n_rows):            
            # place each tile onto the game grid
            if tiles_to_lock[row][col] is not None:
               # compute the position of the tile on the game grid
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               # the game is over if any placed tile is above the game grid
               else:
                  self.game_over = True
      # return the game_over flag
      return self.game_over

   # clearing lines of the game grid
   def clear_tiles(self):
      row = 0
      while(row < self.grid_height):
         # check if the row is full
         if all(self.tile_matrix[row]):
            for element in self.tile_matrix[row]:
               self.score += element.number
            # remove the row from the game grid
            self.tile_matrix = np.delete(self.tile_matrix, row, 0)
            # add an empty row to the game grid
            self.tile_matrix = np.insert(self.tile_matrix, -1, None, 0)
         else:
            row += 1

   # draws the ghost tetromino on the game grid
   def ghost_tetromino(self):
      # the ghost tetromino is the same as the current tetromino, but with a 
      # different color
      ghost_tetromino = cp.deepcopy(self.current_tetromino)
      while ghost_tetromino.can_be_moved("down", self):
         ghost_tetromino.move("down", self)
      ghost_tetromino.draw(True)
                        
   # Method that displays the pause screen
   def pause_game_screen(self):
      # colors used for the menu
      background_color = Color(42, 69, 99)
      button_color = Color(25, 255, 228)
      text_color = Color(31, 160, 239)
      # clear the background canvas to background_color
      stddraw.clear(background_color)
      # get the directory in which this python code file is placed
      current_dir = os.path.dirname(os.path.realpath(__file__))
      # path of the image file
      img_file = current_dir + "/images/menu_image.png"
      # center coordinates to display the image
      img_center_x, img_center_y = (self.game_width - 1) / 2, self.grid_height - 5
      # image is represented using the Picture class
      image_to_display = Picture(img_file)
      # display the image
      stddraw.picture(image_to_display, img_center_x, img_center_y)
      # dimensions of the start game button
      button_w, button_h = 5, 1.5
      # coordinates of the bottom left corner of the start game button 
      button_blc_x, button_blc_y = img_center_x - button_w / 2, self.grid_height - 12
      # display the continue button as a filled rectangle
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
      # display the text on the continue button
      stddraw.setFontFamily("Arial")
      stddraw.setFontSize(25)
      stddraw.setPenColor(text_color)
      text_to_display = "Continue"
      stddraw.text(img_center_x, button_blc_y + 0.75, text_to_display)
      
      # pause screen iteration
      while True:
         # display the menu and wait for a short time (50 ms)
         stddraw.show(50)
         if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            if key_typed == "p":
               break
         # check if the mouse has been left-clicked on the button
         if stddraw.mousePressed():
            # get the x and y coordinates of the location at which the mouse has 
            # most recently been left-clicked  
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside the button
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
               if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                  # return to the game
                  break