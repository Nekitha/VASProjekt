#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import spade
import random
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade
from spade.behaviour import TimeoutBehaviour, CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour

class Narrator(Agent):
    characters = {}
    storyOver = False

    def getInput(self):
        try:
            return int(input())
        except ValueError:
            return -1

    def makeAnObjective(self):
        name = ""
        print("Narrator: This is a story about the kidnapping of a young prince.")
        while name == "":
            name = input("Narrator: What is the name of the prince being saved? ")
        self.characters["objectiveName"] = name

    def makeAQuestGiver(self):
        name = ""
        print("Narrator: The prince\'s father will be very distraught.")
        while name == "":
            name = input("Narrator: What is the king\'s name? ")
        self.characters["giverName"] = name

    def makeAHero(self):
        name = ""
        print("Narrator: A noble dame will need to prove herself.")
        while name == "":
            name = input("Narrator: What is the brave dame\'s name? ")
        self.characters["heroName"] = name
    
    def makeAnEnemy(self):
        print("Narrator: And defeat an evil dragon.")
        name = ""
        while name == "":
            name = input("Narrator: The overgrown lizard\'s name will be: ")
        self.characters["enemyName"] = name

    class SetupStory(OneShotBehaviour):
        async def run(self):
            print("Narrator: Greetings! Before the story can begin, you need to decide on a few things.")
            self.agent.makeAnObjective()            
            self.agent.makeAQuestGiver()
            self.agent.makeAHero()
            self.agent.makeAnEnemy()
            self.agent.add_behaviour(self.agent.SendInfoToCharacters())

    class WaitForAgents(OneShotBehaviour):
        async def run(self):
            everyone = []

            while len(everyone) < 3:
                msg = await self.receive()
                if msg:
                    if msg.body not in everyone:
                        everyone.append(msg.sender)

            self.agent.add_behaviour(self.agent.SendInfoToCharacters())

    class SendInfoToCharacters(OneShotBehaviour):
        async def run(self):
            print("Narrator: Sending info to characters.")
            msg = spade.message.Message(
                to="hero@localhost",
                body=self.agent.characters["heroName"]
                )
            await self.send(msg)            
            msg = spade.message.Message(
                to="questgiver@localhost",
                body=self.agent.characters["giverName"]
                )
            await self.send(msg)
            msg = spade.message.Message(
                to="enemy@localhost",
                body=self.agent.characters["enemyName"]
                )
            await self.send(msg)
            self.agent.add_behaviour(self.agent.WaitForInfo())

    class WaitForInfo(CyclicBehaviour):
        async def run(self):          
            msg = await self.receive()
            if msg:
                if msg.body == "takingPrince":
                    print("Narrator: The young prince was picked up by the evil dragon and taken to the beast\'s lair.")
                    time.sleep(1)
                elif msg.body == "questStart":
                    print("Narrator: The dame heads out, searching for the dragon\'s cave. In order to reach it, she\'ll need to delve into the enchanted forest.")
                    time.sleep(1)  
                elif msg.body == "questLostDeath":
                    print("Narrator: Unfortunately, the hero got lost in the cursed forest, eventually dying due to exhaustion.")
                    time.sleep(1)
                    msg = spade.message.Message(
                        to="enemy@localhost",
                        body="heroDied"
                        )
                    await self.send(msg)
                elif msg.body == "victoryEnemy":
                    print("Narrator: The evil dragon " + self.agent.characters["enemyName"] + " managed to get away with snatching the future of the kingdom.")
                    time.sleep(1)
                    msg = spade.message.Message(
                        to="questgiver@localhost",
                        body="nooneAround"
                        )
                    await self.send(msg)
                    self.agent.storyOver = True
                elif msg.body == "victoryHero":
                    print("Narrator: The brave dame " + self.agent.characters["heroName"] + " managed to save the future of the kingdom.")
                    time.sleep(1)
                    msg = spade.message.Message(
                        to="questgiver@localhost",
                        body="princeReturned"
                        )
                    await self.send(msg)
                    self.agent.storyOver = True
                elif msg.body == "caveFound":
                    print("Narrator: " + self.agent.characters["heroName"] + " reached " + self.agent.characters["enemyName"] + "\'s cave after stumbling throughout the forest.")
                    time.sleep(1)
                elif msg.body == "combat":
                    print("Narrator: The two rivals were locked in combat for hours.")
                    time.sleep(1)
                    dragonWins = 0
                    heroWins = 0
                    while heroWins < 3 and dragonWins < 3:
                        possibilities = [1, 2]
                        choice = random.choice(possibilities)
                        if choice == 1:
                            heroWins = heroWins + 1
                            if heroWins == 1:
                                print("Narrator: The hero landed a hit on the dragon.")
                            elif heroWins == 2:
                                print("Narrator: After dodging a tailswipe, " + self.agent.characters["heroName"] + " landed a slash on the dragon\'s snout.")
                            elif heroWins == 3:
                                print("Narrator: With one final blow, the dame managed to slay the beast with a stab to the heart.")
                        elif choice == 2:
                            dragonWins = dragonWins + 1
                            if dragonWins == 1:
                                print("Narrator: The dragon slashed at the hero, ruining their suit of armour.")
                            elif dragonWins == 2:
                                print("Narrator: " + self.agent.characters["enemyName"] + " managed to slam the hero with his tail, knocking them off balance.")
                            elif dragonWins == 3:
                                print("Narrator: Tired of toying with his prey, the dragon burnt the hero to a crisp.")
                        time.sleep(1)
                        if heroWins >= 3:
                            msg = spade.message.Message(
                                to="enemy@localhost",
                                body="loss"
                                )
                            await self.send(msg)
                            msg = spade.message.Message(
                                to="hero@localhost",
                                body="victory"
                                )
                            await self.send(msg)
                        if dragonWins >= 3:
                            msg = spade.message.Message(
                                to="enemy@localhost",
                                body="victory"
                                )
                            await self.send(msg)
                            msg = spade.message.Message(
                                to="hero@localhost",
                                body="loss"
                                )
                            await self.send(msg)
    async def setup(self):
        print("Narrator: Starting!")
        behaviourSetupStory = self.SetupStory()
        self.add_behaviour(behaviourSetupStory)

