#key functions

import logging
import math

travelPriorities = {
	"snitch" : 6,
	"snitchGoal" : 5,
	"health" : 4,
	"ammo" : 3,
	"chaseEnemy" : 2,
	"idleMovement" : 1
}

currentPriority = 7		#init travel priority below every other kind of movement


def GetHeading(x1,y1,x2,y2):
	heading = math.degrees(math.atan2(y2-y1,x2-x1))
	heading = math.fmod(heading-360,360)
	print(heading)
	return math.fabs(heading)
	
def GetDistance(x1,y1,x2,y2):
	displacement_x=x2-x1
	displacement_y=y2-y1
	return int(math.sqrt(displacement_x**2 + displacement_y**2))

def serpentine(xpos,ypos,desiredxpos,desiredypos):
	pass

def move_to_position(ServerMessageTypes,GameServer,xpos,ypos,desiredxpos,desiredypos,body_heading=0,distance_to_coord=0,movementType="idleMovement",currentMovement="idleMovement"):
	currentPriority = travelPriorities[currentMovement]
	tryPriority = travelPriorities[movementType]

	print(movementType,tryPriority)

	if tryPriority >= currentPriority:
		print("Moving for {}".format(movementType))
		currentPriority = tryPriority
		body_heading = GetHeading(xpos, ypos, desiredxpos,desiredypos )	
		distance_to_coord = GetDistance(xpos, ypos, desiredxpos, desiredypos)

		GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": body_heading})
		GameServer.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE , {"Amount": distance_to_coord})
		print("distance to objective:{}".format(distance_to_coord))
		error = 10						#Change this to adjust how persistent it is to reach an objective
		if distance_to_coord <= error:	#reset tasking
			currentPriority = 7

	
