#!/usr/bin/python

#Master python script for weecsharp MSBot

import json
import socket
import logging
import binascii
import struct
import argparse
import random
import math
import time

import botloop
import serverSetup

i=0
names = []
xpos = 0
ypos = 0
enemyxpos = 0
enemyypos = 0
healthxpos=0
healthypos=0
ammoxpos=0
ammoypos=0
enemies = []

tanks=[]
x=[0, 0, 0, 0, 0]
y=[0, 0, 0, 0, 0]
heading=[0, 0, 0, 0, 0]
distance=[0, 0, 0, 0, 0]

# Connect to game server
GameServer = ServerComms(args.hostname, args.port)

# Spawn our tank
logging.info("Creating tank with name '{}'".format(args.name))
GameServer.sendMessage(ServerMessageTypes.CREATETANK, {'Name': args.name})

# Main loop - read game messages, ignore them and randomly perform actions
botloop.mainLoop()

