#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import spade
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade
from spade.behaviour import TimeoutBehaviour, CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour

class Narrator(Agent):
    characters = {}

    def getInput(self):
        try:
            return int(input())
        except ValueError:
            return -1

    def makeAnObjective(self):
        print("Narrator: What will the objective be?")
        print("1. Save someone")
        print("2. Find a lost trinket")
        choice = -1
        while choice < 1 or choice > 3:
            choice = self.getInput()
            if choice < 1 or choice > 3:
                print("Please give me a valid number")
        if choice == 1:
            self.characters["objective"] = "save"
        elif choice == 2:
            self.characters["objective"] = "trinket"
        name = ""
        while name == "":
            if self.characters["objective"] == "save":
                name = input("The name of the person you\'re saving is: ")
            elif self.characters["objective"] == "trinket":
                name = input("The name of the object you\'re retrieving is: ")
        self.characters["objectiveName"] = name

    def makeAQuestGiver(self):
        print("Narrator: Who will reward the hero once the quest is over?")
        print("1. A noble king")
        print("2. A peasant tavern owner")
        choice = -1
        while choice < 1 or choice > 3:
            choice = self.getInput()
            if choice < 1 or choice > 3:
                print("Please give me a valid number")
        if choice == 1:
            self.characters["giver"] = "king"
        elif choice == 2:
            self.characters["giver"] = "tavern"
        name = ""
        while name == "":
            name = input("Their name will be: ")
        self.characters["giverName"] = name

    def makeAHero(self):
        print("Narrator: Who will the good guy be?")
        print("1. A humble huntress")
        print("2. A spoiled prince")
        choice = -1
        while choice < 1 or choice > 3:
            choice = self.getInput()
            if choice < 1 or choice > 3:
                print("Please give me a valid number")
        if choice == 1:
            self.characters["hero"] = "huntress"
        elif choice == 2:
            self.characters["hero"] = "prince"
        name = ""
        while name == "":
            name = input("Their name will be: ")
        self.characters["heroName"] = name

    def makeTheWorld(self):
        print("Narrator: What\'s the world like?")
        print("1. Heroes always win")
        print("2. Evil prevails")
        print("3. Let fate decide")
        choice = -1
        while choice < 1 or choice > 4:
            choice = self.getInput()
            if choice < 1 or choice > 4:
                print("Please give me a valid number")
        if choice == 1:
            self.characters["fight"] = "good"
        elif choice == 2:
            self.characters["fight"] = "bad"
        elif choice == 3:
            self.characters["fight"] = "luck"
    
    def makeAnEnemy(self):
        print("Narrator: Who will the main enemy be?")
        print("1. An evil dragon")
        print("2. An evil wizard")
        choice = -1
        while choice < 1 or choice > 3:
            choice = self.getInput()
            if choice < 1 or choice > 3:
                print("Please give me a valid number")
        if choice == 1:
            self.characters["enemy"] = "dragon"
        elif choice == 2:
            self.characters["enemy"] = "wizard"
        name = ""
        while name == "":
            name = input("Their name will be: ")
        self.characters["enemyName"] = name

    class SetupStory(OneShotBehaviour):
        async def run(self):
            print("Narrator: Greetings! Before the story can begin, you need to decide on a few things.")
            self.agent.makeAnObjective()
            self.agent.makeAnEnemy()
            self.agent.makeAQuestGiver()
            self.agent.makeAHero()
            self.agent.makeTheWorld()
            self.agent.add_behaviour(self.agent.SendInfoToCharacters())

    class SendInfoToCharacters(OneShotBehaviour):
        async def run(self):
            print("Narrator: Sending info to characters.")
            msg = spade.message.Message(
                to="hero@localhost",
                body=self.agent.characters["heroName"] + ";" + self.agent.characters["hero"]
                )
            await self.send(msg)
            msg = spade.message.Message(
                to="enemy@localhost",
                body=self.agent.characters["enemyName"] + ";" + self.agent.characters["enemy"]
                )
            await self.send(msg)
            msg = spade.message.Message(
                to="questgiver@localhost",
                body=self.agent.characters["giverName"] + ";" + self.agent.characters["giver"]
                )
            await self.send(msg)
            msg = spade.message.Message(
                to="fate@localhost",
                body=self.agent.characters["fight"]
                )
            await self.send(msg)

    async def setup(self):
        print("Narrator: Starting!")
        behaviourSetupStory = self.SetupStory()
        self.add_behaviour(behaviourSetupStory)

