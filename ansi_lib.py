import os
from sys import stdout, stdin

'''
ansi_lib.py is a collection of classes and functions that implement many
of the ANSI Escape Code functionality for VT100 terminals. It is designed
to replace libraries such as the curses and msvcrt libraries. It is 
cross-platform compatible and less dependent on native-code libraries.

With this "module", you can control many aspects of the command-line terminal
such as color, cursor position, erasing the terminal, or parts of the terminal
and printing text to the screen at any position.

The code itself was written to be understandable for those just learning to
code and, therefore, it is not necessarily "pythonic", nor optimized for speed
or space.

Copyright 2022, Jason Fletcher and DevPipeline, LLC
'''

pref = '\033['
os.system("")

class fg: 
   black = "30"
   red = "31"
   green = "32"
   yellow = "33"
   blue = "34"
   magenta = "35"
   cyan = "36"
   white = "37"

class bg:
   black = "40"
   red = "41"
   green = "42"
   yellow = "43"
   blue = "44"
   magenta = "45"
   cyan = "46"
   white = "47"

class text:
   bold = '1'
   dim = '2'
   underline = '4'
   blink = '5'    # Doesn't seem to work on MacBook Pro
   reverse = '7'
   hidden = '8'
   # double_height_top = '#3'
   # double_height_bottom = '#4'
   # single_width = '#5'
   # double_width = '#6'

class erase:
   line_right = '0K'
   line_left = '1K'
   line = '2K'
   screen_down = '0J'
   screen_up = '1J'
   screen = '2J'

class cursor:
   up = 'A'
   down = 'B'
   right = 'C'
   left = 'D'
   home = 'H'  # Upper left of screen
   reverse_linefeed = 'I'
   hide = '?25l'
   show = '?25h' 

def rgb(r, g, b): return f'{pref}48;2;{r};{g};{b}m'

def set_font(*attrs):
   # You may have any number of parameters passed to this function
   # and those parameters will be combined into a list of attributes.
   # attrs is the list of attributes
   # Example usage: 
   #     set_font(fg.green, bg.white, text.bold)
   # attrs => [fg.green, bg.white, text.bold]
   if len(attrs) > 0:
      print_code(';'.join(attrs) + 'm')

def set_color(color):
   set_font(color=color)

'''
Hides the cursor in the terminal. 
If you call this function, make sure to call show_cursor() just prior to exiting the program. Otherwise, the cursor
will remain hidden in the terminal until restarting the terminal.
'''
def hide_cursor():
   print_code(cursor.hide)

'''
Shows the cursor in the terminal
'''
def show_cursor():
   print_code(cursor.show)

cursor_directions = { 'u':cursor.up,'d':cursor.down,'r':cursor.right,'l':cursor.left, 'up':cursor.up, 'down': cursor.down, 'right':cursor.right, 'left':cursor.left }

'''
Moves the cursor {n} lines or spaces in the {direction} specified.

n: Any number from 1 to the width or height of the screen
direction: one of 'u' | 'up' | 'd' | 'down' | 'r' | 'right' | 'l' | 'left'
'''
def move_cursor(n, direction):
   d = cursor_directions[direction.lower()]
   print_code(f'{n}{d}')

'''
Writes a {line} of text to the terminal at the current cursor location
and in a given {color}.
After printing the line, this function will reset the font attributes
to default
'''
def writeln(line, color=None):
   if color:
      set_color(color)
   stdout.write(f'{line}')
   if color: 
      reset()
   stdout.flush()

'''
Writes a {line} of text to the terminal starting at the position specified
by {row} and {col}.
'''
def addstr(row, col, line):
   goto(row, col)
   stdout.write(f'{line}')
   stdout.flush()

'''
Moves the cursor to the next line downwards
'''
def next_line():
   print_code('1E')

'''
Moves the cursor to the previous line upwards
'''
def prev_line():
   print_code('1F')

'''
Moves the cursor to the {col} specified, maintaining the current row
'''
def set_col(col):
   print_code(f'{col}G')

'''
Moves the cursor to the specified {row}, {col}. The upper left is 0,0
'''
def goto(row, col):
   print_code(f'{row};{col}H')

'''
Executes the Escape Code by printing the <ESC> prefix first, then
code passed to it.
'''
def print_code(code):
   stdout.write(f'{pref}{code}')
   stdout.flush()

'''
Deletes the line on which the cursor is located
'''
def deleteln():
   print_code(erase.line)

'''
Resets the font colors and attributes to the default
'''
def reset(): 
   print_code('0m')

'''
Clears the entire console screen
'''
def clear():
   print_code('2J')


# set_font(fg.blue, bg.white, text.bold)

# print("Hello World")

# reset()