import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid # the class for modeling the game grid
from tetromino import Tetromino # the class for modeling the tetrominoes
import random # used for creating tetrominoes with random types/shapes

# MAIN FUNCTION OF THE PROGRAM
#----------------------------------------------------------------------
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

   # read the best score from the file
   best_score = read_best_score()
   # set the dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w
   # create the game grid
   grid = GameGrid(grid_h, grid_w, info_w, game_speed, best_score, game_type)
   # create the first tetromino to enter the game grid
   # by using the create_tetromino function defined below
   current_tetromino = create_tetromino(grid_h, grid_w)
   grid.current_tetromino = current_tetromino
   # create the next tetromino to enter the game grid
   # by using the create_tetromino function defined below
   next_tetromino = create_tetromino(grid_h, grid_w)
   grid.next_tetromino = next_tetromino
   # the main game loop (keyboard interaction for moving the tetromino)
   while True:
      # check user interactions via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
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
         elif key_typed == "d":
            # hard drop: causes the tetromino to fall down to the bottom
            current_tetromino.rotate_tetromino(key_typed, grid)
         elif key_typed == "a":
            # rotate the active tetromino counter-clockwise
            current_tetromino.rotate_tetromino(key_typed, grid)
         elif key_typed == "space":
            # hard drop: causes the tetromino to fall down to the bottom
            while current_tetromino.can_be_moved("down", grid):
               current_tetromino.move("down", grid)
         elif key_typed == "p":
            # pause the game
            grid.pause_game_screen()
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
         grid.update_grid(tiles, pos)
         game_over = grid.game_over
         # game over menu
         if game_over:
            save_best_score(grid.score)
            is_restarted = game_over_screen(grid_h, game_w, grid.score)
            if is_restarted:
               best_score = read_best_score()
               grid = GameGrid(grid_h, grid_w, info_w, game_speed, best_score, game_type)
            else:
               start() # returns the main menu
         # check if any row is filled and clear this rows
         grid.clear_tiles()
         # assign the next tetromino to the current tetromino
         # by using the create_tetromino function defined below
         current_tetromino = next_tetromino
         grid.current_tetromino = current_tetromino
         # create the next tetromino that will used the next time
         next_tetromino = create_tetromino(grid_h, grid_w)
         grid.next_tetromino = next_tetromino

      # display the game grid and the current tetromino
      grid.display()
      # if stop game button is pressed, displyas the game over screen
      game_over = grid.game_over
      if game_over:
         save_best_score(grid.score)
         is_returned = stop_screen(grid_h, game_w, grid.score)
         if is_returned:
            start()

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
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 6.5
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
   button_w, button_h = grid_width - 1.5, 2
   # coordinates of the bottom left corner of the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 1.5
   # display the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Click Here to Start the Game"
   stddraw.text(img_center_x, button_blc_y + 1, text_to_display)
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

