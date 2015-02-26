#!python2.6

import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

class MySMClass(sm.SM):
    startState = 'start'

    def getNextValues(self, state, inp):
        if state == 'start':
            if inp.sonars[3] >=.5:
                return ('moveForward', io.Action(fvel = 0.3, rvel = 0.0))
            else:
                return('turn', io.Action(fvel = 0.0, rvel = 0.0))
        elif state == 'moveForward':
            if inp.sonars[3] >=.5:
                return ('moveForward', io.Action(fvel = 0.3, rvel = 0.0))
            else:
                return ('turn', io.Action(fvel = 0.0, rvel = 0.0))
        elif state == 'turn':
            if inp.sonars[3] <= 0.5 or inp.sonars[7] <= 0.5:
                return('turn', io.Action(fvel=0.0, rvel = 0.5))
            else:
                return ('moveForward', io.Action(fvel = 0.3, rvel = 0.0))
        else:
            return('stop', io.Action(fvel = 0.0, rvel = 0.0))

mySM = MySMClass()
mySM.name = 'brainSM'

######################################################################
###
###          Brain methods
###
######################################################################

def plotSonar(sonarNum):
    robot.gfx.addDynamicPlotFunction(y=('sonar'+str(sonarNum),
                                        lambda: 
                                        io.SensorInput().sonars[sonarNum]))

# this function is called when the brain is (re)loaded
def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True, # slime trails
                                  sonarMonitor=True) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    print inp.sonars[3]
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
