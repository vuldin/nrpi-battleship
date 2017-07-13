import random
import time
import pygame
import requests
import json
import sys, traceback

from pygame.locals import *
from sense_hat import SenseHat

pygame.init()
pygame.display.set_mode((400, 400))
sense = SenseHat()
#sense.low_light = True

# variables 
global seaColor
global boatColor
global hitColor
global missColor
global unkownColor
seaColor = [14, 26, 203]
boatColor = [243, 243, 243]
hitColor = [255, 153, 0]
missColor = [0, 0, 0]
unknownColor = [25, 25, 25]
global x #led position
global y
global score
x = 0
y = 0
score = 0
global thiscolor
thiscolor = unknownColor

s = seaColor
b = boatColor
h = hitColor
m = missColor
u = unknownColor
mySea = [
s, s, s, s, s, s, s, s,
s, s, s, s, s, s, s, s,
b, s, s, s, s, s, b, s,
b, s, s, s, s, s, b, s,
b, s, s, s, s, s, b, s,
b, s, s, s, s, s, s, s,
s, s, b, b, b, s, s, s,
s, s, s, s, s, s, b, b
]
enemySea = [
u, u, u, u, u, u, u, u,
u, u, u, u, u, u, u, u,
u, u, u, u, u, u, u, u,
u, u, u, u, u, u, u, u,
u, u, u, u, u, u, u, u,
u, u, u, u, u, u, u, u,
u, u, u, u, u, u, u, u,
u, u, u, u, u, u, u, u
]

# main
def main():
  global x
  global y
  global score
  global thiscolor

  try:
    # while there are still unsunken boats
    # TODO
    while True:  
      for event in pygame.event.get():
        if event.type == KEYDOWN:
          sense.set_pixel(x, y, thiscolor[0], thiscolor[1], thiscolor[2])
          #thiscolor = sense.get_pixel(x, y)

          if event.key == K_DOWN and y < 7:
              y = y + 1
          elif event.key == K_UP and y > 0:
              y = y - 1
          elif event.key == K_RIGHT and x < 7:
              x = x + 1
          elif event.key == K_LEFT and x > 0:
              x = x - 1
          elif event.key == K_RETURN:
            print(str(x) + ' ' + str(y))
            payload= {"x": x, "y": y, "player": "p1" }
            r = requests.post('https://amantestemail.mybluemix.net/shot/', data = payload)
            shotResult = r.json()
            jsonArr = json.dumps(shotResult)
            result = shotResult['res']
            print(result)
            
            # translate coords to sea position
            your_position = (y*8)+x

            if result == 'hit':
              enemySea[your_position] = hitColor
            if result == 'crazy??':
              print('already a hit')
            elif enemySea[your_position] == seaColor:
              enemySea[your_position] = seaColor

            sense.set_pixels(enemySea)

          thiscolor = sense.get_pixel(x, y)

        sense.set_pixel(x, y, 0, 255, 0) #colour of pixel for location target
  except KeyboardInterrupt:
    print ("shutdown requested... exiting")
    sense.clear()
  except Exception:
    traceback.print_exc(file=sys.stdout)
  sys.exit(0)
          
  print ('game over')
  sense.show_message("game over", text_colour=[0, 255, 255], scroll_speed=0.07)
  sense.show_message(str(score), text_colour=[0, 200, 255])

  # TODO if ships are still floating
  if True:
    print ('well done')
    sense.show_message("well done", text_colour=[0, 255, 255])
    time.sleep(3)
  else:
    print ("better luck next time")

# loop
play_game = True

### add main def and play again###
while play_game == True:
  play_again = 1
  time.sleep(1)

  sense.set_pixels(enemySea)
  time.sleep(1)

  ### Begin the main game ###
  main()

  ### Play again? ###
  print ('Would you like to play again?')
    
  sense.load_image("choice.png")

  while play_again == 1:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == K_DOWN:
          play_again = 0
          play_game = False
          print ('goodbye')
          break

        elif event.key == K_UP:
          play_again = 0
