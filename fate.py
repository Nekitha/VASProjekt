#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import spade
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import quit_spade
from spade.behaviour import TimeoutBehaviour, CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour

class Fate(Agent):
    
    class Setup(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"Fate: Primio sam poruku sadržaja: {msg.body}")
                self.kill()
            else:
                print("Fate: Čekao sam, ali poruke nema.")

    async def setup(self):
        print("Fate: Starting!")
        behaviourSetup = self.Setup()
        self.add_behaviour(behaviourSetup)

