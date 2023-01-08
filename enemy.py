#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import spade
import time
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade
from spade.behaviour import TimeoutBehaviour, CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour

class Enemy(Agent):
    
    name = ""
    person = ""

    class Setup(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                self.agent.name = msg.body

                print("Enemy: My name is " + self.agent.name + ".")   
                time.sleep(1)
                
                agentsBehaviour = self.agent.PlayOut()
                agentsBehaviour.add_state(name="StateLookingForEvilOpportunity", state=self.agent.StateLookingForEvilOpportunity(), initial=True)
                agentsBehaviour.add_state(name="StateWaitingHero", state=self.agent.StateWaitingHero())
                agentsBehaviour.add_state(name="StateCombat", state=self.agent.StateCombat())
                agentsBehaviour.add_state(name="StateEscapedWithIt", state=self.agent.StateEscapedWithIt())
                agentsBehaviour.add_state(name="StateDead", state=self.agent.StateDead())

                agentsBehaviour.add_transition(source="StateLookingForEvilOpportunity", dest="StateLookingForEvilOpportunity")
                agentsBehaviour.add_transition(source="StateLookingForEvilOpportunity", dest="StateWaitingHero")
                agentsBehaviour.add_transition(source="StateWaitingHero", dest="StateWaitingHero")
                agentsBehaviour.add_transition(source="StateWaitingHero", dest="StateEscapedWithIt")
                agentsBehaviour.add_transition(source="StateEscapedWithIt", dest="StateEscapedWithIt")
                agentsBehaviour.add_transition(source="StateWaitingHero", dest="StateDead")
                agentsBehaviour.add_transition(source="StateWaitingHero", dest="StateCombat")
                agentsBehaviour.add_transition(source="StateCombat", dest="StateCombat")
                agentsBehaviour.add_transition(source="StateCombat", dest="StateDead")
                agentsBehaviour.add_transition(source="StateCombat", dest="StateEscapedWithIt")
                agentsBehaviour.add_transition(source="StateDead", dest="StateDead")

                self.agent.add_behaviour(agentsBehaviour)
                self.kill()
            else:
                print("Enemy: No info received.")
                time.sleep(1)

    class PlayOut(FSMBehaviour):
        async def on_start(self):
            print("Enemy: Dragon " + self.agent.name + " is ready!")
            time.sleep(1)
        async def on_end(self):
            print("Enemy: Dragon " + self.agent.name + "\'s journey ends.")
            time.sleep(1)
        
    class StateLookingForEvilOpportunity(State):
        async def run(self):
            msg = spade.message.Message(
                to="questgiver@localhost",
                body="takePrince"
                )
            print("Enemy: Cough up the prince!")
            time.sleep(1)
            await self.send(msg)
            msg = spade.message.Message(
                to="narrator@localhost",
                body="takingPrince"
                )
            await self.send(msg)
            self.set_next_state("StateWaitingHero")

    class StateWaitingHero(State):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                if msg.body == "heroDied":
                    print("Enemy: It\'s been a while, prince, seems like no one\'s coming to save you.")
                    time.sleep(1)
                    self.set_next_state("StateEscapedWithIt")
                elif msg.body == "heroCame":
                    print("Enemy: Welcome to my cave, miss, you\'ll never escape alive.")
                    time.sleep(1)
                    self.set_next_state("StateCombat")
            else:
                self.set_next_state("StateWaitingHero")

    class StateCombat(State):
        async def run(self):
            msg = await self.receive(timeout=30)
            if msg:
                if msg.body == "loss":
                    print("Enemy: Damn you.")
                    time.sleep(1)
                    self.set_next_state("StateDead")
                elif msg.body == "victory":
                    print("Enemy: I expected more.")
                    time.sleep(1)
                    self.set_next_state("StateEscapedWithIt")
            else:
                self.set_next_state("StateCombat")

    class StateEscapedWithIt(State):
        async def run(self):
            print("Enemy: Time to go terrorize another regal family.")
            time.sleep(1)
            msg = spade.message.Message(
                to="narrator@localhost",
                body="victoryEnemy"
                )
            await self.send(msg)

    class StateDead(State):
        async def run(self):
            print("Enemy: *Years later, the dragon became little more than a scary bonfire story.*")

    async def setup(self):
        print("Enemy: Starting!")
        behaviourSetup = self.Setup()
        self.add_behaviour(behaviourSetup)

