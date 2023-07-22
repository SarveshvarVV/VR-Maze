import viz
import vizfx
import vizshape
import vizcam
import vizact

import random
import vizproximity
import vizinfo
import time
import vizmat

viz.go()
start_time = time.time()
maze = vizfx.addChild('maze.osgb')

viz.MainView.collision(viz.ON)

birds_eye_window = viz.addWindow()
birds_eye_view = viz.addView()
birds_eye_window.setView(birds_eye_view)

birds_eye_view.setPosition([0,25,0])
birds_eye_view.setEuler([0,90,0])
birds_eye_window.fov(60)
"""
def print_pos():
    print(viz.MainView.getPosition())
vizact.ontimer(0,print_pos)
"""
# VIZUALIZATION OF THE PLAYER NAVIGATION
# OTF Node3d Class
viz.startLayer(viz.LINE_STRIP)
viz.vertexColor(viz.YELLOW)
my_lines = viz.endLayer(parent = viz.ORTHO, scene=birds_eye_window)

my_lines.dynamic()

no_of_collisions = 0
elasped_time = 0
total_distance = 0
final_score = 0
x_coord = []
y_coord = []
z_coord = []
score = 0
game_over=0
at_least_one = 0
def update_path():
    global elasped_time
    global total_distance
    global game_over
    x,y,z = birds_eye_window.worldToScreen(viz.MainView.getPosition(),mode=viz.WINDOW_PIXELS) # get the info about where you are in the MainWindow and transform and render on to the birds_eye_window
    lx, ly, lz = my_lines.getVertex(-1)
    x_coord.append(x)
    y_coord.append(y)
    z_coord.append(z)
    if x!=lx and y!=ly:
        my_lines.addVertex(x,y,0)
    elasped_time = time.time()-start_time
    #print(elasped_time)
    if elasped_time>60 or no_of_collisions>50:
        game_over=1
    #print(elasped_time)
    p1 = [x,y,0]
    p2 = [lx, ly, 0]
    temp_dist = vizmat.Distance(p1, p2)
    total_distance+=temp_dist
    #print(total_distance)
vizact.ontimer(0,update_path)

vizact.onkeydown(' ',my_lines.clearVertices)
audio_collide = viz.addAudio('crash.wav')

def my_collision(col):
    global no_of_collisions
    no_of_collisions+=1
    audio_collide.play()

   
    #print(no_of_collisions)
   
viz.callback(viz.COLLISION_EVENT,my_collision)

# PROXIMITY SENSING
locations = [[9,1.5,-9.5],[-9.3,1.5,-10],[7.5,1.5,5.5],[3,1.5,-9.5],[-9.4,1.5,3],[8.8,1.5,10.5]]
x = 0.01
y = 0.1
z = 1
def score_update():
    global final_score
    global game_over
    if game_over!=1:
        final_score = score - (total_distance*x) - (y*no_of_collisions) - (z*elasped_time)
        score_info = vizinfo.InfoPanel(str(round(final_score,1)),align=viz.ALIGN_CENTER_BOTTOM,icon=False)
   
        #print(final_score)
        score_info.setPanelVisible(viz.OFF)
    else:    
        game_over_info = vizinfo.InfoPanel('GAME OVER! Your Score is '+ str(round(final_score,1)),align=viz.ALIGN_CENTER,icon=False)
        if at_least_one == 1:
            every_obj_info.setPanelVisible(viz.OFF)

   
   
vizact.ontimer(1,score_update)

final_locations = random.sample(locations,3)
#print(final_locations)

torus = vizshape.addTorus(axis = vizshape.AXIS_X)
torus.setPosition(final_locations[0])
torus.color(viz.RED)
torus.addAction(vizact.spin(0,1,0,90))

box = vizshape.addBox()
box.setPosition(final_locations[1])
box_act1 = vizact.moveTo([final_locations[1][0],2,final_locations[1][2]],time=1)
box_act2 = vizact.moveTo([final_locations[1][0],1,final_locations[1][2]],time=1)
box_action = vizact.sequence([box_act1,box_act2], viz.FOREVER)
box.addAction(box_action)
my_texture = viz.addTexture('gb_noise.jpg')
box.texture(my_texture)

pyramid = vizshape.addPyramid()
pyramid.setPosition(final_locations[2])
pyramid_act1 = vizact.sizeTo([1.5,1.5,1.5],time=1)
pyramid_act2 = vizact.sizeTo([0.8,0.8,0.8],time=1)
pyramid_action = vizact.sequence([pyramid_act1,pyramid_act2], viz.FOREVER)
pyramid.addAction(pyramid_action)
pyramid.color(viz.BLUE)


"""
# Preamble for Proximity Sensing Understanding
# PROXIMITY --> MANAGER, TARGET, SENSOR
my_manager = vizproximity.Manager()
my_manager.setDebug(True)
my_target = vizproximity.Target(viz.MainView)
my_manager.addTarget(my_target)
my_sensor = vizproximity.Sensor(vizproximity.Sphere(2),source=box)
my_manager.addSensor(my_sensor)
"""
audio_torus = viz.addAudio('curtain_stop.wav')
audio_box = viz.addAudio('crashQuiet.wav')
audio_pyramid = viz.addAudio('crashNew.wav')

shapes = [torus,box,pyramid]
total_shapes = len(shapes)
shapes_tbd = len(shapes)


def found_object(e):
    global at_least_one
    global score
    at_least_one = 1

    global shapes_tbd
    global game_over
    global every_obj_info
    shape = e.sensor.getSourceObject()

    if shape==torus and shapes_tbd==len(shapes):
        audio_torus.play()
        score += 200
        shape.visible(viz.OFF)
        e.manager.removeSensor(e.sensor)
        shapes_tbd-=1

    if shape==box and shapes_tbd==len(shapes)-1:
        audio_box.play()
        score += 150
        shape.visible(viz.OFF)
        e.manager.removeSensor(e.sensor)
        shapes_tbd-=1
       
    if shape==pyramid and shapes_tbd==len(shapes)-2:
        audio_pyramid.play()
        score += 100
        shape.visible(viz.OFF)
        e.manager.removeSensor(e.sensor)
        shapes_tbd-=1
       
   
    print(shapes_tbd)
    if shapes_tbd==0:
        game_over=1
    elif shapes_tbd == len(shapes):
        every_obj_info = vizinfo.InfoPanel(str(shapes_tbd) + ' more object(s) to collect',align=viz.ALIGN_LEFT_TOP,icon=False)
        every_obj_info.setPanelVisible(viz.OFF)
    else:
        message = 'Object Collected! '+ str(shapes_tbd) + ' more object(s) to collect'
       
        if shapes_tbd<(len(shapes)-1):
            every_obj_info.setPanelVisible(viz.OFF)
        every_obj_info = vizinfo.InfoPanel(message,align=viz.ALIGN_LEFT_TOP,icon=False)



my_manager = vizproximity.Manager()
#my_manager.setDebug(True)
my_target = vizproximity.Target(viz.MainView)
my_manager.addTarget(my_target)

for s in shapes:
    my_sensor = vizproximity.Sensor(vizproximity.Sphere(2),source=s)
    my_manager.addSensor(my_sensor)
    my_manager.onEnter(my_sensor,found_object)