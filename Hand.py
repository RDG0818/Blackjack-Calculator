from Card import *
from typing import Optional

class Hand:
    def __init__(self, card_list: Optional[list] = None) -> None:
        if card_list == None:
            self.cards = []
        else:
            self.cards = card_list

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def value(self) -> int:
        value = sum(card.value() for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank == 'A')
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1
        return value
    
    def is_bust(self) -> bool:
        return self.value() > 21
    
    def __eq__(self, other: "Hand") -> bool:
        if not isinstance(other, Hand):
            return False
        return self.cards == other.cards
    
    def __str__(self) -> str:
        return ", ".join(str(card) for card in self.cards)
    