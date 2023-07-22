import viz
import vizcam
import vizfx
import vizshape
import vizact
import vizconnect
viz.go()

viz.phys.enable()
vizconnect.go('project_config.py')
scene = vizfx.addChild('dojo.osgb')
scene.collidePlane()

box = vizfx.addChild('crate.osgb')
box.setPosition([0,0.5,3])
box.setScale([1,1,7])
box.collideMesh()

balls = []
for i in range(6):
	ball = viz.addChild('volleyball.osgb', cache=viz.CACHE_CLONE)
	ball.collideSphere(bounce=1, friction=1, hardness=1, density=1)
	ball.setPosition([0,3,i])
	ball.setScale([0.5,0.5,0.5])
	ball.alpha(1)
	balls.append(ball)

grabber = vizconnect.getRawTool('grabber')
grabber.setItems(balls)

from tools import grabber

def on_grab(e):
	e.grabbed.alpha(0.8)
	
def on_release(e):
	e.released.alpha(1)
	
viz.callback(grabber.GRAB_EVENT, on_grab)
viz.callback(grabber.RELEASE_EVENT, on_release)