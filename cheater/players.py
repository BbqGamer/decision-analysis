import random
from typing import Any

from accountant import Accountant
from player import Player

# inspired from this article https://medium.com/game-of-theories/the-game-theory-of-bullshit-aed0872251e8


class Saint(Player):
    """Player that never cheats and never checks"""

    def putCard(self, declared_card):
        assert self.cards is not None
        legal_cards = self.cards
        if declared_card is not None:
            legal_cards = list(filter(lambda c: c >= declared_card, legal_cards))

        if legal_cards:
            play = min(legal_cards, key=lambda c: c[0])
            return play, play
        return "draw"

    def checkCard(self, opponent_declaration):
        return False


class CheatySaint(Saint):
    """Player that only cheats when can't play a cards (or draws if has one card) and never checks"""

    def putCard(self, declared_card):
        assert self.cards is not None
        legal_cards = self.cards
        if declared_card is not None:
            legal_cards = list(filter(lambda c: c >= declared_card, legal_cards))

        if legal_cards:
            play = min(legal_cards, key=lambda c: c[0])
            return play, play

        if len(self.cards) == 1:
            return "draw"

        return min(self.cards, key=lambda c: c[0]), declared_card


class Acer(Player):
    """Player draws if has to plays card if can and cheats
    by playing some random ace whenever can't place card
    """

    def putCard(self, declared_card):
        if len(self.cards) == 1:
            if declared_card and (declared_card[0] > self.cards[0][0]):
                return "draw"
            else:
                return self.cards[0], self.cards[0]
        play = min(self.cards, key=lambda c: c[0])
        if play[1] == 14:  # if ace
            return play, play
        return play, (14, random.randint(0, 3))

    def checkCard(self, opponent_declaration):
        if opponent_declaration in self.cards:
            return True
        return False


class AccountantFactory:
    def __init__(self, min_cheat=True, log=False):
        self.min_cheat = min_cheat
        self.log = log

    def __call__(self, name, *args: Any, **kwds: Any) -> Any:
        return Accountant(name=name, min_cheat=self.min_cheat, log=self.log)
