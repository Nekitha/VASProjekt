#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import spade
import narrator
import hero
import enemy
import fate
import questgiver
from spade import quit_spade

if __name__ == '__main__':
    agentNarrator = narrator.Narrator("narrator@localhost", "narrator")
    agentHero = hero.Hero("hero@localhost", "hero")
    agentEnemy = enemy.Enemy("enemy@localhost", "enemy")
    agentQuestGiver = questgiver.Questgiver("questgiver@localhost", "questgiver")
    agentFate = fate.Fate("fate@localhost", "fate")
    startedUpNarrator = agentNarrator.start()
    startedUpHero = agentHero.start()
    startedUpEnemy = agentEnemy.start()
    startedUpQuestGiver = agentQuestGiver.start()
    startedUpFate = agentFate.start()
    characterAgents = []
    characterAgents.append(agentNarrator)
    characterAgents.append(agentHero)
    characterAgents.append(agentEnemy)
    characterAgents.append(agentQuestGiver)
    characterAgents.append(agentFate)
    startedUpNarrator.result()
    while agentNarrator.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    for character in characterAgents:
        character.stop()
    quit_spade()
    print("\n")
    print("A massive asteroid wipes out everyone, ending the story prematurely.")

