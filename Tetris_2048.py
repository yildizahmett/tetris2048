import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid # the class for modeling the game grid
from tetromino import Tetromino # the class for modeling the tetrominoes
import random # used for creating tetrominoes with random types/shapes

# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution
def start():
   # fake set the size of the window for centering game grid canvas
   stddraw.setCanvasSize(800, 800)
   # set main window canvas
   stddraw.setCanvasSize(500, 500)
   # set the scale of the coordinate system
   stddraw.setXscale(-0.5, 16.5)
   stddraw.setYscale(-0.5, 15.5)
   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   display_game_menu(16, 17)
   # set game settings
   game_speed, grid_results, game_type = prepare_screen()

   # set the dimensions of the game grid
   grid_h, grid_w = grid_results[1], grid_results[0]
   info_w = 5 # do not change this value
   game_w = grid_w + info_w
   box_radius = 40 # do not change this value
   # set the size of the drawing canvas
   canvas_h, canvas_w = box_radius * grid_h, box_radius * game_w
   # set the game grid canvas
   stddraw.setCanvasSize(canvas_w, canvas_h)
   # set the scale of the coordinate system
   stddraw.setXscale(-0.5, game_w - 0.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)

   # set the dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w

   # create the game grid
   grid = GameGrid(grid_h, grid_w)
   # create the first tetromino to enter the game grid
   # by using the create_tetromino function defined below
   current_tetromino = create_tetromino(grid_h, grid_w)
   grid.current_tetromino = current_tetromino

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   display_game_menu(grid_h, grid_w + 10)

   # the main game loop (keyboard interaction for moving the tetromino)
   while True:
      # check user interactions via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
         print(key_typed)
         # if the left arrow key has been pressed
         if key_typed == "left":
            # move the active tetromino left by one
            current_tetromino.move(key_typed, grid)
         # if the right arrow key has been pressed
         elif key_typed == "right":
            # move the active tetromino right by one
            current_tetromino.move(key_typed, grid)
         # if the down arrow key has been pressed
         elif key_typed == "down":
            # move the active tetromino down by one
            # (soft drop: causes the tetromino to fall down faster)
            current_tetromino.move(key_typed, grid)
         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

      # move the active tetromino down by one at each iteration (auto fall)
      success = current_tetromino.move("down", grid)

      # place the active tetromino on the grid when it cannot go down anymore
      if not success:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)
         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles, pos)
         # end the main game loop if the game is over
         if game_over:
            break
         # Check if the
         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         current_tetromino = create_tetromino(grid_h, grid_w)
         grid.current_tetromino = current_tetromino

      # display the game grid and the current tetromino
      grid.display()

   # print a message on the console when the game is over
   print("Game over")

# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
   # type (shape) of the tetromino is determined randomly
   tetromino_types = [ 'I', 'O', 'Z' ]
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
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
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
   button_w, button_h = grid_width - 1.5, 2
   # coordinates of the bottom left corner of the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # display the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Click Here to Start the Game"
   stddraw.text(img_center_x, 5, text_to_display)
   # menu interaction loop
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the button
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has
         # most recently been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break # break the loop to end the method and start the game

# Function for displaying the preparing menu
def prepare_screen():

   background_color = Color(42, 69, 99); button_color = Color(25, 255, 228); text_color = Color(31, 160, 239)

   pixelToCoordinate = lambda x, in_min, in_max, out_min, out_max : int( round((x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min) )

   scale = 500
   stddraw.setXscale(0,scale)
   stddraw.setYscale(0,scale)

   gridDimensions = [280,280]
   gridResults = [14, 20]

   gameSpeed = 160
   game_type = ""
   while True:
      stddraw.clear(background_color)
      stddraw.setPenColor(Color(0,0,0))
      stddraw.filledRectangle(280-300/2,450,300,10)
      stddraw.filledRectangle(280-300/2,400,300,10)

      stddraw.setPenColor(button_color)
      stddraw.rectangle(280-300/2,450,300.5,10.5)
      stddraw.rectangle(280-300/2,400,300.5,10.5)

      stddraw.setPenColor(Color(255,255,255))
      stddraw.filledRectangle(120-75/2,315,85,50)
      stddraw.filledRectangle(245-75/2,315,85,50)
      stddraw.filledRectangle(370-75/2,315,85,50)

      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(125-75/2,320,75,40)
      stddraw.filledRectangle(250-75/2,320,75,40)
      stddraw.filledRectangle(375-75/2,320,75,40)

      stddraw.setPenColor(Color(255,255,255))
      stddraw.filledRectangle(245-350/2,55,360,230)

      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(250-350/2,60,350,220)

      stddraw.setFontFamily("Arial")
      stddraw.setFontSize(16)
      stddraw.setPenColor(Color(0,0,0))

      stddraw.boldText(125,340,"EASY")
      stddraw.boldText(250,340,"MEDIUM")
      stddraw.boldText(375,340,"HARD")

      stddraw.setPenColor(background_color)
      stddraw.filledCircle(gridDimensions[0],455,18)
      stddraw.filledCircle(gridDimensions[1],405,18)
      stddraw.setPenColor(Color(255,255,255))
      stddraw.filledCircle(gridDimensions[0],455,15)
      stddraw.filledCircle(gridDimensions[1],405,15)
      stddraw.setFontSize(14)
      stddraw.boldText(100,457,"Width :")
      stddraw.boldText(100,407,"Height :")
      stddraw.setFontSize(16)
      stddraw.setPenColor(Color(0,0,0))
      stddraw.text(gridDimensions[0],455,str(int(gridResults[0])))
      stddraw.text(gridDimensions[1],405,str(int(gridResults[1])))

      stddraw.show(50)

      if stddraw.mousePressed():

         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()

         if mouse_x >= 280-300/2 and mouse_x <= 280-300/2 + 300:
               if (mouse_y >= (450) - 15 and mouse_y <= (450) + 20):
                  gridDimensions[0] = (mouse_x)
                  gridResults[0] = pixelToCoordinate(mouse_x,130,430,8,20)
               if (mouse_y >= (400) - 15 and mouse_y <= (400) + 20):
                  gridDimensions[1] = (mouse_x)
                  gridResults[1] = pixelToCoordinate(mouse_x,130,430,16,24)


         if (mouse_y >= (320) and mouse_y <= (320) + 40) :
               if (mouse_x >= 125-75/2 and mouse_x <= 125-75/2 + 40):
                  gameSpeed = 400
                  game_type = "easy"
               if (mouse_x >= 250-75/2 and mouse_x <= 250-75/2 + 40):
                  gameSpeed = 250
                  game_type = "medium"
               if (mouse_x >= 375-75/2 and mouse_x <= 375-75/2 + 40):
                  gameSpeed = 150
                  game_type = "hard"

               if (gameSpeed != 0) :
                  return gameSpeed, tuple(gridResults), game_type

# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__== '__main__':
   start()
