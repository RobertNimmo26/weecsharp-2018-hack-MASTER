#!/usr/bin/python

#Master python script for weecsharp MSBot

import logging
import random
import math
import time

import botloop
import serverSetup

args = serverSetup.parseArgs()

ServerMessageTypes = serverSetup.ServerMessageTypes()

# Connect to game server
GameServer = serverSetup.ServerComms(args.hostname, args.port)

# Spawn our tank
logging.info("Creating tank with name '{}'".format(args.name))
GameServer.sendMessage(ServerMessageTypes.CREATETANK, {'Name': args.name})

# Main loop - read game messages, ignore them and randomly perform actions
botloop.mainLoop(GameServer,ServerMessageTypes)

