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

global returnCount
returnCount = 0

# get my ships
payload = { "p": "p2" }
r = requests.post('https://amantestemail.mybluemix.net/givemeships', data = payload)
mySeaRes = r.json()
mySeaCoords = json.dumps(mySeaRes)

myBoatLocs = []
for coord in mySeaRes:
  myBoatLocs.append((coord['y']*8)+coord['x'])

mySea = [
s, s, s, s, s, s, s, s,
s, s, s, s, s, s, s, s,
s, s, s, s, s, s, s, s,
s, s, s, s, s, s, s, s,
s, s, s, s, s, s, s, s,
s, s, s, s, s, s, s, s,
s, s, s, s, s, s, s, s,
s, s, s, s, s, s, s, s
]
for idx, loc in enumerate(mySea):
  for boatLoc in myBoatLocs:
    if idx == boatLoc:
      mySea[idx] = b

print ('ships received')
sense.set_pixels(mySea)
time.sleep(2)
sense.clear()

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
  global returnCount

  try:
    # while we haven't clicked the return 3 times in a row
    while returnCount < 3:  
      for event in pygame.event.get():
        if event.type == KEYDOWN:
          sense.set_pixel(x, y, thiscolor[0], thiscolor[1], thiscolor[2])

          if event.key == K_DOWN and y < 7:
            returnCount = 0
            y = y + 1
          elif event.key == K_UP and y > 0:
            returnCount = 0
            y = y - 1
          elif event.key == K_RIGHT and x < 7:
            returnCount = 0
            x = x + 1
          elif event.key == K_LEFT and x > 0:
            returnCount = 0
            x = x - 1
          elif event.key == K_RETURN:
            returnCount = returnCount + 1
            print(returnCount)
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
            elif result == 'miss':
              enemySea[your_position] = seaColor
            elif result == 'crazy??':
              enemySea[your_position] = hitColor
              print('already a hit')
            else:
              print('unknown response: ' + result)
            sense.set_pixels(mySea)
            time.sleep(2)
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
