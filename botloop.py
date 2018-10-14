#Main loop for bot after server init etc.
from mapFunctions import *
import logging
import time

def mainLoop(GameServer,ServerMessageTypes):

	i=0
	names = []
	xpos = 0
	ypos = 0
	enemyxpos = 0
	enemyypos = 0
	enemies = []

	tanks=[]
	x=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	y=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	heading=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	distance=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	while True:
		message = GameServer.readMessage()
		logging.info(message)

		if type(message) == dict and "Name" in message:
			#print(message)

			if (message["Name"] == 'DONKEY'):								#our bot tank
				xpos = message["X"]
				ypos = message["Y"]

				try:
					if message['Health']<3:
						movement = move_to_position(ServerMessageTypes,GameServer,xpos,ypos,healthxpos,healthypos,movementType="health")

					elif message['Ammo']<3:
						movement = move_to_position(ServerMessageTypes,GameServer,xpos,ypos,ammoxpos,ammoypos,movementType="ammo")
				except: print("Not seen any health or ammo yet!")

			else:
				if (message["Type"] == 'Tank'):									#enemy tank
					enemyname = message["Name"]
					enemyxpos = message["X"]
					enemyypos = message['Y']
					if enemyname in enemies:
						enemies[1] = enemyname
					badguy = [enemyname,enemyxpos,enemyypos]
					#print(enemies)
					enemies.append(badguy)
					movement = move_to_position(ServerMessageTypes,GameServer,xpos,ypos,enemyxpos,enemyypos,movementType="chaseEnemy")

					if message["Name"] not in tanks:
						tanks.append(message["Name"])
					else:
						pos=tanks.index(message["Name"])                       

						x[pos]=message["X"]
						y[pos]=message["Y"]

						if message["Name"] != "DONKEY":                                
							heading[pos]=GetHeading(x[0], y[0], x[pos], y[pos])
							distance[pos]=GetDistance(x[0], y[0], x[pos], y[pos])

					if len(distance) > 0:
						lowest = distance[1]           
						for i in distance:
							if i != 0 and lowest-i > 0: 
								lowest = i

					lowestpos=distance.index(lowest)              
					logging.info(lowest)
					logging.info(heading[lowestpos])
					
					GameServer.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING, {"Amount" : heading[lowestpos]})
					time.sleep(0.05)
					GameServer.sendMessage(ServerMessageTypes.FIRE)
																			#<-- Find a more elegant solution?


				


				#other items in the game

				if (message["Type"] == 'HealthPickup'):
					healthxpos= message['X']
					healthypos=message['Y']

				if (message["Type"] == 'AmmoPickup'):
					ammoxpos= message['X']
					ammoypos=message['Y']

				if (message["Type"] == 'SnitchPickup'):
					snitchxpos= message['X']
					snitchypos=message['Y']
					movement = move_to_position(ServerMessageTypes,GameServer,xpos,ypos,snitchxpos,snitchypos,movementType="snitch",movement=movement)

				else:
					movement = move_to_position(ServerMessageTypes,GameServer,xpos,ypos,0,0,movementType="idleMovement")
