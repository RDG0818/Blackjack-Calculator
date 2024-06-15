from Hand import *
from Deck import *

class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.hand = Hand()

    def hit(self, deck: Deck) -> None:
        self.hand.add_card(deck.deal_card())

    def stand(self) -> None:
        pass

    def is_bust(self) -> bool:
        return self.hand.is_bust()
    
    def hand_value(self) -> int:
        return self.hand.value()
    
    