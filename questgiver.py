#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import spade
import time
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade
from spade.behaviour import TimeoutBehaviour, CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour

class Questgiver(Agent):

    name = ""
    person = ""    

    class Setup(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                self.agent.name = msg.body

                print("QuestGiver: My name is " + self.agent.name + ".")
                time.sleep(1)

                agentsBehaviour = self.agent.PlayOut()

                agentsBehaviour.add_state(name="StateEnjoyingLife", state=self.agent.StateEnjoyingLife(), initial=True)
                agentsBehaviour.add_state(name="StateLookingForHelp", state=self.agent.StateLookingForHelp())
                agentsBehaviour.add_state(name="StateWaitingForHeroToWin", state=self.agent.StateWaitingForHeroToWin())
                agentsBehaviour.add_state(name="StateEverythingOver", state=self.agent.StateEverythingOver())

                agentsBehaviour.add_transition(source="StateEnjoyingLife", dest="StateEnjoyingLife")
                agentsBehaviour.add_transition(source="StateEnjoyingLife", dest="StateLookingForHelp")
                agentsBehaviour.add_transition(source="StateLookingForHelp", dest="StateLookingForHelp")
                agentsBehaviour.add_transition(source="StateLookingForHelp", dest="StateWaitingForHeroToWin")
                agentsBehaviour.add_transition(source="StateWaitingForHeroToWin", dest="StateWaitingForHeroToWin")
                agentsBehaviour.add_transition(source="StateWaitingForHeroToWin", dest="StateEverythingOver")
                agentsBehaviour.add_transition(source="StateEverythingOver", dest="StateEverythingOver")

                self.agent.add_behaviour(agentsBehaviour)
                self.kill()
            else:
                print("QuestGiver: No info received.")
                time.sleep(1)

    class PlayOut(FSMBehaviour):
        async def on_start(self):
            print("QuestGiver: King " + self.agent.name + " is ready!")
            time.sleep(1)
        async def on_end(self):
            print("QuestGiver: King " + self.agent.name + "\'s journey ends.")
            time.sleep(1)
        
    class StateEnjoyingLife(State):
        async def run(self):
            msg = await self.receive(timeout = 10)
            if msg:
                if msg.body == "takePrince":
                    print("QuestGiver: Oh no, my son! He was kidnapped.")
                    time.sleep(1)
                    print("QuestGiver: I need a brave hero to go and save him.")
                    time.sleep(1)
                    self.set_next_state("StateLookingForHelp")
            else:
                self.set_next_state("StateEnjoyingLife")
       
    class StateLookingForHelp(State):
        async def run(self):
            msg = spade.message.Message(
                to="hero@localhost",
                body="pleaseHelp"
                )
            await self.send(msg)
            print("QuestGiver: Won\'t you help me, brave dame?")
            msg = await self.receive(timeout = 10)
            if msg:
                if msg.body == "okay":
                    print("QuestGiver: Thank you, brave hero!")
                    time.sleep(1)
            self.set_next_state("StateWaitingForHeroToWin")
            

    class StateWaitingForHeroToWin(State):
        async def run(self):
            msg = await self.receive(timeout = 10)
            if msg:
                if msg.body == "princeReturned":
                    print("QuestGiver: You\'ve returned my son to me! Thank you so much!")
                    time.sleep(1)
                    self.set_next_state("StateEverythingOver")
                elif msg.body == "nooneAround":
                    print("QuestGiver: I fear my son is gone for good, truly a sad day for the kingdom.")
                    time.sleep(1)
            else:
                self.set_next_state("StateWaitingForHeroToWin")

    class StateEverythingOver(State):
        async def run(self):
            print("QuestGiver: It\'s over")

    async def setup(self):
        print("QuestGiver: Starting!")
        behaviourSetup = self.Setup()
        self.add_behaviour(behaviourSetup)

