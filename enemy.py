#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import spade
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
                self.agent.name = msg.body.split(";")[0]
                self.agent.person = msg.body.split(";")[1]
                self.agent.add_behaviour(self.agent.ShowThing())
                self.kill()
            else:
                1+1

    class ShowThing(OneShotBehaviour):
        async def run(self):
            print("Enemy: " + self.agent.name + " " + self.agent.person)

    async def setup(self):
        print("Enemy: Starting!")
        behaviourSetup = self.Setup()
        self.add_behaviour(behaviourSetup)

