# gravity
# boundaries
# inertia - friction, mass, density, forces and torques

 #Simulink ODE Solver
 
# Colliders
# Joints

import viz
import vizcam
import vizshape
import vizact
viz.go()

viz.phys.enable()

ground = viz.addChild('ground.osgb')
ground.collidePlane()

board = viz.addChild('box.wrl')
board.setScale([8.,0.1,2.])
board.collideBox()

cylinder = viz.addChild('cylinder.wrl')
cylinder.setScale([5,5,5])
cylinder.setEuler([0,90,0])
cylinder.setPosition([0,0.25,3.75])
cylinder.collideMesh()
cylinder.disable(viz.DYNAMICS)

load1 = viz.addChild('volleyball.osgb')
load1.setScale([3,3,3])
load1.collideSphere()

load2 = viz.addChild('volleyball.osgb')
load2.setScale([3,3,3])
load2.collideSphere(density=50)

viz.MainView.setPosition([0,1.8,-10])

def reset():
	board.setPosition([0,3,5])
	load1.setPosition([3,5,5])
	load2.setPosition([-3.1,7,5])
	
reset()
vizact.onkeydown(' ',reset)