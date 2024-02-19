import pygame
from pygame.locals import *
import random
import sqlite3
from readMusic import readSong

#gets pygame module started up
pygame.init()

#sets up mixer module
pygame.mixer.init()

#sets frame rate
clock = pygame.time.Clock()
fps = 60

screenWidth = 600
screenHeight = 420

#loads background image
background = pygame.image.load("images/Bg.png")
question = pygame.image.load("images/Question.png")
question = pygame.transform.scale_by(question, 1.5)

questionRect = question.get_rect()
questionRect.centerx = screenWidth // 2
questionRect.y = 0

#creates screen and labels it 'Reggae Run'
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Reggae Run")

#defines game variables
tileSize = 30
gameOver = 0

#defines music list
usedSigs = []

def levelReset():
  global gameOver, levelDesign
  
  player.reset()

  slabGroup.empty()
  blobGroup.empty()
  spikeGroup.empty()
  tunnelGroup.empty()
  gameOver = 0

  world = World(levelDesign)

  return world

def timeSelect():
  global usedSigs
  timeSigs = ["2/4", "3/4", "4/4", "5/4", "7/4", "6/8", "9/8", "12/8"]
  correctTimeSig = None
  wrongTimeSig = None
  wrongPos = []


  #checks if all time sigs have been used
  if len(usedSigs) == len(timeSigs):
    print("All time signatures have been used.")
    used = False
  else:
    used = True
    
  while used:
    wrongPos = []
    
    #creates a possible time signature
    den = random.choice([4, 8])
    if den == 4:
      num = random.choice([2,3,4,5,7])
    else:
      num = random.choice([6,9,12])

    correctTimeSig = f"{num}/{den}"

    #checks if time signature has been used already
    if not correctTimeSig in usedSigs:
      timeSigs.remove(correctTimeSig)
      for sig in timeSigs:
        if den == 8 and (sig[2] == "8" or len(sig) == 4):
          wrongPos.append(sig)
        if den == 4 and sig[2] == "4":
          wrongPos.append(sig)
      usedSigs.append(correctTimeSig)
      used = False

  wrongTimeSig = random.choice(wrongPos)
  
  sigList = [(correctTimeSig, True), (wrongTimeSig, False)]

  readSong(correctTimeSig)

  #loads song and plays it
  pygame.mixer.music.load("currentSong.mp3")
  pygame.mixer.music.play(-1)

  
  return sigList


class Player():
  def __init__(self,x,y):
    imgL = pygame.image.load("images/PlayerL.png")
    self.image = pygame.transform.scale(imgL, (22, 45))
    self.deadImage = pygame.image.load("images/Dead.png")
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.width = self.image.get_width()
    self.height = self.image.get_height()
    self.vel_y = 0
    self.in_air = False

  def update(self, gameOver):
    imgR = pygame.image.load("images/PlayerR.png")
    imgL = pygame.image.load("images/PlayerL.png")
    dx = 0
    dy = 0
    colThresh = 15

    if gameOver == 0:
      #get spacebar press
      eventList = pygame.event.get()
      for event in eventList:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE and self.in_air == False:
            self.vel_y = -15
            self.in_air = True
      #get left and right arrow presses 
      key = pygame.key.get_pressed()
      if key[pygame.K_LEFT]:
        self.image = pygame.transform.scale(imgL, (22, 45))
        dx -= 4
      if key[pygame.K_RIGHT]:
        self.image = pygame.transform.scale(imgR, (22, 45))
        dx += 4
  
      #add gravity
      self.vel_y += 2
      if self.vel_y > 10:
        self.vel_y = 10
      dy += self.vel_y
  
      #check for collision
      for tile in world.tileList:
        #check for collision in x direction
        if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
          dx = 0
        #check for collision in y direction
        if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
          #check if below ground (jumping)
          if self.vel_y < 0:
            #distance between player and tile
            dy = tile[1].bottom - self.rect.top
            self.vel_y = 0
          #check if above ground (falling)
          elif self.vel_y >= 0:
            #distance between player and tile
            dy = tile[1].top - self.rect.bottom
            self.vel_y = 0
            self.in_air = False

      #check for collision with blobs
      if pygame.sprite.spritecollide(self, blobGroup, False):
        gameOver = -1
      #check for collision with spikes
      if pygame.sprite.spritecollide(self, spikeGroup, False):
        gameOver = -1
      #check for collision with tunnels
      if pygame.sprite.spritecollide(self, tunnelGroup, False):
        gameOver = 1

      #check for collision with moving slabs
      for slab in slabGroup:
        #check for collision in x direction
        if slab.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
          dx = 0
        #check for collison in y direction
        if slab.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
          #check if above slab or if squashed between slab and tile
          if (abs((self.rect.bottom + dy) - slab.rect.top) < colThresh) or ((abs((self.rect.top + dy) - slab.rect.bottom) < colThresh) and self.in_air == False):
            self.in_air = False
            self.vel_y = 0
            self.rect.bottom = slab.rect.top - 1
            dy = 0
          #check if below slab
          elif abs((self.rect.top + dy) - slab.rect.bottom) < colThresh:
            self.vel_y = 0
            dy = slab.rect.bottom - self.rect.top
          
  
      #update player coordinates
      self.rect.x += dx
      self.rect.y += dy

    elif gameOver == -1:
      self.image = self.deadImage
      if self.rect.y > 10:
        self.rect.y -= 5
    
    #draw player onto screen
    screen.blit(self.image, self.rect)

    return gameOver

  def reset(self):
    imgL = pygame.image.load("images/PlayerL.png")
    self.image = pygame.transform.scale(imgL, (22, 45))
    self.rect.x = 120
    self.rect.y = 230

