import pygame, os, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

mainSurface = pygame.display.set_mode((800, 600))
pygame.display.set_caption('trenca-joanes');
black = pygame.Color(0, 0, 0)

bat = pygame.image.load('bat.png')
playerY = 540
batRect = bat.get_rect()
mousex, mousey = (0, playerY)

SPEED = 7
ball = pygame.image.load('ball.png')
ballRect = ball.get_rect()
ballStartY = 300
ballSpeed = SPEED
ballServed = False
bx, by = (24, ballStartY)
sx, sy = (ballSpeed, ballSpeed)
ballRect.topleft = (bx, by)
level = 1

lifes = 5
heart = pygame.image.load('heart.jpg')

letra30 = pygame.font.SysFont("Arial", 30)
brick = pygame.image.load('brick.png')

def draw_bricks():
    bricks = []
    broken_bricks = []
    for y in range(10 if level%10 == 0 else level%10): #5
        brickY = (y * 24) + 120
        for x in range(11): #22
            brickX = (x * 35) + 210 
            width = brick.get_width()
            height = brick.get_height()
            rect = Rect(brickX, brickY, width, height)
            bricks.append(rect)
    return bricks, broken_bricks
bricks, broken_bricks = draw_bricks()

broken_brick = pygame.image.load('brock.png')

while True:
    mainSurface.fill(black)

    # brick draw
    for b in bricks:
        mainSurface.blit(brick, b)
    
    for i in range(lifes):
        mainSurface.blit(heart, (50+(i*70),30))
        
    # brick draw
    for bb in broken_bricks:
        mainSurface.blit(broken_brick, bb)

    # bat and ball draw
    mainSurface.blit(ball, ballRect)
    mainSurface.blit(bat, batRect)
    imagenTextoPresent = letra30.render(f"NIVEL {level}", True, (200,200,200), (0,0,0))
    mainSurface.blit(imagenTextoPresent, (630,30))
    
    # events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
            if (mousex < 800 - 55):
                batRect.topleft = (mousex, playerY)
            else:
                batRect.topleft = (800 - 55, playerY)
        elif event.type == MOUSEBUTTONUP and not ballServed:
            ballServed = True
            
    # main game logic 
    if ballServed:
        bx += sx
        by += sy
        ballRect.topleft = (bx, by)

    if (by <= 0):
        by = 0
        sy *= -1
    if (by >= 600 - 8):
        ballServed = False
        bx, by = (24, ballStartY)
        sx, sy = (SPEED, SPEED)
        ballRect.topleft = (bx, by)
        lifes -= 1
    if (bx <= 0):
        bx = 0
        sx *= -1
    if (bx >=800 - 8):
        bx = 800 - 8
        sx *= -1
        
    if ballRect.colliderect(batRect):
        by = playerY - 8
        sy *= -1
        sx = ((bx+4)-batRect.center[0])/3
        
    # brick collision detection
    brickHitIndex = ballRect.collidelist(bricks)
    
    # broken brick collision detection
    bbrickHitIndex = ballRect.collidelist(broken_bricks)
    
    if brickHitIndex >= 0:
        hb = bricks[brickHitIndex]
        if level%2 == 0:
            broken_bricks.append(hb)
        mx = bx + 4
        my = by + 4
        if mx > hb.x + hb.width or mx < hb.x:
            sx *= -1
        else:
            sy *= -1
        del (bricks[brickHitIndex])
    
    if bbrickHitIndex >= 0 and level%2 == 0:
        hbb = broken_bricks[bbrickHitIndex]
        bmx = bx + 4
        bmy = by + 4
        if bmx > hbb.x + hbb.width or bmx < hbb.x:
            sx *= -1
        else:
            sy *= -1
        del (broken_bricks[bbrickHitIndex])
    
    if lifes == 0:
        pygame.quit()
        sys.exit()
    
    if len(bricks) == 0 and len(broken_bricks) == 0:
        level += 1
        lifes += 1
        SPEED += 1
        if SPEED >= 18:
            SPEED = 18
        ballServed = False
        bx, by = (24, ballStartY)
        sx, sy = (SPEED, SPEED)
        ballRect.topleft = (bx, by)
        bricks, broken_bricks = draw_bricks()
        
    pygame.display.update()
    fpsClock.tick(60)