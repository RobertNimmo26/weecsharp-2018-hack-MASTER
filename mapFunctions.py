#key functions

import logging
import math

travelPriorities = {
	"snitch" : 1,
	"snitchGoal" : 2,
	"health" : 3,
	"ammo" : 4,
	"chaseEnemy" : 5,
	"idleMovement" : 6
}

currentPriority = 7		#init travel priority below every other kind of movement


def GetHeading(x1,y1,x2,y2):
	heading = math.degrees(math.atan2(y2-y1,x2-x1))
	heading = math.fmod(heading-360,360)
	print(heading)
	return int(math.fabs(heading))
	
def GetDistance(x1,y1,x2,y2):
	displacement_x=x2-x1
	displacement_y=y2-y1
	return int(math.sqrt(displacement_x**2 + displacement_y**2))

def move_to_position(ServerMessageTypes,GameServer,xpos,ypos,desiredxpos,desiredypos,body_heading=0,distance_to_coord=0,movementType="idleMovement"):

	tryPriority = travelPriorities[movementType]
	if tryPriority > currentPriority:
		currentPriority = tryPriority
		body_heading = GetHeading(xpos, ypos, desiredxpos,desiredypos )	
		distance_to_coord = GetDistance(xpos, ypos, desiredxpos, desiredypos)
		
		
		logging.info('Going to origin')
		GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": body_heading})
		GameServer.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE , {"Amount": distance_to_coord})

	
	print(travelPriorities[movementType])
