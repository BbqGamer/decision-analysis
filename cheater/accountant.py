from player import Player


class Accountant(Player):
    def __init__(self, name):  # only run once
        super().__init__(name)
        self._just_played = False    # auxilary variable for counting cards in pile
        self._reset_counts()

    def putCard(self, declared_card):
        self._just_played = True
        assert self.cards is not None
        self.playing_set = self.playing_set | set(self.cards)

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
        if log:
            print("Feedback = " + self.name + " : checked this turn = " + str(checked) +
                  "; I checked = " + str(iChecked) + "; I drew cards = " +
                  str(iDrewCards) + "; revealed card = " +
                  str(revealedCard) + "; number of taken cards = " + str(noTakenCards))

        print("[ARGS]", checked, iChecked,
              iDrewCards, revealedCard, noTakenCards)
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
                    self.pile = self.pile[:-noTakenCards+1]
            else:
                if iDrewCards:
                    self.pile = self.pile[:-noTakenCards]
                else:
                    self.pile = self.pile[:-noTakenCards]

        print("[AFTER] I think that this is current pile", self.pile)

        if self._just_played:
            self.i_moved += 1
        else:
            self.he_moved += 1

        if self._just_played:
            self._just_played = False

        if self.i_moved > 100 or self.he_moved > 100:
            print("END - Draw")
            self._reset_counts()

        assert self.cards is not None
        if len(self.cards) == 0:
            print("END - Victory")
            self._reset_counts()

        his_cards = 16 - len(self.cards) - len(self.pile)
        if his_cards == 0:
            print("END - Defeat")
            self._reset_counts()

    def _reset_counts(self):
        self.pile = []
        self.i_moved = 0
        self.he_moved = 0
        self.playing_set = set()
