from player import Player
from collections import Counter

# inspired from this article https://medium.com/game-of-theories/the-game-theory-of-bullshit-aed0872251e8


class Saint(Player):
    """Player that never cheats and never checks"""

    def putCard(self, declared_card):
        assert self.cards is not None
        legal_cards = self.cards
        if declared_card is not None:
            legal_cards = list(
                filter(lambda c: c >= declared_card, legal_cards))

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
            legal_cards = list(
                filter(lambda c: c >= declared_card, legal_cards))

        if legal_cards:
            play = min(legal_cards, key=lambda c: c[0])
            return play, play

        if len(self.cards) == 1:
            return "draw"

        return min(self.cards, key=lambda c: c[0]), declared_card


class CountingCheatySaint(Saint):
    def checkCard(self, opponent_declaration):
        """Check if we have three cards of the type that player said"""
        counts = {}
        if self.cards is not None:
            counts = Counter([c[0] for c in self.cards])

        if counts[opponent_declaration] == 4:
            return True

        return False


class Accountant(Player):
    def __init__(self, name):
        super().__init__(name)
        self.pile = []
        self._num_his_checks = 0     # might be useful later
        self._just_played = None     # auxilary variable for counting cards in pile
        self._prev_cards = None

    def putCard(self, declared_card):
        self._just_played = True
        assert self.cards is not None
        legal_cards = self.cards
        if declared_card is not None:
            legal_cards = list(
                filter(lambda c: c >= declared_card, legal_cards))

        if legal_cards:
            play = min(legal_cards, key=lambda c: c[0])
            self.pile.append(play)
            return play, play

        if len(self.cards) == 1:
            return "draw"

        play = min(self.cards, key=lambda c: c[0])
        self.pile.append(play)
        return play, declared_card

    def checkCard(self, opponent_declaration):
        if opponent_declaration in self.cards or opponent_declaration in self.pile:
            return True

        return False

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        print(self._prev_cards, self.cards)
        if self._prev_cards != self.cards:
            print("[END]")
            self.pile = []

        if log:
            print("Feedback = " + self.name + " : checked this turn = " + str(checked) +
                  "; I checked = " + str(iChecked) + "; I drew cards = " +
                  str(iDrewCards) + "; revealed card = " +
                  str(revealedCard) + "; number of taken cards = " + str(noTakenCards))

        print("[ARGS]", checked, iChecked,
              iDrewCards, revealedCard, noTakenCards)
        print("[JUST PLAYED]", self._just_played)
        print("[BEFORE] I think that this was current pile", self.pile)

        if not checked:
            if noTakenCards is None:  # normal move
                if not self._just_played:
                    self.pile.append(None)
            else:  # drawn
                self.pile = self.pile[:-noTakenCards]
        else:  # someone checked
            if iChecked:
                if iDrewCards:
                    self.pile = self.pile[:-noTakenCards]
                else:
                    self.pile = self.pile[:-noTakenCards+1]
            else:
                if iDrewCards:
                    self.pile = self.pile[:-noTakenCards]
                else:
                    self.pile = self.pile[:-noTakenCards]

        if self._just_played:
            self._just_played = False

        print("[AFTER] I think that this is current pile", self.pile)

        assert self.cards is not None
        self._prev_cards = self.cards.copy()
        # if not self.cards:
        #     print("[VICTORY]!!!")
        #     self.pile = []

        # if len(self.cards) + len(self.pile) == 26:
        #     print("[DEFEAT]!!!")
        #     self.pile = []