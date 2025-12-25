import pygame


# setting up window and clock
pygame.init()
window = pygame.display.set_mode((600,600))
pygame.display.set_caption("Hitbox Test")
TestClock = pygame.time.Clock()


# loading and preparing images, setting player start position
sourceImage1 = pygame.image.load('Assets/TestSprite1.png').convert_alpha()
sourceImage2 = pygame.image.load('Assets/TestSprite2.png').convert_alpha()
sourceImage3 = pygame.transform.flip(sourceImage2, True, False)

sourceImage4 = pygame.image.load('Assets/TestSprite3.png').convert_alpha()
sourceImage5 = pygame.image.load('Assets/TestSprite4.png').convert_alpha()
sourceImage6 = pygame.image.load('Assets/TestSprite5.png').convert_alpha()

PlayerSprite1 = pygame.transform.scale_by(sourceImage1, 3)
PlayerSprite2 = pygame.transform.scale_by(sourceImage2, 3)
PlayerSprite3 = pygame.transform.scale_by(sourceImage3, 3)

PlayerSprite4 = pygame.transform.scale_by(sourceImage4, 3)
PlayerSprite5 = pygame.transform.scale_by(sourceImage5, 3)
PlayerSprite6 = pygame.transform.scale_by(sourceImage6, 3)

PlayerSpritesDown = [PlayerSprite1, PlayerSprite2, PlayerSprite3]
PlayerSpritesRight = [PlayerSprite4, PlayerSprite5, PlayerSprite6]
PlayerPosition = [20,20]


# rect object as player hitbox. Used to aling player movement stops
PlayerHitBoxPosition = [20, 83]
PlayerHitBox = pygame.Rect(PlayerHitBoxPosition[0], PlayerHitBoxPosition[1], 48, 9)


# player right movement stop
PlayerRightMoveStopPos = [69 , 83]
PlayerRightMoveStop = pygame.Rect(PlayerRightMoveStopPos[0], PlayerRightMoveStopPos[1], 1, 9)


# test hitbox to collide against
TestHitBox = pygame.Rect(90, 20, 90, 90)

# variable for keeping track of what spriteset to use
SpriteSetToUse = str("Down")

# preparing background
window.fill('white')


# walk animation lenght in frames and current animation frame
walkAnimFrames = 6
walkAnimCurrentFrame = 0


# variable for stopping movement on collision
firstCollision = False
RightMoveStopped = False


# walking animation
def walk(walkFuncArg):
    # declaring global variable use
    global onSpriteNum
    global walkAnimFrames
    global walkAnimCurrentFrame
    global SpriteSetToUse
    global PlayerHitBox
    global firstCollision
    global RightMoveStopped

    # selecting walk sprites based on func arg and setting spriteset to use for rendering
    match walkFuncArg:
        case "Down":
            PlayerSprites = PlayerSpritesDown
            SpriteSetToUse = "Down"

        case "Right":
            PlayerSprites = PlayerSpritesRight
            SpriteSetToUse = "Right"

    # blocking all key events from being called
    pygame.event.set_blocked(pygame.KEYDOWN)

    # looping code when walk cycle is in progress
    while walkAnimCurrentFrame < walkAnimFrames:

        # checking which way to walk, moving player sprite, hitbox and movement stop
        match walkFuncArg:
            case "Down":
                PlayerPosition[1] += 1
                PlayerHitBox.move_ip(0, 1)
                PlayerRightMoveStop.move_ip(0, 1)

                # incrementing current sprite to display, player position and animation frame
                onSpriteNum += 1
                walkAnimCurrentFrame += 1
            case "Right":
                if RightMoveStopped == False:
                    PlayerPosition[0] += 1
                    PlayerHitBox.move_ip(1, 0)
                    PlayerRightMoveStop.move_ip(1, 0)

                    # incrementing current sprite to display, player position and animation frame
                    onSpriteNum += 1
                    walkAnimCurrentFrame += 1
                # other condition for just turning player if movement not possible. Necessary for processing input and avoid getting stuck
                elif RightMoveStopped == True:
                    onSpriteNum = 0
                    walkAnimCurrentFrame = walkAnimFrames

        # resetting animation loop
        if onSpriteNum > 2:
            onSpriteNum = 1

        # setting sprite to stand and allowing input
        if walkAnimCurrentFrame == walkAnimFrames:
            onSpriteNum = 0
            pygame.event.set_allowed(pygame.KEYDOWN)

        # checking to see if playerhitbox intersects test hitbox
        StopMovement = pygame.Rect.colliderect(PlayerRightMoveStop, TestHitBox)

        if StopMovement == True:
            # if first collision frame, let the lower if loop play out
            if firstCollision == False:
                # ending walk animation if clipping
                walkAnimCurrentFrame = walkAnimFrames
                onSpriteNum = 0
                pygame.event.set_allowed(pygame.KEYDOWN)

                # set this to true here to prevent the next frame input from lacking frames
                firstCollision = True
                RightMoveStopped = True
        else:
            firstCollision = False
            RightMoveStopped = False

        # clearing event que here to avoid looping
        pygame.event.clear()

        # rendering here aswell since this loop is separate from main program operation
        render()

        # setting the walk cycle framerate
        TestClock.tick(8)

    # setting current frame the animation is on to 0 to prepare for next animation cycle
    walkAnimCurrentFrame = 0


# rendering function
def render():
    # global variable use
    global onSpriteNum
    global SpriteSetToUse
    global PlayerSpritesDown
    global PlayerSpritesRight

    # actually choosing which spriteset to use
    match SpriteSetToUse:
        case "Down":
            PlayerSprites = PlayerSpritesDown
        case "Right":
            PlayerSprites = PlayerSpritesRight

    # doing the actual rendering
    window.fill('white')
    pygame.draw.rect(window, 'red', TestHitBox)
    pygame.draw.rect(window, 'green', PlayerHitBox)
    pygame.draw.rect(window, 'blue', PlayerRightMoveStop)
    window.blit(PlayerSprites[onSpriteNum], (PlayerPosition[0], PlayerPosition[1]))
    pygame.display.flip()


# main loop
gameActive = True
onSpriteNum = int(0)

while gameActive == True:
    # processing events
    for events in pygame.event.get():

        # keys pressed
        if events.type == pygame.KEYDOWN:

            #ClippingHitbox = pygame.Rect.colliderect(PlayerRightMoveStop, TestHitBox)

            # dowm movement key pressed
            if events.key == pygame.K_DOWN:
                walk("Down")

            # right movement key pressed
            if events.key == pygame.K_RIGHT:
                walk("Right")

        # window termination
        if events.type == pygame.QUIT:
            gameActive = False

    # calling our rendering function
    render()

    # this is the framerate the main program operates at
    TestClock.tick(20)

pygame.quit()
