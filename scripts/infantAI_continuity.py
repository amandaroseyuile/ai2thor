import pandas
from PIL import Image
from ai2thor.controller import Controller

c = Controller(
    local_executable_path = "unity/builds/thor-OSXIntel64-local/thor-OSXIntel64-local.app/Contents/MacOS/AI2-THOR",
    agentMode = "arm",
    scene = "FloorPlan_ExpRoom",
    width = 1600,
    height = 900,
    renderDepthImage = False
    )

# move agent to the opposite side of table to avoid having the door in the background
c.step(
    action = "Teleport",
    position = dict(x=-.4, y=.9009, z=-1),
    rotation = dict(x=0, y=0, z=0)
    )

# center camera
c.step(
    action = "AddThirdPartyCamera",
    position = dict(x=0,y=.8, z=5),
    rotation = dict(x=0, y=0, z=90),
    fieldOfView = 60
    )

# left camera

# right camera




#Image.fromarray(c.last_event.third_party_camera_frames[0]).save("temp.png")
