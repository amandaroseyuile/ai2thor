impoArt json
from PIL import Image
from ai2thor.controller import Controller
import math

def MoveArmLinear(relMovementX, relMovementY, relMovementZ, vidFrame):
    # 30 (29.97) FPS
    # max arm movement per second = .075, max arm movement per frame = .0025
    step_size = 0.05

    if relMovementX >= 0:
        directionX = 1
    else:
        directionX = -1

    if relMovementY >= 0:
        directionY = 1
    else:
        directionY = -1

    if relMovementZ >= 0:
        directionZ = 1
    else:
        directionZ = -1


    maxRelMovement = max( abs(relMovementX), abs(relMovementY), abs(relMovementZ) )
    steps = math.floor( maxRelMovement / step_size )
    #print("%d steps of size %f to get to %f" % (steps, step_size, max(abs(relMovementX), abs(relMovementY), abs(relMovementZ))))
    #print(steps)
    if steps:
        if abs(relMovementX) == maxRelMovement:
            stepX = directionX * step_size
            stepY = directionY * step_size * ( relMovementY / maxRelMovement )
            stepZ = directionZ * step_size * ( relMovementZ / maxRelMovement )
        elif abs(relMovementY) == maxRelMovement:
            stepX = directionX * step_size * ( relMovementX / maxRelMovement )
            stepY = directionY * step_size
            stepZ = directionZ * step_size * ( relMovementZ / maxRelMovement )
        else:
            stepX = directionX * step_size * ( relMovementX / maxRelMovement )
            stepY = directionY * step_size * ( relMovementY / maxRelMovement )
            stepZ = directionZ * step_size
    else:
        stepX = 0
        stepY = 0
        stepZ = 0

    i = 0
    for i in range(steps):

        #print(stepX, stepY, stepZ)    
        c.step(
            action = "MoveArm",
            position = dict(x=stepX, y=stepY, z=stepZ), 
            coordinateSpace = "wrist",
            #speed = .075,#how fast arm moves in meters per second
            #fixedDeltaTime = .033#the interval in seconds with which physics is simulated
        )

        # center camera:
        Image.fromarray(c.last_event.third_party_camera_frames[0]).save("scripts/centerCam/centerCam_" + str(vidFrame) + ".png")

        # left camera:                                                                                                                                                 
        Image.fromarray(c.last_event.third_party_camera_frames[1]).save("scripts/leftCam/leftCam_" + str(vidFrame) + ".png")

        # right camera:                                                                                                                                               
        Image.fromarray(c.last_event.third_party_camera_frames[2]).save("scripts/rightCam/rightCam_" + str(vidFrame) + ".png")
        
        i = i + 1
        vidFrame = vidFrame + 1


    # Calculate final "remainder" movement, if necessary
    stepX = relMovementX - stepX * steps
    stepY = relMovementY - stepY * steps
    stepZ = relMovementZ - stepZ * steps    
    if stepX or stepY or stepZ:
        #print(stepX, stepY, stepZ)            
        c.step(
            action = "MoveArm",
            position = dict(x = relMovementX - stepX * steps,
                            y = relMovementY - stepY * steps,
                            z = relMovementZ - stepZ * steps), 
            coordinateSpace = "wrist",
            speed = .075,#how fast arm moves in meters per second
            fixedDeltaTime = .033#the interval in seconds with which physics is simulated
        )
                        
        # center camera:
        Image.fromarray(c.last_event.third_party_camera_frames[0]).save("scripts/centerCam/centerCam_" + str(vidFrame) + ".png")

        # left camera:                                                                                                                                                 
        Image.fromarray(c.last_event.third_party_camera_frames[1]).save("scripts/leftCam/leftCam_" + str(vidFrame) + ".png")
        
        # right camera:                                                                                                                                               
        Image.fromarray(c.last_event.third_party_camera_frames[2]).save("scripts/rightCam/rightCam_" + str(vidFrame) + ".png")   
                    
        vidFrame = vidFrame + 1                        
    return vidFrame


c = Controller(
    local_executable_path = "unity/builds/thor-OSXIntel64-local/thor-OSXIntel64-local.app/Contents/MacOS/AI2-THOR",
    agentMode = "arm",
    scene = "FloorPlan_ExpRoom",
    width = 1600,
    height = 900,
    renderDepthImage = False
    )

event = c.step(
    action="Teleport",
    position = dict(x=-.329, y=.9009, z=-.936),
    rotation = dict(x=0, y=0, z=0),
    forceAction = True
    )

# center camera
c.step(
    action = "AddThirdPartyCamera",
    position = dict(x=-.5,y=1.25, z=1.011),
    rotation = dict(x=180, y=0, z=180),
    fieldOfView = 60
    )

# left camera
c.step(
    action = "AddThirdPartyCamera",
    position = dict(x=.25, y=1.5, z=1.5),
    rotation = dict(x=160, y=25, z=185),
    fieldOfView = 60
    )

# right camera
c.step(
    action = "AddThirdPartyCamera",
    position = dict(x=-1, y=1.5, z=1.5),
    rotation = dict(x=160, y=-25, z=185),
    fieldOfView = 60
    )

assetList = json.load(open("scripts/assetList.json"))
totalNumPairs = 1

for i in range(totalNumPairs):

    obj = assetList["availableObjects"][i]
    cover = assetList["availableCovers"][i]
    
    # teleport object to correct location
    c.step(
        action = "PlaceObjectAtPoint",
        objectId = obj["objectId"],
        position = dict(
            x = obj["x"],
            y = obj["y"],
            z = obj["z"]
            )
        )

    # teleport cover to correct locaction
    # assumption: cover is placed in from of agent's arm/hand
    c.step(
        action = "PlaceObjectAtPoint",
        objectId = cover["objectId"],
        position = dict(
            x = cover["x"],
            y = cover["y"],
            z = cover["z"]
            ),
        rotation = dict(
            x = 180,
            y = 0,
            z = 0
            )
        )

    vidFrame = 0
    
    # center camera:                                                                                                                                                   
    Image.fromarray(c.last_event.third_party_camera_frames[0]).save("scripts/centerCam/centerCam_" + str(vidFrame) + ".png")

    # left camera:
    Image.fromarray(c.last_event.third_party_camera_frames[1]).save("scripts/leftCam/leftCam_" + str(vidFrame) + ".png")
    
    # right camera:                                                                                                                                                    
    Image.fromarray(c.last_event.third_party_camera_frames[2]).save("scripts/rightCam/rightCam_" + str(vidFrame) + ".png")

    vidFrame = vidFrame + 1

    event = c.step(
        action = "PickupObject"
    )
    
    # center camera:                                                                                                                                                   
    Image.fromarray(c.last_event.third_party_camera_frames[0]).save("scripts/centerCam/centerCam_" + str(vidFrame) + ".png")

    # left camera:                                                                                                                                                     
    Image.fromarray(c.last_event.third_party_camera_frames[1]).save("scripts/leftCam/leftCam_" + str(vidFrame) + ".png")

    # right camera:                                                                                                                                                  
    Image.fromarray(c.last_event.third_party_camera_frames[2]).save("scripts/rightCam/rightCam_" + str(vidFrame) + ".png")

    vidFrame = vidFrame + 1
    
    vidFrame = MoveArmLinear(0, .25, 0, vidFrame)

    vidFrame = MoveArmLinear(-.33, 0, 0, vidFrame)

    vidFrame = MoveArmLinear(0, -.25, 0, vidFrame)

    vidFrame = MoveArmLinear(-.25, 0, 0, vidFrame)

    vidFrame = MoveArmLinear(0, .25, 0, vidFrame)


    # create video
    
