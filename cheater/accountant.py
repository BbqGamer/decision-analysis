import random

from player import Player


class Accountant(Player):
    """Player tries to count cards in his hand and some of cards in the pile, then it makes decision accordingly"""

    def __init__(self, name, cheating_strategy="pile", log=False):  # only run once
        super().__init__(name)
        self._just_played = False  # auxilary variable for counting cards in pile
        self._reset_counts()

        self.cheating_strategy = cheating_strategy

        self.log = log

    def putCard(self, declared_card):
        self._just_played = True
        assert self.cards is not None

        legal_cards = self.cards

        # Update legal cards with respect to the declared card
        if declared_card is not None:
            legal_cards = list(filter(lambda c: c >= declared_card, legal_cards))

        # Play the smallest legal card
        if legal_cards:
            smallest_legal = min(legal_cards, key=lambda c: c[0])
            self.pile.append(smallest_legal)
            return tuple(smallest_legal), tuple(smallest_legal)

        # Play the very last card safely
        if len(self.cards) == 1:
            return "draw"

        # Cheat by playing the smallest card
        smallest_illegal = min(self.cards, key=lambda c: c[0])
        self.pile.append(smallest_illegal)

        # Declare card value based on cheating strategy

        declare = None

        if self.cheating_strategy == "pile":
            for card in self.pile:
                if card is not None and card[0] >= declared_card[0]:
                    declare = tuple(card)
                    break

        if declare is None:
            declare = (
                {
                    "min": declared_card[0],
                    "max": 14,
                    "random": random.randint(declared_card[0], 14),
                    "pile": 14,
                }[self.cheating_strategy],
                random.randint(0, 3),
            )

        return (tuple(smallest_illegal), tuple(declare))

    def checkCard(self, opponent_declaration):
        assert self.cards is not None
        if opponent_declaration in self.cards or opponent_declaration in self.pile:
            return True

        n_his_cards = 16 - len(self.cards) - len(self.pile)

        known = filter(lambda a: a is not None, self.cards + self.pile)
        unknown = self._getDeck() - set(known)
        legal = list(filter(lambda c: c[0] >= opponent_declaration[0], unknown))
        nunknown = len(unknown)
        nlegal = len(legal)
        nillegal = nunknown - nlegal

        # calculate chance that opponent doesn't have the required card
        # if has more cards than illegal
        if n_his_cards > nillegal:
            return False

        prob_doesnt_have = 1
        for i in range(n_his_cards):
            x = (nillegal - i) / (nunknown - i)
            prob_doesnt_have *= x

        if self.log:
            print("Possible cards: ", legal)
            print("Probability ", prob_doesnt_have)
        return random.random() < prob_doesnt_have

    def getCheckFeedback(
        self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=False
    ):
        assert self.cards is not None
        self.playing_set = self.playing_set | set(self.cards)
        if log:
            print(
                "Feedback = "
                + self.name
                + " : checked this turn = "
                + str(checked)
                + "; I checked = "
                + str(iChecked)
                + "; I drew cards = "
                + str(iDrewCards)
                + "; revealed card = "
                + str(revealedCard)
                + "; number of taken cards = "
                + str(noTakenCards)
            )

            print("[ARGS]", checked, iChecked, iDrewCards, revealedCard, noTakenCards)
            print(self.playing_set)
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
                    self.pile = self.pile[: -noTakenCards + 1]
            else:
                if iDrewCards:
                    self.pile = self.pile[:-noTakenCards]
                else:
                    self.pile = self.pile[:-noTakenCards]

        if log:
            print("[AFTER] I think that this is current pile", self.pile)

        if self._just_played:
            self.i_moved += 1
        else:
            self.he_moved += 1

        if self._just_played:
            self._just_played = False

        if self.i_moved > 100 or self.he_moved > 100:
            if log:
                print("END - Draw")
            self._reset_counts()

        assert self.cards is not None
        if len(self.cards) == 0:
            if log:
                print("END - Victory")
            self._reset_counts()

        his_cards = 16 - len(self.cards) - len(self.pile)
        if his_cards == 0:
            if log:
                print("END - Defeat")
            self._reset_counts()

    def _reset_counts(self):
        self.pile = []
        self.i_moved = 0
        self.he_moved = 0
        self.playing_set = set()

    def _getDeck(self):
        return set([(number, color) for color in range(4) for number in range(9, 15)])