class World():
  def __init__(self, data):
    self.tileList = []
    
    #load images
    dirtImg = pygame.image.load("images/Dirt.png")
    grassImg = pygame.image.load("images/Grass.png")
    brickImg = pygame.image.load("images/Brick.png")

    #loads 2 time signatures
    timeSigs = timeSelect()
    
    #iterates through each tile in the grid
    rowCount = 0
    for row in data:
      colCount = 0
      for tile in row:
        #Dirt block
        if tile == 1:
          #scales image to tile size
          img = pygame.transform.scale(dirtImg, (tileSize, tileSize))
          imgRect = img.get_rect()
          imgRect.x = colCount * tileSize
          imgRect.y = rowCount * tileSize
          tile = (img, imgRect, "dirt")
          self.tileList.append(tile)
        #Grass block
        if tile == 2:
          #scales image to tile size
          img = pygame.transform.scale(grassImg, (tileSize, tileSize))
          imgRect = img.get_rect()
          imgRect.x = colCount * tileSize
          imgRect.y = rowCount * tileSize
          tile = (img, imgRect, "grass")
          self.tileList.append(tile)
        #Brick block
        if tile == 3:
          #scales image to tile size
          img = pygame.transform.scale(brickImg, (tileSize, tileSize))
          imgRect = img.get_rect()
          imgRect.x = colCount * tileSize
          imgRect.y = rowCount * tileSize
          tile = (img, imgRect, "brick")
          self.tileList.append(tile)
        #Tunnel block
        if tile == 4:
          if len(timeSigs) == 2:
            choice = random.choice(timeSigs)
            timeSigs.remove(choice)
          else:
            choice = timeSigs[0]
            timeSigs.remove(choice)
          
          tunnel = Tunnel(colCount * tileSize, rowCount * tileSize - 30, choice[0], choice[1])
          tunnelGroup.add(tunnel)
        #Grass Slab block
        if tile == 5:
          slab = Slab(colCount * tileSize, rowCount * tileSize)
          slabGroup.add(slab)
        #Spike block
        if tile == 6:
          spike = Spike(colCount * tileSize, rowCount * tileSize + 15)
          spikeGroup.add(spike)
        #Blob enemy
        if tile == 7:
          blob = Blob(colCount * tileSize + 3, rowCount * tileSize + 17)
          blobGroup.add(blob)
    
        colCount += 1
      rowCount += 1
      
  def draw(self):
    for tile in self.tileList:
      screen.blit(tile[0], tile[1])

class Blob(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load("images/Blob.png")
    self.image = pygame.transform.scale(img, (20, 13))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.moveDirection = 1
    self.moveCounter = 0

  def update(self):
    self.rect.x += self.moveDirection
    self.moveCounter += 1
    if abs(self.moveCounter) > 33:
      self.moveDirection *= -1
      self.moveCounter *= -1

class Slab(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load("images/Slab.png")
    self.image = pygame.transform.scale(img, (30, 15))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.moveDirection = 1
    self.moveCounter = 0

  def update(self):
    self.rect.y += self.moveDirection
    self.moveCounter += 1
    if self.moveCounter > 90:
      self.moveDirection *= -1
      self.moveCounter = 0 

class Spike(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load("images/Spikes.png")
    self.image = pygame.transform.scale(img, (tileSize, tileSize // 2))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

class Tunnel(pygame.sprite.Sprite):
  def __init__(self, x, y, timeSig, correct):
    pygame.sprite.Sprite.__init__(self)

    #checks timSig length
    if len(timeSig) == 4:
      img = pygame.image.load(f"tunnels/{timeSig[:2]}-{timeSig[3]}.png")
    else:
      img = pygame.image.load(f"tunnels/{timeSig[0]}-{timeSig[2]}.png")
    self.image = pygame.transform.scale(img, (tileSize, tileSize * 2))
    self.correct = correct
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y


levelDesign = [
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,3,3,3,0,0,0,7,0,0,2,0,2,0,2,0,0,0,0,3],
[3,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,5,0,0,3],
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,2,3],
[3,0,0,5,3,2,2,6,6,6,6,2,6,2,6,2,2,2,1,3],
[3,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
[3,1,2,6,2,2,2,6,6,2,0,7,0,2,0,7,0,0,4,3],
[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
]

player = Player(120, 230)

slabGroup = pygame.sprite.Group()
spikeGroup = pygame.sprite.Group()
blobGroup = pygame.sprite.Group()
tunnelGroup = pygame.sprite.Group()

world = World(levelDesign)

#initialises game loop
run = True
while run:
  clock.tick(fps)

  screen.blit(background, (0,0))
  screen.blit(question, questionRect)

  world.draw()
  
  if gameOver == 0:
    slabGroup.update()
    blobGroup.update()

  slabGroup.draw(screen)
  blobGroup.draw(screen)
  spikeGroup.draw(screen)
  tunnelGroup.draw(screen)

  gameOver = player.update(gameOver)

  #checks for an event
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    elif event.type == pygame.KEYDOWN:
      if (event.key == pygame.K_r) and (gameOver in [1, -1]):
          world = levelReset()

  #updates window based on instructions
  pygame.display.update()

pygame.quit()