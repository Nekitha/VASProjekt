#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import spade
import random
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade
from spade.behaviour import TimeoutBehaviour, CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour

class Hero(Agent):
    
    name = ""
    person = ""

    class Setup(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                self.agent.name = msg.body

                print("Hero: My name is " + self.agent.name + ".")
                time.sleep(1)

                agentsBehaviour = self.agent.PlayOut()
                agentsBehaviour.add_state(name="StateQuestless", state=self.agent.StateQuestless(), initial=True)
                agentsBehaviour.add_state(name="StateOnQuest", state=self.agent.StateOnQuest())
                agentsBehaviour.add_state(name="StateCombat", state=self.agent.StateCombat())
                agentsBehaviour.add_state(name="StateFinishedQuest", state=self.agent.StateFinishedQuest())
                agentsBehaviour.add_state(name="StateDead", state=self.agent.StateDead())

                agentsBehaviour.add_transition(source="StateQuestless", dest="StateQuestless")
                agentsBehaviour.add_transition(source="StateQuestless", dest="StateOnQuest")
                agentsBehaviour.add_transition(source="StateOnQuest", dest="StateOnQuest")
                agentsBehaviour.add_transition(source="StateOnQuest", dest="StateFinishedQuest")
                agentsBehaviour.add_transition(source="StateFinishedQuest", dest="StateFinishedQuest")
                agentsBehaviour.add_transition(source="StateOnQuest", dest="StateCombat")
                agentsBehaviour.add_transition(source="StateCombat", dest="StateCombat")
                agentsBehaviour.add_transition(source="StateCombat", dest="StateFinishedQuest")
                agentsBehaviour.add_transition(source="StateCombat", dest="StateDead")
                agentsBehaviour.add_transition(source="StateOnQuest", dest="StateDead")
                agentsBehaviour.add_transition(source="StateDead", dest="StateDead")

                self.agent.add_behaviour(agentsBehaviour)
                self.kill()
            else:
                print("Hero: No info received.")
                time.sleep(1)

    class PlayOut(FSMBehaviour):
        async def on_start(self):
            print("Hero: Dame " + self.agent.name + " is ready!")
            time.sleep(1)
        async def on_end(self):
            print("Hero: Dame " + self.agent.name + "\'s journey ends.")
            time.sleep(1)
        
    class StateQuestless(State):
        async def run(self):
            msg = await self.receive(timeout = 10)
            if msg:
                if msg.body == "pleaseHelp":
                    msg = msg.make_reply()
                    msg.body = "okay"
                    await self.send(msg)
                    print("Hero: Fine, I will rescue the prince from the dragon\'s clutches.")
                    time.sleep(2)
                    msg = spade.message.Message(
                        to="narrator@localhost",
                        body="questStart"
                        )
                    await self.send(msg)
                    time.sleep(1)                  

                    self.set_next_state("StateOnQuest")
            else:
                self.set_next_state("StateQuestless")          
        
    class StateOnQuest(State):
        days = 0
        async def run(self):
            self.days = self.days + 1
            possibilities = [1, 2, 3, 4]
            choice = random.choice(possibilities)
            print("Hero: The Sun is up, I better make haste. It\'s been " + str(self.days) + " days since I started.")
            time.sleep(2)
            if choice == 1:
                msg = spade.message.Message(
                        to="narrator@localhost",
                        body="caveFound"
                        )
                await self.send(msg)
                time.sleep(1)
                print("Hero: This must be the cave")
                time.sleep(1)
                self.set_next_state("StateCombat")
            else:
                if self.days >= 3:
                    print("Hero: It\'s been three days, I fear I\'ve gotten lost")
                    msg = spade.message.Message(
                        to="narrator@localhost",
                        body="questLostDeath"
                        )
                    await self.send(msg)
                    time.sleep(1)
                    self.set_next_state("StateDead")
                else:
                    self.set_next_state("StateOnQuest")

    class StateCombat(State):
        sent = False
        async def run(self):
            if self.sent != True:
                print("Hero: Face me!")
                time.sleep(1)
                self.sent = True
                msg = spade.message.Message(
                    to="narrator@localhost",
                    body="combat"
                    )
                await self.send(msg)
                time.sleep(1)
            msg = await self.receive(timeout=30)
            if msg:
                if msg.body == "loss":
                    print("Hero: I failed.")
                    time.sleep(1)
                    self.set_next_state("StateDead")
                elif msg.body == "victory":
                    print("Hero: Don\'t worry, prince, you\'re safe now. Come with me.")
                    time.sleep(1)
                    self.set_next_state("StateFinishedQuest")
            else:
                self.set_next_state("StateCombat")

    class StateFinishedQuest(State):
        async def run(self):
            print("Hero: It\'s over.")
            time.sleep(1)
            msg = spade.message.Message(
                to="narrator@localhost",
                body="victoryHero"
                )
            await self.send(msg)

    class StateDead(State):
        async def run(self):
            print("Hero: *The hero\'s remains were never found.*")

    async def setup(self):
        print("Hero: Starting!")
        behaviourSetup = self.Setup()
        self.add_behaviour(behaviourSetup)

