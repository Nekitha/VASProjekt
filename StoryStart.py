#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import spade
import narrator
import hero
import enemy
import questgiver
from spade import quit_spade

if __name__ == '__main__':    
    agentHero = hero.Hero("hero@localhost", "hero")
    agentEnemy = enemy.Enemy("enemy@localhost", "enemy")
    agentQuestGiver = questgiver.Questgiver("questgiver@localhost", "questgiver")
    agentNarrator = narrator.Narrator("narrator@localhost", "narrator")
    
    startedUpHero = agentHero.start()
    startedUpHero.result()
    
    startedUpQuestGiver = agentQuestGiver.start()
    startedUpQuestGiver.result()

    startedUpEnemy = agentEnemy.start()
    startedUpEnemy.result()
    
    startedUpNarrator = agentNarrator.start()
    startedUpNarrator.result()    
    
    characterAgents = []
    
    characterAgents.append(agentHero)
    characterAgents.append(agentEnemy)
    characterAgents.append(agentQuestGiver)
    characterAgents.append(agentNarrator)

    while agentHero.is_alive() and agentNarrator.storyOver == False:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    for character in characterAgents:
        if character.is_alive() == True:
            character.stop()
    quit_spade()
    print("\n")
    if agentNarrator.storyOver == False:
        print("A massive asteroid wipes out everyone, ending the story prematurely.")
    else:
        print("The story is over, thank you for reading.")

