#Main loop for bot after server init etc.
import mapFunctions

def mainLoop():
	while True:
		message = GameServer.readMessage()
		logging.info(message)

		if type(message) == dict and "Name" in message:
			print(message)

			if (message["Name"] == 'RandomBot'):								#our bot tank
				xpos = message["X"]
				ypos = message["Y"]

				if message['Health']<3:
					move_to_position(xpos,ypos,healthxpos,healthypos)

				elif message['Ammo']<3:
					move_to_position(xpos,ypos,ammoxpos,ammoypos)

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
					move_to_position(xpos,ypos,enemyxpos,enemyypos)

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
					GameServer.sendMessage(ServerMessageTypes.FIRE)
					#time.sleep(0.25)														<-- Find a more elegant solution?


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
					move_to_position(xpos,ypos,snitchxpos,snitchypos)

			else:
				move_to_position(xpos,ypos,0,0)