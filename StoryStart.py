#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import spade
import narrator
from spade import quit_spade

if __name__ == '__main__':
    storyteller = narrator.Narrator("narrator@localhost", "narrator")
    startedUp = storyteller.start()
    startedUp.result()  # pričekamo kraj pokretanja agenta
    while storyteller.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    for character in storyteller.characters:
        character.stop()
    quit_spade()
    print("\n")
    print("A massive asteroid wipes out everyone, ending the story prematurely.")