# Function promps, when the game is initialized at the first.
# It gets the values of grid @(n)x@(p) and the game speed @(speed) from the user.
# @return it returns the speed of the game, which is delay of game. And a tuple of dimensions of the wanted grid.
def prepare_screen():
   # setting default colors.
   background_color = Color(42, 69, 99); button_color = Color(25, 255, 228); text_color = Color(31, 160, 239); black_color = Color(0, 0, 0); white_color = Color(255, 255, 255)
   # creating a short method, to do conversions.
   pixelToCoordinate = lambda x, in_min, in_max, out_min, out_max : int( round( ((x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min) ) )
   # re-scaling the canvas to be able to set sliders.
   stddraw.setXscale(0,500); stddraw.setYscale(0,500)
   # grid dimensions are the values in pixel for slider.
   gridDimensions = [280,280]
   # grid dimensions are the values in real for slider.
   gridResults = [14, 20]
   # setting a default game speed.
   gameSpeed = 0
   # setting a default game type.
   game_type = ""
   # a loop that runs the window fully, it draw all neccessary elements, and gets input from the user.
   while True:
      # clearing the background, to be able to create an doubleBuffering affect on canvas
      stddraw.clear(background_color)
      # pulling boundaries of sliders.
      stddraw.setPenColor(Color(0,0,0)); stddraw.filledRectangle(280-300/2,450,300,10); stddraw.filledRectangle(280-300/2,400,300,10)
      # pulling bound-boundaries of sliders
      stddraw.setPenColor(button_color); stddraw.rectangle(280-300/2,450,300.5,10.5); stddraw.rectangle(280-300/2,400,300.5,10.5)
      # drawing the boundaries of game mode options
      stddraw.setPenColor(Color(255,255,255)); stddraw.filledRectangle(120-75/2,315,85,50); stddraw.filledRectangle(245-75/2,315,85,50); stddraw.filledRectangle(370-75/2,315,85,50)
      # drawing the bound-boundaries of game mode options
      stddraw.setPenColor(button_color); stddraw.filledRectangle(125-75/2,320,75,40); stddraw.filledRectangle(250-75/2,320,75,40); stddraw.filledRectangle(375-75/2,320,75,40)
      # drawing text info part boundaries
      stddraw.setPenColor(Color(255,255,255)); stddraw.filledRectangle(245-350/2,55,360,230)
      # drawing text info part bound-boundaries
      stddraw.setPenColor(button_color); stddraw.filledRectangle(250-350/2,60,350,220)
      # setting drawer. and putting a line in info part with black color
      stddraw.setFontFamily("Arial"); stddraw.setFontSize(14); stddraw.setPenColor(white_color); stddraw.line(100,252.5,400,252.5)
      # drawing game info
      stddraw.setPenColor(black_color); stddraw.boldText(250,265,"Welcome to Tetris 2048 !"); stddraw.boldText(250,240,"< To Play > Press -"); stddraw.boldText(250,215,"Left and Right Arrow buttons to"); stddraw.boldText(250,200,"- Move tetromino left and right"); stddraw.boldText(250,175,"Down arrow button to"); stddraw.boldText(250,160,"- Move tetromino down faster"); stddraw.boldText(250,135,"\"Space\" to - Directly fall tetromino"); stddraw.boldText(250,110,"\"A\" and \"D\" to"); stddraw.boldText(250,95,"Rotate tetromino clockwise and c-clockwise"); stddraw.boldText(250,70,"\"P\" to - Pause the game")
      # drawing the texts of game mod buttons
      stddraw.setPenColor(black_color); stddraw.boldText(125,340,"EASY"); stddraw.boldText(250,340,"MEDIUM"); stddraw.boldText(375,340,"HARD")
      # drawing slider circles boundaries
      stddraw.setPenColor(background_color); stddraw.filledCircle(gridDimensions[0],455,18); stddraw.filledCircle(gridDimensions[1],405,18)
      # drawing slider circle inside
      stddraw.setPenColor(Color(255,255,255)); stddraw.filledCircle(gridDimensions[0],455,15);stddraw.filledCircle(gridDimensions[1],405,15)
      # drawing sliders definers text
      stddraw.setFontSize(14); stddraw.boldText(100,457,"Width :"); stddraw.boldText(100,407,"Height :")
      # drawing sliders circles text
      stddraw.setFontSize(16); stddraw.setPenColor(Color(0,0,0)); stddraw.text(gridDimensions[0],455,str(int(gridResults[0]))); stddraw.text(gridDimensions[1],405,str(int(gridResults[1])))
      # showing results, with the most less value
      stddraw.show(10)
      # mouse press check, to find where mouse is"
      if stddraw.mousePressed():
         # getting mouse position after check
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # catching the game type option and slider buttons
         if   ((mouse_x >= 125-75/2 and mouse_x <= 125-75/2 + 40) and (mouse_y >= (320) and mouse_y <= (320) + 40)): gameSpeed = 400; game_type = "easy";   return gameSpeed, tuple(gridResults), game_type
         elif ((mouse_x >= 250-75/2 and mouse_x <= 250-75/2 + 40) and (mouse_y >= (320) and mouse_y <= (320) + 40)): gameSpeed = 250; game_type = "medium"; return gameSpeed, tuple(gridResults), game_type
         elif ((mouse_x >= 375-75/2 and mouse_x <= 375-75/2 + 40) and (mouse_y >= (320) and mouse_y <= (320) + 40)): gameSpeed = 150; game_type = "hard";   return gameSpeed, tuple(gridResults), game_type
         elif ((mouse_y >= (450) - 15 and mouse_y <= (450) + 20)  and (mouse_x >= 280-300/2 and mouse_x <= 280-300/2 + 300)) : gridDimensions[0] = (mouse_x); gridResults[0] = pixelToCoordinate(mouse_x,130,430,8,20 )
         elif ((mouse_y >= (400) - 15 and mouse_y <= (400) + 20   and (mouse_x >= 280-300/2 and mouse_x <= 280-300/2 + 300))): gridDimensions[1] = (mouse_x); gridResults[1] = pixelToCoordinate(mouse_x,130,430,16,24)

# Function for displaying the game over screen
def game_over_screen(grid_h, game_w, current_score):
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
   img_center_x, img_center_y = (game_w - 1) / 2, grid_h - 5
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
   button_w, button_h = game_w - 6, 1.5
   # coordinates of the bottom left corner of the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 2.75
   # display game over text
   stddraw.setPenColor(button_color)
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(80)
   game_over_text = "Game Over!"
   stddraw.boldText(img_center_x, (button_blc_y + img_center_y) / 2, game_over_text)
   # display the current score text
   stddraw.setFontSize(40)
   stddraw.text(img_center_x, (button_blc_y + img_center_y) / 2 - 1.5, "Your score: " + str(current_score))

   # display the restart game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the restart game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Restart the Game"
   stddraw.text(img_center_x, button_blc_y + 0.75, text_to_display)

   # display the return main button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y - 2, button_w, button_h)
   # display the text on the return menu button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Return to Main Menu"
   stddraw.text(img_center_x, button_blc_y - 1.25, text_to_display)
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
               return True # return True to indicate that the game should be restarted

         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y - 2 and mouse_y <= button_blc_y - 2 + button_h:
               return False # return False to indicate that the game should be returned to the main menu

# Function for displaying the stop game screen
def stop_screen(grid_h, game_w, current_score):
   # colors used for the stop screen
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
   img_center_x, img_center_y = (game_w - 1) / 2, grid_h - 5
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
   button_w, button_h = game_w - 6, 1.5
   # coordinates of the bottom left corner of the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 2.75
   # display game over text
   stddraw.setPenColor(button_color)
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(70)
   game_stopped_text = "Game Stopped!"
   stddraw.boldText(img_center_x, (button_blc_y + img_center_y) / 2, game_stopped_text)
   # display the current score text
   stddraw.setFontSize(40)
   stddraw.text(img_center_x, (button_blc_y + img_center_y) / 2 - 2, "Your score: " + str(current_score))

   # display the restart game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the restart game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Return the Main Menu"
   stddraw.text(img_center_x, button_blc_y + 0.75, text_to_display)
   # stop screen iteration loop
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
               return True # return True to indicate that the game should be restarted

# Function for save best score
def save_best_score(best_score):
   # if the best score is already saved in the binary file :)
   # then the best score is updated
   if os.path.exists("best_score.bin"):
      with open("best_score.bin", "rb") as file:
         # read the best score from the binary file
         bit_string = ""
         byte = file.read(1)
         while len(byte) > 0:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)
         old_score = int(bit_string, 2)
         # if the new score is greater than the old score
         # then the new score is saved in the binary file
         if best_score > old_score:
            with open("best_score.bin", "wb") as file:
               best_score_bits = "{0:032b}".format(best_score)
               b = bytearray()
               for i in range(0, len(best_score_bits), 8):
                  one_byte = best_score_bits[i:i+8]
                  b.append(int(one_byte, 2))
               file.write(bytes(b))
   # if the best score is not saved yet
   # then saave the current score as best score
   else:
      # write the best score to the binary file
      with open("best_score.bin", "wb") as file:
         best_score_bits = "{0:032b}".format(best_score)
         b = bytearray()
         for i in range(0, len(best_score_bits), 8):
            one_byte = best_score_bits[i:i+8]
            b.append(int(one_byte, 2))
         file.write(bytes(b))

# read the best score from the binary file
def read_best_score():
   # if the best score is already saved in the binary file :)
   # read the best score from the binary file and return it
   # if the best score is not saved yet, return 0
   if os.path.exists("best_score.bin"):
      with open("best_score.bin", "rb") as file:
         bit_string = ""
         byte = file.read(1)
         while len(byte) > 0:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)

         best_score = int(bit_string, 2)
         return best_score
   else:
      return 0

# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__== '__main__':
   start()
