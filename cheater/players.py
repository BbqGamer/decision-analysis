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
        # self.his_counts = [None] * 9
        self._pile_counts = [None] * 6
        self._num_his_checks = 0     # might be useful later
        self._just_played = None     # auxilary variable for counting cards in pile
        self._last_declaration = None

    def putCard(self, declared_card):
        assert self.cards is not None
        legal_cards = self.cards
        if declared_card is not None:
            legal_cards = list(
                filter(lambda c: c >= declared_card, legal_cards))

        if legal_cards:
            play = min(legal_cards, key=lambda c: c[0])
            self._just_played = play
            self._last_declaration = play
            return play, play

        if len(self.cards) == 1:
            self._last_declaration = None
            return "draw"

        play = min(self.cards, key=lambda c: c[0])
        self._just_played = play
        self._last_declaration = declared_card
        return play, declared_card

    def checkCard(self, opponent_declaration):
        if opponent_declaration in self.cards or opponent_declaration in self._pile_counts:
            return True

        return False

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        if log:
            print("Feedback = " + self.name + " : checked this turn = " + str(checked) +
                  "; I checked = " + str(iChecked) + "; I drew cards = " +
                  str(iDrewCards) + "; revealed card = " +
                  str(revealedCard) + "; number of taken cards = " + str(noTakenCards))

        if noTakenCards:
            assert self.cards is not None
            drawn = self._pile_counts[-noTakenCards:]
            self._pile_counts = self._pile_counts[:-noTakenCards]
        else:
            if self._just_played:
                self._pile_counts.append(self._just_played)
                self._just_played = None
            else:
                self._pile_counts.append(None)

        if checked and not iChecked:
            self._num_his_checks += 1
