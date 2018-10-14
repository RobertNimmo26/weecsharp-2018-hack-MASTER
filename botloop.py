#Main loop for bot after server init etc.
from mapFunctions import *
import logging
import random
import time

def mainLoop(GameServer,ServerMessageTypes):

	i=0
	names = []
	xpos = 0
	ypos = 0
	enemyxpos = 0
	enemyypos = 0
	enemies = []
	killCounter=0
	SnitchCounter=0

	tanks=[]
	x=[0, 0, 0, 0, 0]
	y=[0, 0, 0, 0, 0]
	heading=[0, 0, 0, 0, 0]
	distance=[0, 0, 0, 0, 0]
	turretBearing = 0
	noObject = True

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
						noObject = False
						movement = move_to_position(ServerMessageTypes,GameServer,xpos,ypos,healthxpos,healthypos,movementType="health")

					elif message['Ammo']<3:
						noObject = False
						movement = move_to_position(ServerMessageTypes,GameServer,xpos,ypos,ammoxpos,ammoypos,movementType="ammo")

					else:
						noObject = True

				except: 
					print("Not seen any health or ammo yet!")


			else:
				if (message["Type"] == 'Tank'):								#enemy tank
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
					noObject = False
					lowestpos=distance.index(lowest)              
					logging.info(lowest)
					logging.info(heading[lowestpos])
					GameServer.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING, {"Amount" : heading[lowestpos]})
					GameServer.sendMessage(ServerMessageTypes.FIRE)

				
					if (message["Type"] == 'SnitchPickup' and xpos==message['X'] and ypos==message['Y']):
						SnitchCounter+=1

					if SnitchCounter > 0:
						SnitchCounter=0
						if ypos> 0:
							body_heading = GetHeading(xpos, ypos, 0,102 )	
							distance_to_coord = GetDistance(xpos, ypos, 0, 102)
	
							GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": body_heading})
							GameServer.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE , {"Amount": distance_to_coord})

						else:
							body_heading = GetHeading(xpos, ypos, 0, -102 )	
							distance_to_coord = GetDistance(xpos, ypos, 0, -102)
	
							GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": body_heading})
							GameServer.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE , {"Amount": distance_to_coord})

					if (message["Name"] != 'Donkey') and (message['Health'] !=0):

						GameServer.sendMessage(ServerMessageTypes.FIRE)
						if (message["Name"] != 'Donkey') and (message['Health'] ==0):
							killCounter +=1

						if killCounter > 0:
							killCounter=0
							if ypos> 0:
								body_heading = GetHeading(xpos, ypos, 0,102 )	
								distance_to_coord = GetDistance(xpos, ypos, 0, 102)
		
								GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": body_heading})
								GameServer.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE , {"Amount": distance_to_coord})

							else:
								body_heading = GetHeading(xpos, ypos, 0, -102 )	
								distance_to_coord = GetDistance(xpos, ypos, 0, -102)
		
								GameServer.sendMessage(ServerMessageTypes.TURNTOHEADING, {"Amount": body_heading})
								GameServer.sendMessage(ServerMessageTypes.MOVEFORWARDDISTANCE , {"Amount": distance_to_coord})
					#HITDETECTED: "HITDETECTED",
					#KILL: "KILL",
					
					#time.sleep(0.25)														<-- Find a more elegant solution?


				#other items in the game

				if (message["Type"] == 'HealthPickup'):			#Health pickup
					healthxpos= message['X']
					healthypos=message['Y']

				if (message["Type"] == 'AmmoPickup'):			#Ammo pickup
					ammoxpos= message['X']
					ammoypos=message['Y']

				if (message["Type"] == 'SnitchPickup'):			#Snitch pickup
					snitchxpos= message['X']
					snitchypos=message['Y']
					movement = move_to_position(ServerMessageTypes,GameServer,xpos,ypos,snitchxpos,snitchypos,movementType="snitch")
																#If there's nothing else tae do
			if noObject:
				randx = random.uniform(-10,10)
				randy = random.uniform(-10,10)
				# turretBearing += 10
				# GameServer.sendMessage(ServerMessageTypes.TURNTURRETTOHEADING,{"Amount" : turretBearing})
				# time.sleep(0.05)
				movement = move_to_position(ServerMessageTypes,GameServer,xpos,ypos,randx,randy,movementType="idleMovement")

